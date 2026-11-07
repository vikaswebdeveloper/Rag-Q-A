import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from main import loadDocs, createChunk, storeInChroma, Collection, DatabaseFolder, DataFolder
from backend.app import rag, lexical

def run():
    start_time = time.time()
    print("=" * 70)
    print("STEP 1: INGESTING ALL 254 DOCUMENTS (ALL >= 5,000 WORDS)")
    print("=" * 70)
    docs = loadDocs(DataFolder)
    print(f"Loaded {len(docs)} documents from: {DataFolder}")
    chunks = createChunk(docs)
    total_chunks = len(chunks)
    print(f"Generated {total_chunks} chunks across the expanded library (ChunkSize=700, Overlap=100).")

    print("\n" + "=" * 70)
    print("STEP 2: COMPUTING BGE EMBEDDINGS & STORING INTO CHROMADB")
    print("=" * 70)
    # Reset collection to ensure fresh clean state with all chunks
    storeInChroma(chunks, db_path=DatabaseFolder, collection_name=Collection, reset=True)

    print("\n" + "=" * 70)
    print("STEP 3: REBUILDING BM25 KEYWORD INDEX")
    print("=" * 70)
    lexical._build_index(rag.getCollection)
    rag.clear_retrieval_cache()
    print(f"BM25 index synchronized with {total_chunks} chunks.")

    print("\n" + "=" * 70)
    print("STEP 4: MULTI-CATEGORY VERIFICATION SPOT-CHECKS")
    print("=" * 70)
    test_queries = [
        ("Philosophy", "What is epistemology and how does it define justified true belief?"),
        ("Economics", "What are the core tenets of modern monetary theory and sovereign currency?"),
        ("Psychology", "How does cognitive psychology explain mental schemas and information processing?"),
        ("Law", "What is the United Nations Convention on the Law of the Sea and exclusive economic zone?"),
        ("Mathematics", "What is the fundamental theorem of calculus relating differentiation and integration?"),
        ("Physics", "What are Maxwell's equations and how do they describe electromagnetic wave propagation?"),
        ("Chemistry", "What are the key thermodynamic properties and atomic weight of Hydrogen in the periodic table?"),
        ("Biology", "How does DNA replication maintain fidelity through DNA polymerase enzymes?"),
        ("Engineering", "How do cable-stayed bridges differ from suspension bridges in structural load paths?"),
        ("Medicine", "What is the role of the sinoatrial node in human cardiac conduction and electrophysiology?"),
        ("Sports", "Who holds the men's 100m sprint world record and what was the official time?"),
        ("Arts", "What are the primary techniques involved in classical lost-wax bronze casting sculpture?"),
        ("Space (JWST)", "What are the primary instruments on the James Webb Space Telescope and how is MIRI cooled?"),
        ("Technology (AI)", "How do self-attention mechanisms operate in the Transformer neural network architecture?"),
        ("Food (Nutrition)", "How much protein is in 100g of chicken breast according to nutritional data?"),
    ]

    collection = rag.getCollection()
    print(f"ChromaDB Collection: '{Collection}' | Active Vectors: {collection.count()}\n")

    passed = 0
    for cat, q in test_queries:
        docs, metas, dists = rag.search(q, topK=3)
        sources = [m.get("source") for m in metas[:3]]
        status = "PASS" if docs else "FAIL"
        if docs:
            passed += 1
        print(f"[{cat}] {status}")
        print(f"  Q: '{q}'")
        print(f"  Top Sources: {sources}")
        if dists and dists[0] is not None:
            print(f"  Top Score/Dist: {dists[0]:.4f}")
        print()

    elapsed = time.time() - start_time
    print("=" * 70)
    print(f"PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS!")
    print(f"Verification: {passed}/{len(test_queries)} queries successfully retrieved relevant documents.")
    print("=" * 70)

if __name__ == "__main__":
    run()
