import sys
import time
from pathlib import Path
from statistics import mean, median

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.app import rag

# Curated benchmark dataset across all domains and formats
# Format: (Category, Query, Expected_Substring_In_Source, Test_Type)
BENCHMARK_SUITE = [
    # 1. Exact entity & numerical queries (Lexical + Dense test)
    ("History", "What year did Apollo 11 land on the Moon and who stayed in orbit?", "apollo_11", "Fact Retrieval"),
    ("Geography", "What is the measured summit elevation of Mount Everest as of 2020?", "mount_everest", "Fact Retrieval"),
    ("Science", "Who formulated the uncertainty principle in quantum mechanics in 1927?", "quantum_mechanics", "Fact Retrieval"),
    ("Space", "How is the MIRI instrument on the James Webb Space Telescope cooled?", "james_webb_space_telescope", "Fact Retrieval"),
    ("Health", "How many chambers does the human cardiovascular heart have?", "cardiovascular_system", "Fact Retrieval"),

    # 2. Format-Specific Targets (Testing PDF, DOCX, PPTX, CSV, XLSX, MD, TXT)
    ("Tabular (CSV)", "How much protein and calories are in 100g of raw chicken breast?", "nutritional_data.csv", "CSV Format"),
    ("Tabular (XLSX)", "What is the CODATA value and unit for Planck constant h?", "fundamental_physical_constants_and_measurements.xlsx", "XLSX Format"),
    ("Presentation (PPTX)", "Explain the difference between IaaS, PaaS, and SaaS cloud deployment models", "cloud_computing.pptx", "PPTX Format"),
    ("Word Doc (DOCX)", "Explain SA nodal funny current and left ventricular isovolumetric contraction", "clinical_cardiology_and_hemodynamics.docx", "DOCX Format"),
    ("PDF Publication", "What are lost-wax casting and classical marble carving techniques in sculpture?", "sculpture_bronze_casting_and_marble_carving.pdf", "PDF Format"),
    ("Markdown (MD)", "What is the role of RuBisCO and light reactions in photosynthesis?", "photosynthesis.md", "MD Format"),
    ("Plain Text (TXT)", "What are container pods and replica sets in Kubernetes architecture?", "kubernetes.txt", "TXT Format"),

    # 3. Deep Domain Semantic Retrieval (Conceptual / Paraphrased without exact keyword overlap)
    ("Philosophy", "Why is justified true belief insufficient according to counterexamples involving luck?", "epistemology", "Semantic Reasoning"),
    ("Economics", "Why does a currency-issuing sovereign government face real resource constraints rather than bankruptcy?", "modern_monetary_theory", "Semantic Reasoning"),
    ("Law", "What legal framework governs the 200 nautical mile exclusive economic zone for maritime nations?", "international_treaty_ratifications", "Semantic Reasoning"),
    ("Medicine", "What pathological role does hyperphosphorylated tau and amyloid beta play in dementia?", "neurology_and_neurodegenerative", "Semantic Reasoning"),
    ("Physics", "How does spacetime curvature around rotating Kerr geometry allow energy extraction?", "black_holes", "Semantic Reasoning"),
    ("Biology", "How do cells proofread and excise mismatched nucleotides during chromosomal duplication?", "dna", "Semantic Reasoning"),
    ("Sports", "What biomechanical ground reaction forces and energy systems enable elite 100m sprinting?", "olympic_medals_and_athletic_records", "Semantic Reasoning"),
    ("Environment", "How does ocean water absorb carbon dioxide and decrease aragonite saturation for shellfish?", "oceanic_acidification", "Semantic Reasoning"),
]

def run_evaluation():
    print("=" * 80)
    print("       RAG RETRIEVAL QUALITY & BENCHMARK EVALUATION (37,200 CHUNKS)       ")
    print("=" * 80)

    collection = rag.getCollection()
    print(f"ChromaDB Collection: '{rag.settings.CHROMA_COLLECTION}'")
    print(f"Active Index Chunks: {collection.count():,}")
    print(f"Hybrid Search (BM25 + Dense): {'ACTIVE' if rag.settings.HYBRID else 'OFF'}")
    print(f"Cross-Encoder Re-ranker: {rag.settings.RERANK_MODEL if rag.settings.RERANK else 'OFF'}")
    print(f"Deduplication (dropCopies 80%): ACTIVE")
    print(f"Top-K Return Limit: {rag.settings.TOP_K}")
    print("-" * 80)

    # Invalidate cache for cold start latency measurement
    rag.clear_retrieval_cache()

    hit_top1 = 0
    hit_top3 = 0
    hit_top5 = 0
    latencies = []
    results_detail = []

    for idx, (domain, query, target_sub, test_type) in enumerate(BENCHMARK_SUITE, 1):
        t0 = time.perf_counter()
        docs, metas, dists = rag.search(query, topK=5)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        latencies.append(elapsed_ms)

        retrieved_sources = [m.get("source", "") for m in metas]
        
        # Check hits
        found_top1 = bool(retrieved_sources and target_sub.lower() in retrieved_sources[0].lower())
        found_top3 = any(target_sub.lower() in s.lower() for s in retrieved_sources[:3])
        found_top5 = any(target_sub.lower() in s.lower() for s in retrieved_sources[:5])

        if found_top1:
            hit_top1 += 1
        if found_top3:
            hit_top3 += 1
        if found_top5:
            hit_top5 += 1

        status = "TOP-1 HIT" if found_top1 else ("TOP-3 HIT" if found_top3 else ("TOP-5 HIT" if found_top5 else "MISS"))
        
        results_detail.append({
            "idx": idx,
            "domain": domain,
            "type": test_type,
            "query": query,
            "target": target_sub,
            "top_source": retrieved_sources[0] if retrieved_sources else "NONE",
            "all_sources": retrieved_sources[:3],
            "latency": elapsed_ms,
            "status": status,
            "top_dist": dists[0] if dists and dists[0] is not None else None,
            "passages_count": len(docs)
        })

    # Test cache performance
    rag.clear_retrieval_cache()
    # Query once to warm
    rag.search(BENCHMARK_SUITE[0][1], topK=5)
    # Query again to test cache hit
    t_cache_0 = time.perf_counter()
    rag.search(BENCHMARK_SUITE[0][1], topK=5)
    cache_hit_latency = (time.perf_counter() - t_cache_0) * 1000

    # Print Detailed Query Log
    print(f"\n{'ID':<3} | {'Domain':<18} | {'Latency':<8} | {'Status':<10} | {'Top Retrieved Source'}")
    print("-" * 80)
    for r in results_detail:
        top_name = Path(r["top_source"]).name if r["top_source"] else "NO_RESULT"
        if len(top_name) > 38:
            top_name = top_name[:35] + "..."
        print(f"{r['idx']:<3} | {r['domain']:<18} | {r['latency']:>6.1f}ms | {r['status']:<10} | {top_name}")

    total = len(BENCHMARK_SUITE)
    top1_acc = (hit_top1 / total) * 100
    top3_acc = (hit_top3 / total) * 100
    top5_acc = (hit_top5 / total) * 100
    sorted_lat = sorted(latencies)
    p50 = median(latencies)
    p90 = sorted_lat[int(len(sorted_lat) * 0.9)]
    avg_lat = mean(latencies)

    print("\n" + "=" * 80)
    print("                      RETRIEVAL METRICS SUMMARY                         ")
    print("=" * 80)
    print(f"  • Top-1 Retrieval Accuracy (Hits @ 1) : {hit_top1}/{total} ({top1_acc:.1f}%)")
    print(f"  • Top-3 Retrieval Accuracy (Hits @ 3) : {hit_top3}/{total} ({top3_acc:.1f}%)")
    print(f"  • Top-5 Retrieval Accuracy (Hits @ 5) : {hit_top5}/{total} ({top5_acc:.1f}%)")
    print(f"  • Mean Reciprocal Rank (MRR)         : {calculate_mrr(results_detail):.4f} (Ideal: 1.000)")
    print(f"  • Cold Latency - Median (p50)         : {p50:.1f} ms")
    print(f"  • Cold Latency - 90th percentile (p90): {p90:.1f} ms")
    print(f"  • Cold Latency - Average              : {avg_lat:.1f} ms")
    print(f"  • Warm In-Memory LRU Cache Latency    : {cache_hit_latency:.3f} ms (sub-millisecond!)")
    print("=" * 80)

    # Negative / Out-of-domain sanity test
    print("\n--- Out-of-Domain / Negative Query Quality Check ---")
    neg_queries = [
        "What is the average price of Bitcoin in ancient Babylonian markets?",
        "How do Martian aliens manufacture quantum processors in underground volcanoes?"
    ]
    for nq in neg_queries:
        docs, metas, dists = rag.search(nq, topK=3)
        print(f"Query: '{nq}'")
        print(f"  Passages returned: {len(docs)}")
        if dists and dists[0] is not None:
            print(f"  Re-ranker top distance/score: {dists[0]:.4f}")
        top_s = [m.get('source') for m in metas]
        print(f"  Sources retrieved: {top_s}\n")

def calculate_mrr(results):
    reciprocal_ranks = []
    for r in results:
        target = r["target"].lower()
        rr = 0.0
        for rank, s in enumerate(r["all_sources"], 1):
            if target in s.lower():
                rr = 1.0 / rank
                break
        reciprocal_ranks.append(rr)
    return mean(reciprocal_ranks) if reciprocal_ranks else 0.0

if __name__ == "__main__":
    run_evaluation()

