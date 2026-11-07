import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.app import rag
from main import Collection

test_queries = [
    ("Space (JWST)", "What are the primary instruments on the James Webb Space Telescope?"),
    ("Technology (Kubernetes)", "When was Kubernetes first released and who designed it?"),
    ("History (Apollo 11)", "When did Apollo 11 land on the Moon?"),
    ("Geography (Everest)", "What is the official summit elevation of Mount Everest?"),
    ("Food (Beer)", "What are the four traditional ingredients used in beer brewing?"),
    ("Health (Heart)", "How many chambers are there in the human heart?"),
    ("Science (DNA)", "Who discovered the molecular double helix structure of DNA in 1953?"),
    ("History (Vikings)", "What type of wooden vessel characterized Viking maritime mobility?"),
    ("Food (Nutrition)", "How much protein is in 100g of chicken breast?"),
    ("Science (Quantum)", "Who formulated the quantum Uncertainty Principle in 1927?"),
]

collection = rag.getCollection()
print(f"ChromaDB Collection '{Collection}': active vectors = {collection.count()}")
print()

passed = 0
for cat, q in test_queries:
    docs, metas, dists = rag.search(q, topK=3)
    sources = [m.get("source", "N/A") for m in metas[:3]]
    top_dist = f"{dists[0]:.4f}" if dists and dists[0] is not None else "N/A"
    status = "PASS" if docs else "WARN (no results)"
    if docs:
        passed += 1
    print(f"[{cat}] {status}")
    print(f"  Q: {q}")
    print(f"  Sources: {sources}")
    print(f"  Top dist: {top_dist}")
    print()

print(f"{'='*60}")
print(f"Verification: {passed}/{len(test_queries)} queries returned results.")
print(f"{'='*60}")

