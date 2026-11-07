import os
import re
import sys
from pathlib import Path
from typing import Any

# Ensure backend/app is importable
ProjectRoot = Path(__file__).resolve().parent
sys.path.insert(0, str(ProjectRoot))
sys.path.insert(0, str(ProjectRoot / "backend"))

from backend.app.loaders import Supported, extractText, titleFromName
from backend.app.embedding import get_embedding_function

# Constants
ChunkSize = 700
Overlap = 100
MinSize = 50
BatchSize = 500
Collection = "myData"
DatabaseFolder = ProjectRoot / "chromaDB"
DataFolder = ProjectRoot / "data"

SkipHeadings = {
    "see also",
    "references",
    "external links",
    "further reading",
    "notes",
    "bibliography",
    "sources",
}


def loadDocs(folder: str | Path) -> list[tuple[str, str, str]]:
    """For every supported file in sorted order, call extractText. Skip and print files that fail."""
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"Data folder '{folder_path}' does not exist.")
        return []

    docs = []
    files = sorted(folder_path.iterdir(), key=lambda p: p.name.lower())
    for f in files:
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext not in Supported:
            continue

        filename = f.name
        if "__" in filename:
            category = filename.split("__", 1)[0].lower()
        else:
            category = "general"

        try:
            text = extractText(f)
            docs.append((filename, category, text))
        except Exception as e:
            print(f"Skipping '{filename}': {e}")

    return docs


def getTitle(filename: str, text: str) -> tuple[str, str]:
    """If first line is non-empty, <100 chars, not ending in .!?, it is the title."""
    lines = text.split("\n")
    first_line = lines[0].strip() if lines else ""
    if first_line and len(first_line) < 100 and not first_line.endswith((".", "!", "?")):
        title = first_line
        body = "\n".join(lines[1:]).strip()
        return title, body
    return titleFromName(filename), text.strip()


def splitSections(body: str) -> list[tuple[list[str], str]]:
    """Walk lines and track a heading path. A heading with n '=' has level n-1."""
    sections: list[tuple[list[str], str]] = []
    current_path: list[str] = []
    current_lines: list[str] = []

    def flush():
        nonlocal current_lines
        if current_lines:
            text = "\n".join(current_lines).strip()
            if text:
                # Check top heading
                if not (current_path and current_path[0].lower().strip() in SkipHeadings):
                    sections.append((list(current_path), text))
            current_lines = []

    for line in body.split("\n"):
        m = re.match(r"^(=+)\s*(.+?)\s*\1$", line.strip())
        if m:
            flush()
            n = len(m.group(1))
            level = max(1, n - 1)
            heading_text = m.group(2).strip()
            current_path = current_path[: level - 1] + [heading_text]
        else:
            current_lines.append(line)

    flush()
    return sections


SEPARATORS = ["\n\n", "\n", "SENTENCE", " "]


def splitText(text: str, sep_idx: int = 0) -> list[str]:
    """Recursive splitter using paragraph, line, sentence, and word."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= ChunkSize:
        return [text]
    if sep_idx >= len(SEPARATORS):
        return [text[i : i + ChunkSize] for i in range(0, len(text), ChunkSize)]

    sep = SEPARATORS[sep_idx]
    if sep == "SENTENCE":
        parts = re.split(r"(?<=[.!?])\s+", text)
        joiner = " "
    else:
        parts = text.split(sep)
        joiner = sep

    pieces: list[str] = []
    current_acc: list[str] = []
    current_len = 0

    for part in parts:
        part_str = part.strip() if sep != " " else part
        if not part_str:
            continue
        if len(part_str) > ChunkSize:
            if current_acc:
                pieces.append(joiner.join(current_acc))
                current_acc = []
                current_len = 0
            sub_pieces = splitText(part_str, sep_idx + 1)
            pieces.extend(sub_pieces)
            continue

        needed_len = current_len + (len(joiner) if current_acc else 0) + len(part_str)
        if needed_len <= ChunkSize:
            current_acc.append(part_str)
            current_len = needed_len
        else:
            if current_acc:
                pieces.append(joiner.join(current_acc))
            current_acc = [part_str]
            current_len = len(part_str)

    if current_acc:
        pieces.append(joiner.join(current_acc))
    return pieces


def addOverlap(pieces: list[str]) -> list[str]:
    """Every piece after the first is prefixed with '...' + last 100 chars of prev piece (trimmed to word boundary)."""
    if not pieces:
        return []
    result = [pieces[0]]
    for i in range(1, len(pieces)):
        prev = pieces[i - 1]
        tail = prev[-Overlap:] if len(prev) >= Overlap else prev
        space_idx = tail.find(" ")
        if space_idx != -1 and space_idx < len(tail) - 1:
            trimmed = tail[space_idx + 1 :].strip()
        else:
            trimmed = tail.strip()

        if trimmed:
            result.append(f"...{trimmed} " + pieces[i])
        else:
            result.append(pieces[i])
    return result


def createChunk(docs: list[tuple[str, str, str]] | tuple[str, str, str]) -> list[dict[str, Any]]:
    """Importable chunking function. docs can be a list or a single tuple of (filename, category, text)."""
    if isinstance(docs, tuple):
        docs_list = [docs]
    else:
        docs_list = docs

    all_chunks: list[dict[str, Any]] = []

    for filename, category, text in docs_list:
        title, body = getTitle(filename, text)
        sections = splitSections(body)

        # If no sections were extracted, treat the whole body as one section
        if not sections and body:
            sections = [([], body)]

        chunk_idx = 0
        for path, section_text in sections:
            section_name = " > ".join([title] + path)
            pieces = splitText(section_text)
            overlapped = addOverlap(pieces)

            for piece in overlapped:
                if len(piece.strip()) < MinSize:
                    continue
                chunk_text = f"{section_name}\n{piece.strip()}"
                all_chunks.append({
                    "id": f"{filename}-{chunk_idx}",
                    "text": chunk_text,
                    "source": filename,
                    "category": category,
                    "section": section_name,
                })
                chunk_idx += 1

    return all_chunks


# Alias for backward compatibility
createChunks = createChunk


def storeInChroma(chunks: list[dict[str, Any]], db_path: Path = DatabaseFolder, collection_name: str = Collection, reset: bool = False):
    """Store chunks in ChromaDB with persistent client and batch upserts."""
    import chromadb

    client = chromadb.PersistentClient(path=str(db_path))
    ef = get_embedding_function()

    if reset:
        try:
            client.delete_collection(name=collection_name)
        except Exception:
            pass

    try:
        collection = client.get_or_create_collection(name=collection_name, embedding_function=ef)
    except Exception as e:
        if "Embedding function conflict" in str(e) or "already exists" in str(e):
            print(f"Embedding function updated. Recreating collection '{collection_name}' with new embeddings...")
            try:
                client.delete_collection(name=collection_name)
            except Exception:
                pass
            collection = client.create_collection(name=collection_name, embedding_function=ef)
        else:
            raise e

    # Delete existing chunks of every source being re-indexed
    sources_to_update = {c["source"] for c in chunks}
    for source in sources_to_update:
        try:
            collection.delete(where={"source": source})
        except Exception:
            pass

    total = len(chunks)
    print(f"Indexing {total} chunks into collection '{collection_name}' at '{db_path}'...")

    for i in range(0, total, BatchSize):
        batch = chunks[i : i + BatchSize]
        ids = [c["id"] for c in batch]
        documents = [c["text"] for c in batch]
        metadatas = [
            {
                "source": c["source"],
                "category": c["category"],
                "section": c["section"],
            }
            for c in batch
        ]
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        print(f"Stored {min(i + BatchSize, total)} / {total} chunks")

    print(f"Done. Total chunks in collection: {collection.count()}")


def main():
    print(f"Loading documents from: {DataFolder}")
    docs = loadDocs(DataFolder)
    print(f"Loaded {len(docs)} documents.")
    chunks = createChunk(docs)
    print(f"Created {len(chunks)} chunks.")
    if chunks:
        storeInChroma(chunks)
    else:
        print("No chunks to store.")


if __name__ == "__main__":
    main()

