import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI

_backend_dir = Path(__file__).resolve().parent.parent
_project_root = _backend_dir.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from backend.app.config import settings
from backend.app.databases import createTables
from backend.app.routers import admin, auth, chat, documents
from backend.app import rag

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("rag.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing RAG Q&A backend...")
    # Initialize databases
    try:
        createTables()
        logger.info("Databases initialized.")
    except Exception as e:
        logger.warning("Could not initialize databases (Postgres might be offline or starting): %s", e)

    # Initialize ChromaDB
    try:
        col = rag.getCollection()
        count = col.count()
        logger.info("ChromaDB initialized: %d chunks found.", count)
        if count == 0:
            logger.info("ChromaDB is empty. Launching background auto-indexer for data/ corpus...")
            import threading
            from main import loadDocs, createChunk, storeInChroma, DatabaseFolder, Collection, DataFolder
            def _auto_index():
                try:
                    docs = loadDocs(DataFolder)
                    chunks = createChunk(docs)
                    storeInChroma(chunks, db_path=DatabaseFolder, collection_name=Collection, reset=True)
                    rag.getKeywordIndex()
                    logger.info("Auto-indexing completed: %d chunks ready.", col.count())
                except Exception as ex:
                    logger.error("Auto-indexing error: %s", ex)
            threading.Thread(target=_auto_index, daemon=True).start()
    except Exception as e:
        logger.error("ChromaDB initialization failed: %s", e)

    # Pre-load re-ranker
    if settings.RERANK:
        try:
            rag.getReranker()
            logger.info("FastEmbed cross-encoder pre-loaded.")
        except Exception as e:
            logger.error("Failed to load cross-encoder: %s", e)

    # Pre-build keyword index
    if settings.HYBRID:
        try:
            rag.getKeywordIndex()
            logger.info("BM25 keyword index ready.")
        except Exception as e:
            logger.error("Failed to build keyword index: %s", e)

    yield
    logger.info("Shutting down RAG Q&A backend.")


app = FastAPI(title="RAG Q&A", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    try:
        col = rag.getCollection()
        count = col.count()
    except Exception:
        count = 0
    return {"status": "ok", "chunks": count}
