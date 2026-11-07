import sys
from pathlib import Path

ProjectRoot = Path(__file__).resolve().parent
sys.path.insert(0, str(ProjectRoot))
sys.path.insert(0, str(ProjectRoot / "backend"))

from backend.app.config import settings
from backend.app import rag

def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "When was Kubernetes first released?"
    print(f"--- RAG Pipeline Test ---")
    print(f"Query: \"{query}\"")
    print(f"Settings: Hybrid={settings.HYBRID}, Rerank={settings.RERANK}, Model={settings.LLM_MODEL} ({settings.LLM_PROVIDER})")

    print("\n1. Initializing BM25 Keyword index...")
    rag.getKeywordIndex()

    print("\n2. Executing Search & Re-ranking...")
    documents, metadatas, distances = rag.search(query)
    sources = rag.collectSources(metadatas, distances)

    print(f"Retrieved {len(documents)} passages across {len(sources)} unique document sources:")
    for i, s in enumerate(sources):
        dist_str = f"{s['distance']:.4f}" if s['distance'] is not None else "N/A"
        print(f"  [{i + 1}] Source: {s['slug']} ({s['category']}) | Distance: {dist_str}")
        print(f"      Section: {s['section']}")

    print("\n3. Building Messages...")
    messages = rag.buildMessages(query, documents, history=[])

    print("\n4. Streaming Answer from LLM:")
    print("-" * 50)
    full_answer = []
    try:
        for token in rag.streamAnswer(messages):
            print(token, end="", flush=True)
            full_answer.append(token)
        print("\n" + "-" * 50)
        answer_text = "".join(full_answer)

        print("\n5. Generating Suggested Follow-up Questions...")
        try:
            followups = rag.suggestFollowups(query, answer_text, sources)
            print(f"Follow-ups ({len(followups)}):")
            for f in followups:
                print(f"  • {f}")
        except Exception as e:
            print(f"Could not generate follow-ups: {e}")

    except Exception as e:
        print(f"\n[LLM Connection Notice]: {e}")
        print(f"Note: To enable live generation, ensure {settings.LLM_PROVIDER} is running or set LLM_PROVIDER=openai with an API key in backend/.env.")

if __name__ == "__main__":
    main()

