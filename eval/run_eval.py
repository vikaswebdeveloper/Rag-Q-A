import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

ProjectRoot = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ProjectRoot))
sys.path.insert(0, str(ProjectRoot / "backend"))

from backend.app.config import settings
from backend.app.loaders import slugFor
from backend.app import rag

EvalDir = ProjectRoot / "eval"
ResultsDir = EvalDir / "results"
ResultsDir.mkdir(parents=True, exist_ok=True)
TestsetPath = EvalDir / "testset.json"

RefusalPatterns = [
    r"not contain",
    r"no information",
    r"cannot",
    r"not mentioned",
    r"does not mention",
    r"not provided",
    r"missing",
    r"not found",
    r"outside the scope",
]


def load_testset() -> list[dict[str, Any]]:
    if not TestsetPath.exists():
        print(f"Error: {TestsetPath} not found.")
        sys.exit(1)
    return json.loads(TestsetPath.read_text(encoding="utf-8"))


def get_stem_from_source(source: str) -> str:
    slug = slugFor(source)
    # remove trailing extension if any
    return slug.replace(re.search(r"-[a-z0-9]+$", slug).group(0), "") if re.search(r"-[a-z0-9]+$", slug) else slug


def run_retrieval(testset: list[dict[str, Any]]):
    print("--- Running Retrieval Evaluation ---")
    rag.getKeywordIndex()

    hit_1 = 0
    hit_3 = 0
    hit_5 = 0
    hit_10 = 0
    reciprocal_ranks = []
    evaluated_count = 0

    results_log = []

    for item in testset:
        # Only evaluate fact and followup questions that have gold targets
        gold_stems = [g.lower() for g in item.get("gold", [])]
        if not gold_stems:
            continue

        evaluated_count += 1
        query = item["turns"][-1]

        # Use full conversational context for followups
        if len(item["turns"]) > 1:
            search_query = f"{item['turns'][-2]}\n{query}"
        else:
            search_query = query

        documents, metadatas, distances = rag.search(search_query, topK=10)
        retrieved_stems = []
        for m in metadatas:
            src = m.get("source", "")
            s_stem = Path(src).stem.lower()
            retrieved_stems.append(s_stem)

        # Calculate hits
        h1 = any(s in gold_stems for s in retrieved_stems[:1])
        h3 = any(s in gold_stems for s in retrieved_stems[:3])
        h5 = any(s in gold_stems for s in retrieved_stems[:5])
        h10 = any(s in gold_stems for s in retrieved_stems[:10])

        if h1:
            hit_1 += 1
        if h3:
            hit_3 += 1
        if h5:
            hit_5 += 1
        if h10:
            hit_10 += 1

        # Calculate RR
        rr = 0.0
        for rank, s in enumerate(retrieved_stems, start=1):
            if s in gold_stems:
                rr = 1.0 / rank
                break
        reciprocal_ranks.append(rr)

        results_log.append({
            "id": item["id"],
            "query": query,
            "gold": gold_stems,
            "retrieved": retrieved_stems,
            "mrr": rr,
            "hit@1": h1,
            "hit@5": h5,
            "hit@10": h10,
        })

    mrr = sum(reciprocal_ranks) / max(1, evaluated_count)
    hit1_pct = (hit_1 / evaluated_count) * 100
    hit3_pct = (hit_3 / evaluated_count) * 100
    hit5_pct = (hit_5 / evaluated_count) * 100
    hit10_pct = (hit_10 / evaluated_count) * 100

    metrics = {
        "evaluated_questions": evaluated_count,
        "hit@1": round(hit1_pct, 2),
        "hit@3": round(hit3_pct, 2),
        "hit@5": round(hit5_pct, 2),
        "hit@10": round(hit10_pct, 2),
        "mrr": round(mrr, 4),
        "details": results_log,
    }

    out_file = ResultsDir / "retrieval.json"
    out_file.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"\nResults on {evaluated_count} questions:")
    print(f"  • Hit@1:  {hit1_pct:.1f}%")
    print(f"  • Hit@3:  {hit3_pct:.1f}%")
    print(f"  • Hit@5:  {hit5_pct:.1f}%")
    print(f"  • Hit@10: {hit10_pct:.1f}% (Target: >= 95%)")
    print(f"  • MRR:    {mrr:.4f} (Target: >= 0.90)")
    print(f"Saved to {out_file}\n")


def run_answers(testset: list[dict[str, Any]]):
    print("--- Running Answers Evaluation ---")
    correct_count = 0
    unans_refused_count = 0
    total_unans = 0
    results_log = []

    for item in testset:
        turns = item["turns"]
        is_unans = item["type"] == "unanswerable"
        if is_unans:
            total_unans += 1

        history = []
        answer = ""

        # For multi-turn, run through turns
        for t_idx, q in enumerate(turns):
            search_query = f"{turns[t_idx-1]}\n{q}" if t_idx > 0 else q
            documents, metadatas, distances = rag.search(search_query)
            messages = rag.buildMessages(q, documents, history)

            try:
                tokens = list(rag.streamAnswer(messages))
                answer = "".join(tokens)
            except Exception as e:
                # If LLM offline, note failure
                answer = f"[LLM Unavailable: {e}]"

            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": answer})

        # Grade answer
        if is_unans:
            refused = any(re.search(pat, answer, re.IGNORECASE) for pat in RefusalPatterns)
            if refused:
                unans_refused_count += 1
            results_log.append({
                "id": item["id"],
                "type": item["type"],
                "question": turns[-1],
                "answer": answer,
                "refused": refused,
            })
        else:
            # Check fact groups
            fact_groups = item.get("facts", [])
            facts_passed = True
            for fg in fact_groups:
                matched = any(re.search(rf"\b{re.escape(spell)}\b", answer, re.IGNORECASE) for spell in fg)
                if not matched:
                    facts_passed = False
                    break
            if facts_passed and fact_groups:
                correct_count += 1

            results_log.append({
                "id": item["id"],
                "type": item["type"],
                "question": turns[-1],
                "answer": answer,
                "passed": facts_passed,
            })

    total_fact_q = len(testset) - total_unans
    fact_pct = (correct_count / max(1, total_fact_q)) * 100
    unans_pct = (unans_refused_count / max(1, total_unans)) * 100

    metrics = {
        "total_questions": len(testset),
        "fact_accuracy": round(fact_pct, 2),
        "unanswerable_refusal_rate": round(unans_pct, 2),
        "details": results_log,
    }

    out_file = ResultsDir / "answers.json"
    out_file.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Results:")
    print(f"  • Correct Facts: {correct_count}/{total_fact_q} ({fact_pct:.1f}%)")
    print(f"  • Refusal Rate:  {unans_refused_count}/{total_unans} ({unans_pct:.1f}%)")
    print(f"Saved to {out_file}\n")


def run_speed(testset: list[dict[str, Any]]):
    print("--- Running Speed & Concurrency Benchmark ---")
    rag.getKeywordIndex()

    # 1. Search Latency Benchmark over 50 queries
    queries = [item["turns"][-1] for item in testset]
    latencies = []

    for q in queries:
        t0 = time.perf_counter()
        rag.search(q, topK=5)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000)  # ms

    latencies.sort()
    p50 = latencies[len(latencies) // 2]
    p95 = latencies[int(len(latencies) * 0.95)]
    avg_latency = sum(latencies) / len(latencies)

    print(f"Search Latency ({len(queries)} queries):")
    print(f"  • p50: {p50:.2f} ms")
    print(f"  • p95: {p95:.2f} ms")
    print(f"  • Avg: {avg_latency:.2f} ms")

    # 2. Concurrency test: 4 simultaneous search workers
    print("\nRunning 4 Simultaneous Search Users Test...")
    concurrent_latencies = []
    errors = 0

    def worker_task(q_text: str):
        nonlocal errors
        try:
            w_t0 = time.perf_counter()
            rag.search(q_text, topK=5)
            w_t1 = time.perf_counter()
            return (w_t1 - w_t0) * 1000
        except Exception:
            errors += 1
            return 0.0

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker_task, q) for q in queries]
        for f in futures:
            res = f.result()
            if res > 0:
                concurrent_latencies.append(res)

    avg_wait = sum(concurrent_latencies) / max(1, len(concurrent_latencies))
    max_wait = max(concurrent_latencies) if concurrent_latencies else 0.0

    print(f"Concurrent Test Results:")
    print(f"  • Simultaneous workers: 4")
    print(f"  • Errors: {errors}")
    print(f"  • Average wait: {avg_wait:.2f} ms")
    print(f"  • Maximum wait: {max_wait:.2f} ms")

    metrics = {
        "search_p50_ms": round(p50, 2),
        "search_p95_ms": round(p95, 2),
        "search_avg_ms": round(avg_latency, 2),
        "concurrent_4_users": {
            "errors": errors,
            "average_wait_ms": round(avg_wait, 2),
            "max_wait_ms": round(max_wait, 2),
        },
    }

    out_file = ResultsDir / "speed.json"
    out_file.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Saved to {out_file}\n")


def main():
    parser = argparse.ArgumentParser(description="Run evaluation benchmarks for RAG Q&A")
    parser.add_argument("subcommand", choices=["retrieval", "answers", "speed", "all"], help="Subcommand to run")
    args = parser.parse_args()

    testset = load_testset()

    if args.subcommand in ("retrieval", "all"):
        run_retrieval(testset)

    if args.subcommand in ("speed", "all"):
        run_speed(testset)

    if args.subcommand in ("answers", "all"):
        run_answers(testset)


if __name__ == "__main__":
    main()

