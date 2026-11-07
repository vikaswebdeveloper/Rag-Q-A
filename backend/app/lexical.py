import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Optional

import bm25s
from bm25s.tokenization import Tokenizer

logger = logging.getLogger("rag.lexical")

QUESTION_WORDS = (
    "what who whom whose how when where which why does did do can could would "
    "should tell explain describe me about many much"
).split()

Stopwords = list(bm25s.stopwords.STOPWORDS_EN) + QUESTION_WORDS

# Global state
_lock = threading.Lock()
_buildLock = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=1)
_pendingRebuild = threading.Event()

_retriever: Optional[bm25s.BM25] = None
_tokenizer: Optional[Tokenizer] = None
_chunk_ids: list[str] = []


def _create_tokenizer() -> Tokenizer:
    return Tokenizer(stopwords=Stopwords, splitter=r"[^\W_]+")


def _build_index(getCollection: Callable[[], Any]):
    global _retriever, _tokenizer, _chunk_ids
    with _buildLock:
        _pendingRebuild.clear()
        try:
            collection = getCollection()
            result = collection.get(include=["documents"])
            ids = result.get("ids", [])
            documents = result.get("documents", [])

            if not ids or not documents:
                with _lock:
                    _retriever = None
                    _tokenizer = _create_tokenizer()
                    _chunk_ids = []
                return

            tokenizer = _create_tokenizer()
            tokens = tokenizer.tokenize(documents, show_progress=False)
            retriever = bm25s.BM25()
            retriever.index(tokens, show_progress=False)

            with _lock:
                _retriever = retriever
                _tokenizer = tokenizer
                _chunk_ids = list(ids)

            logger.info("BM25 index built with %d documents.", len(ids))
        except Exception as e:
            logger.error("Failed to build BM25 index: %s", e)


def ensure(getCollection: Callable[[], Any]):
    """Build the index on first use (called at startup)."""
    with _lock:
        if _retriever is not None:
            return
    _build_index(getCollection)


def scheduleRebuild(getCollection: Callable[[], Any]):
    """Rebuild in the background on a single-thread executor. Several quick changes share one rebuild."""
    if _pendingRebuild.is_set():
        return
    _pendingRebuild.set()

    def task():
        _build_index(getCollection)

    _executor.submit(task)


def search(question: str, n: int) -> list[str]:
    """Tokenize the question (update_vocab=False). Return chunk ids with score > 0, best first."""
    with _lock:
        if _retriever is None or _tokenizer is None or not _chunk_ids:
            return []
        retriever = _retriever
        tokenizer = _tokenizer
        chunk_ids = _chunk_ids

    tokens = tokenizer.tokenize([question], update_vocab=False, show_progress=False)
    # Check if there are any valid tokens
    if hasattr(tokens, "shape") and tokens.shape[1] == 0:
        return []
    if isinstance(tokens, list) and (not tokens or not tokens[0]):
        return []

    try:
        k = min(n, len(chunk_ids))
        if k <= 0:
            return []
        doc_indices, scores = retriever.retrieve(tokens, k=k, show_progress=False)
        first_indices = doc_indices[0]
        first_scores = scores[0]

        results = []
        for idx, score in zip(first_indices, first_scores):
            if score > 0 and 0 <= idx < len(chunk_ids):
                results.append(chunk_ids[idx])
        return results
    except Exception as e:
        logger.error("BM25 search error: %s", e)
        return []

