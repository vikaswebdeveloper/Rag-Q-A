import logging
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from backend.app.config import settings
from backend.app.loaders import Supported, extractText
from backend.app import rag

logger = logging.getLogger("rag.indexer")

# Ensure main.py can be imported
sys.path.insert(0, str(settings.resolve(Path(".."))))
try:
    from main import createChunk
except ImportError:
    # If project root is current dir or sibling
    from main import createChunk  # type: ignore

_executor = ThreadPoolExecutor(max_workers=1)
_lock = threading.Lock()
_statuses: dict[str, dict[str, Any]] = {}
_version: int = 0
_cached_chunk_counts: Optional[Counter] = None
_cached_version: int = -1


def statusSnapshot() -> dict[str, dict[str, Any]]:
    """Returns a copy of file indexing statuses."""
    with _lock:
        return {k: dict(v) for k, v in _statuses.items()}


def _bump_version():
    global _version
    with _lock:
        _version += 1


def chunkCounts() -> Counter:
    """Counter of chunks per source, read from Chroma metadata and cached until version changes."""
    global _cached_chunk_counts, _cached_version
    with _lock:
        current_v = _version
        if _cached_chunk_counts is not None and _cached_version == current_v:
            return Counter(_cached_chunk_counts)

    try:
        collection = rag.getCollection()
        all_meta = collection.get(include=["metadatas"]).get("metadatas", [])
        counts: Counter = Counter()
        for m in all_meta:
            src = m.get("source")
            if src:
                counts[src] += 1

        with _lock:
            _cached_chunk_counts = counts
            _cached_version = current_v
        return Counter(counts)
    except Exception as e:
        logger.error("Error reading chunk counts from Chroma: %s", e)
        return Counter()


def removeNow(name: str):
    """Delete the file's chunks immediately, refresh keyword index, and clear status."""
    try:
        collection = rag.getCollection()
        collection.delete(where={"source": name})
        logger.info("Deleted chunks for '%s'", name)
    except Exception as e:
        logger.error("Error deleting chunks for '%s': %s", name, e)

    with _lock:
        _statuses.pop(name, None)
    _bump_version()
    rag.refreshKeywordIndex()


def indexNow(path: Path):
    """Extract and chunk the file, delete old chunks and upsert new ones in batches of 200."""
    fname = path.name
    now_iso = datetime.now(timezone.utc).isoformat()

    with _lock:
        _statuses[fname] = {
            "state": "indexing",
            "detail": "",
            "chunks": 0,
            "at": now_iso,
        }
    _bump_version()

    try:
        if not path.exists():
            with _lock:
                _statuses.pop(fname, None)
            _bump_version()
            return

        category = fname.split("__", 1)[0].lower() if "__" in fname else "general"
        text = extractText(path)
        chunks = createChunk([(fname, category, text)])

        collection = rag.getCollection()

        # Check file still exists before deleting/writing
        if not path.exists():
            with _lock:
                _statuses.pop(fname, None)
            _bump_version()
            return

        # Delete old chunks
        try:
            collection.delete(where={"source": fname})
        except Exception:
            pass

        # Batch upsert 200
        batch_size = 200
        total_chunks = len(chunks)
        for i in range(0, total_chunks, batch_size):
            if not path.exists():
                # File deleted/renamed during indexing: clean up what was written
                try:
                    collection.delete(where={"source": fname})
                except Exception:
                    pass
                with _lock:
                    _statuses.pop(fname, None)
                _bump_version()
                return

            batch = chunks[i : i + batch_size]
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

        with _lock:
            _statuses[fname] = {
                "state": "ready",
                "detail": "",
                "chunks": total_chunks,
                "at": datetime.now(timezone.utc).isoformat(),
            }
        _bump_version()
        logger.info("Indexed '%s': %d chunks", fname, total_chunks)

    except Exception as e:
        logger.error("Failed to index '%s': %s", fname, e)
        with _lock:
            _statuses[fname] = {
                "state": "error",
                "detail": str(e),
                "chunks": 0,
                "at": datetime.now(timezone.utc).isoformat(),
            }
        _bump_version()


def queueIndex(path: Path):
    """Set status to queued, submit indexNow, followed by keyword index refresh."""
    fname = path.name
    with _lock:
        _statuses[fname] = {
            "state": "queued",
            "detail": "",
            "chunks": 0,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    _bump_version()

    def task():
        indexNow(path)
        rag.refreshKeywordIndex()

    _executor.submit(task)

