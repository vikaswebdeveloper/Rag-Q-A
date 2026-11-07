import concurrent.futures
import json
import logging
import re
import threading
import time
from collections import OrderedDict, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator, Optional

import chromadb
from fastembed.rerank.cross_encoder import TextCrossEncoder

from backend.app.config import settings
from backend.app.embedding import get_embedding_function
from backend.app.loaders import slugFor
from backend.app import lexical, llm

logger = logging.getLogger("rag")

_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="rag_search")


class RetrievalCache:
    """Thread-safe in-memory LRU cache with TTL for search results."""

    def __init__(self, maxsize: int = 128, ttl_seconds: int = 3600):
        self.maxsize = maxsize
        self.ttl = ttl_seconds
        self._cache: OrderedDict[tuple[str, int], tuple[float, tuple]] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: tuple[str, int]) -> Optional[tuple]:
        with self._lock:
            if key not in self._cache:
                return None
            ts, val = self._cache[key]
            if time.time() - ts > self.ttl:
                del self._cache[key]
                return None
            self._cache.move_to_end(key)
            return val

    def set(self, key: tuple[str, int], val: tuple) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (time.time(), val)
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


_retrieval_cache = RetrievalCache()


def clear_retrieval_cache():
    """Clear all cached search and re-rank results."""
    _retrieval_cache.clear()


SYSTEM_PROMPT = """You are the AI Librarian for the digital library.
Your goal is to answer the user's question clearly, accurately, and concisely based strictly on the retrieved library context.

Guidelines:
1. Conciseness: Keep your response direct and focused (typically 2 to 3 short paragraphs or clean bullet points). Do not write unnecessarily long essays.
2. Direct Answer: Answer the question directly right away. Never use generic filler, preamble, or meta-headers like "Short answer:", "Based on the retrieved context:", or "What the retrieved information tells us:".
3. Formatting: Use clean markdown with brief paragraphs, bold key terms, and bullet points for readability. Avoid markdown tables unless specifically requested, as tables are difficult to read in a narrow chat window.
4. Relevance: Only answer what was asked. Do not summarize unrelated passages (e.g. if asked about health, do not discuss bean roasting or agricultural history unless directly relevant).
5. Grounding: Rely strictly on the provided context. If the context does not contain enough information to answer the question, state clearly and politely what is missing rather than speculating."""


@lru_cache(maxsize=1)
def getCollection():
    """Persistent Chroma client and collection with configured embedding model."""
    resolved_path = settings.resolve(settings.CHROMA_PATH)
    client = chromadb.PersistentClient(path=str(resolved_path))
    ef = get_embedding_function()
    try:
        return client.get_or_create_collection(name=settings.CHROMA_COLLECTION, embedding_function=ef)
    except Exception as e:
        if "Embedding function conflict" in str(e) or "already exists" in str(e):
            return client.get_collection(name=settings.CHROMA_COLLECTION, embedding_function=ef)
        raise e


@lru_cache(maxsize=1)
def getReranker() -> TextCrossEncoder:
    """Cached FastEmbed cross-encoder model."""
    return TextCrossEncoder(model_name=settings.RERANK_MODEL)


def getKeywordIndex():
    """Ensure BM25 keyword index is built."""
    lexical.ensure(getCollection)


def refreshKeywordIndex():
    """Schedule rebuild of BM25 index when hybrid search is active and invalidate cache."""
    clear_retrieval_cache()
    if settings.HYBRID:
        lexical.scheduleRebuild(getCollection)


def fuse(rankings: list[list[str]], k: int = 60) -> list[str]:
    """Reciprocal Rank Fusion. Score = 1 / (k + rank), 1-based rank."""
    scores: dict[str, float] = defaultdict(float)
    for r_list in rankings:
        for rank, item_id in enumerate(r_list, start=1):
            scores[item_id] += 1.0 / (k + rank)
    sorted_items = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return sorted_items


def _query_vector(collection, question: str, n_results: int):
    return collection.query(
        query_texts=[question],
        n_results=min(n_results, max(1, collection.count())),
        include=["documents", "metadatas", "distances"],
    )


def candidates(question: str) -> list[tuple[str, dict[str, Any], Optional[float]]]:
    """Retrieve vector and optional keyword search candidates in parallel, fused with RRF."""
    collection = getCollection()
    if settings.HYBRID:
        lexical.ensure(getCollection)
    n_results = settings.CANDIDATES if settings.RERANK else settings.TOP_K

    # Launch vector search and lexical search concurrently
    fut_vec = _thread_pool.submit(_query_vector, collection, question, n_results)
    fut_lex = (
        _thread_pool.submit(lexical.search, question, settings.KEYWORD_CANDIDATES)
        if settings.HYBRID
        else None
    )

    vec_res = fut_vec.result()
    vec_ids = vec_res.get("ids", [[]])[0]
    vec_docs = vec_res.get("documents", [[]])[0]
    vec_metas = vec_res.get("metadatas", [[]])[0]
    vec_dists = vec_res.get("distances", [[]])[0]

    id_map: dict[str, tuple[str, dict[str, Any], Optional[float]]] = {}
    for cid, doc, meta, dist in zip(vec_ids, vec_docs, vec_metas, vec_dists):
        id_map[cid] = (doc, meta, dist)

    rankings = [vec_ids]

    if fut_lex is not None:
        kw_ids = fut_lex.result()
        rankings.append(kw_ids)

        missing_ids = [kid for kid in kw_ids if kid not in id_map]
        if missing_ids:
            fetched = collection.get(ids=missing_ids, include=["documents", "metadatas"])
            f_ids = fetched.get("ids", [])
            f_docs = fetched.get("documents", [])
            f_metas = fetched.get("metadatas", [])
            for cid, doc, meta in zip(f_ids, f_docs, f_metas):
                id_map[cid] = (doc, meta, None)

    fused_ids = fuse(rankings)[:settings.CANDIDATES]
    return [id_map[cid] for cid in fused_ids if cid in id_map]


def _extract_words(text: str) -> set[str]:
    lines = text.split("\n", 1)
    body = lines[1] if len(lines) > 1 else lines[0]
    words = re.findall(r"\b[a-zA-Z0-9]+\b", body.lower())
    return set(words)


def dropCopies(
    passages: list[tuple[str, dict[str, Any], Optional[float]]],
    overlap: float = 0.8,
) -> list[tuple[str, dict[str, Any], Optional[float]]]:
    """Drop duplicate passages from same article stem sharing >= 80% words."""
    kept: list[tuple[str, dict[str, Any], Optional[float]]] = []
    seen_stems: dict[str, list[set[str]]] = defaultdict(list)

    for doc, meta, dist in passages:
        source = meta.get("source", "")
        stem = Path(source).stem.lower()

        words = _extract_words(doc)
        if not words:
            kept.append((doc, meta, dist))
            continue

        is_duplicate = False
        for prev_words in seen_stems[stem]:
            min_len = min(len(words), len(prev_words))
            if min_len == 0:
                continue
            shared = len(words & prev_words)
            if shared / min_len >= overlap:
                is_duplicate = True
                break

        if not is_duplicate:
            seen_stems[stem].append(words)
            kept.append((doc, meta, dist))

    return kept


def search(
    question: str,
    topK: Optional[int] = None,
) -> tuple[list[str], list[dict[str, Any]], list[Optional[float]]]:
    """Search, deduplicate, re-rank, and return top passages with metadata and distances."""
    k = topK or settings.TOP_K
    cache_key = (question.strip().lower(), k)
    cached = _retrieval_cache.get(cache_key)
    if cached is not None:
        return cached

    cand_passages = dropCopies(candidates(question))

    if not cand_passages:
        empty_res = ([], [], [])
        _retrieval_cache.set(cache_key, empty_res)
        return empty_res

    if settings.RERANK and len(cand_passages) > 1:
        reranker = getReranker()
        texts = [p[0] for p in cand_passages]
        scores = list(reranker.rerank(question, texts))
        scored = list(zip(cand_passages, scores))
        scored.sort(key=lambda x: x[1], reverse=True)

        # Dynamic relevance threshold: prune low-scoring passages that drop off the score cliff
        is_jina = "jina" in settings.RERANK_MODEL.lower()
        max_drop = 1.6 if is_jina else 7.0
        min_cutoff = 0.2 if is_jina else -2.0

        top_score = scored[0][1]
        top = [scored[0][0]]
        for p, s in scored[1:k]:
            if top_score > 0 and (s < min_cutoff or (top_score - s) > max_drop):
                continue
            if top_score <= 0 and (top_score - s) > 1.0:
                continue
            top.append(p)
    else:
        top = cand_passages[:k]

    documents = [p[0] for p in top]
    metadatas = [p[1] for p in top]
    distances = [p[2] for p in top]
    result = (documents, metadatas, distances)
    _retrieval_cache.set(cache_key, result)
    return result


def collectSources(
    metadatas: list[dict[str, Any]],
    distances: list[Optional[float]],
) -> list[dict[str, Any]]:
    """One entry per document, in rank order."""
    sources: list[dict[str, Any]] = []
    seen_slugs = set()

    for meta, dist in zip(metadatas, distances):
        source_name = meta.get("source", "")
        slug = slugFor(source_name)
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        d_val = round(dist, 4) if dist is not None else None
        sources.append({
            "slug": slug,
            "section": meta.get("section", ""),
            "category": meta.get("category", "general"),
            "distance": d_val,
        })

    return sources


def buildMessages(question: str, documents: list[str], history: list[dict[str, str]]) -> list[dict[str, str]]:
    """Format prompt with system prompt, history, and retrieved context."""
    context_str = "\n---\n".join(documents)
    user_content = f"Retrieved Context:\n{context_str}\n\nUser Query:\n{question}"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_content})
    return messages


def streamAnswer(messages: list[dict]) -> Iterator[str]:
    """Yields tokens from LLM stream."""
    return llm.chatStream(messages)


def suggestFollowups(
    question: str,
    answer: str,
    sources: list[dict[str, Any]],
    count: int = 3,
) -> list[str]:
    """Generate short relevant follow-up questions."""
    unique_sections = sorted({s.get("section", "") for s in sources if s.get("section")})
    sections_str = ", ".join(unique_sections)

    sys_prompt = f"""Suggest {count} short follow-up questions the user might ask next, based on the conversation below.
Each question must be under 15 words, stand on its own (no "it" or "this" without saying what),
not repeat the question already asked, and be answerable from the same documents.
Reply with JSON only: {{"questions": ["...", "..."]}}"""

    user_msg = f"Question: {question}\n\nAnswer: {answer}\n\nDocument sections used: {sections_str}"
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_msg},
    ]

    schema = {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {"type": "string"},
            }
        },
        "required": ["questions"],
    }

    try:
        raw_json = llm.chatJson(messages, schema=schema, temperature=0.3, maxTokens=400)
        cleaned_json = raw_json.strip()
        if "```" in cleaned_json:
            m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned_json)
            if m:
                cleaned_json = m.group(1).strip()
        data = json.loads(cleaned_json)
        raw_questions = data.get("questions", [])
    except Exception as e:
        logger.warning("Error suggesting followups: %s", e)
        return []

    valid_questions = []
    norm_q = question.strip().lower()

    for q in raw_questions:
        if not isinstance(q, str):
            continue
        cleaned_q = q.strip()
        if not (6 <= len(cleaned_q) <= 150):
            continue
        if cleaned_q.lower() == norm_q:
            continue
        if not cleaned_q.endswith("?"):
            cleaned_q += "?"
        if cleaned_q not in valid_questions:
            valid_questions.append(cleaned_q)
        if len(valid_questions) >= count:
            break

    return valid_questions

