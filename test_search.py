import sys
from pathlib import Path
import chromadb

ProjectRoot = Path(__file__).resolve().parent
DbPath = ProjectRoot / "chromaDB"
CollectionName = "myData"

def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "When was Kubernetes first released?"
    print(f"Connecting to ChromaDB at '{DbPath}'...")
    if not DbPath.exists():
        print("ChromaDB directory not found. Please run 'python main.py' first.")
        sys.exit(1)

    client = chromadb.PersistentClient(path=str(DbPath))
    collection = client.get_or_create_collection(name=CollectionName)
    count = collection.count()
    print(f"Collection '{CollectionName}' contains {count} chunks.")
    if count == 0:
        print("Collection is empty. Run 'python main.py' to index documents.")
        sys.exit(1)

    print(f"\nSearching for: \"{query}\" (Top 5)\n" + "-" * 60)
    results = collection.query(
        query_texts=[query],
        n_results=min(5, count),
        include=["documents", "metadatas", "distances"],
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists)):
        print(f"\n[{i + 1}] Source: {meta.get('source')} | Category: {meta.get('category')} | Distance: {dist:.4f}")
        print(f"    Section: {meta.get('section')}")
        snippet = doc.split("\n", 1)[-1].strip()[:200].replace("\n", " ")
        print(f"    Snippet: {snippet}...")

if __name__ == "__main__":
    main()

