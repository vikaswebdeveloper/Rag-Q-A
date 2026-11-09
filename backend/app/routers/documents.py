import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.app.config import settings
from backend.app.loaders import (
    Supported,
    TableFormats,
    extractText,
    readTables,
    slugFor,
    titleFromName,
)
from backend.app.security import getCurrentUser

router = APIRouter(prefix="/api/documents", tags=["documents"])


# Schemas
class TableOut(BaseModel):
    name: str
    columns: list[str]
    rows: list[list[Any]]
    totalRows: int


class DocSummary(BaseModel):
    slug: str
    title: str
    category: str
    format: str
    preview: str
    words: int


class DocDetail(BaseModel):
    slug: str
    title: str
    category: str
    format: str
    text: str
    tables: Optional[list[TableOut]] = None


def _get_files_state(data_dir: Path) -> tuple[tuple[str, float], ...]:
    """Helper to produce a hashable state of files in data_dir for lru_cache."""
    if not data_dir.exists():
        return ()
    files = []
    for f in sorted(data_dir.iterdir(), key=lambda p: p.name.lower()):
        if f.is_file() and f.suffix.lower() in Supported:
            files.append((f.name, f.stat().st_mtime))
    return tuple(files)


@lru_cache(maxsize=8)
def _build_library(files_state: tuple[tuple[str, float], ...]) -> tuple[list[dict[str, Any]], dict[str, Path], dict[str, str]]:
    data_dir = settings.resolve(settings.DATA_DIR)
    manifest_path = Path(__file__).resolve().parent.parent / "data_manifest.json"

    # Fast path: load pre-indexed catalog in 1ms without parsing 254 files sequentially
    cached_docs = None
    if manifest_path.exists():
        try:
            import json
            with open(manifest_path, "r", encoding="utf-8") as f:
                cached_docs = json.load(f)
        except Exception:
            cached_docs = None

    paths: dict[str, Path] = {}
    aliases: dict[str, str] = {}

    if data_dir.exists():
        for f in data_dir.iterdir():
            if f.is_file() and f.suffix.lower() in Supported:
                s = slugFor(f.name)
                paths[s] = f
                aliases[f.stem] = s

    if cached_docs:
        return cached_docs, paths, aliases

    docs = []

    for fname, _ in files_state:
        fpath = data_dir / fname
        ext = fpath.suffix.lstrip(".").lower()
        slug = slugFor(fname)
        stem = fpath.stem

        paths[slug] = fpath
        aliases[stem] = slug

        if "__" in fname:
            category = fname.split("__", 1)[0].lower()
        else:
            category = "general"

        try:
            full_text = extractText(fpath)
        except Exception:
            full_text = ""

        # Extract title and body
        lines = full_text.split("\n")
        first_line = lines[0].strip() if lines else ""
        if first_line and len(first_line) < 100 and not first_line.endswith((".", "!", "?")):
            title = first_line
            body = "\n".join(lines[1:]).strip()
        else:
            title = titleFromName(fpath)
            body = full_text.strip()

        words = len(re.findall(r"\b\w+\b", body))

        # Build preview
        is_table = fpath.suffix.lower() in TableFormats
        if is_table:
            tables = readTables(fpath)
            if tables:
                t = tables[0]
                cols_snippet = ", ".join(t["columns"][:4])
                if len(t["columns"]) > 4:
                    cols_snippet += ", …"
                preview = f"{t['totalRows']} rows × {len(t['columns'])} columns ({cols_snippet})"
            else:
                preview = "Spreadsheet table"
        else:
            # Strip heading lines
            clean_lines = []
            for line in body.split("\n"):
                if not re.match(r"^(=+)\s*(.+?)\s*\1$", line.strip()):
                    clean_lines.append(line)
            clean_text = re.sub(r"\s+", " ", " ".join(clean_lines)).strip()
            preview = clean_text[:200]

        docs.append({
            "slug": slug,
            "title": title,
            "category": category,
            "format": ext,
            "preview": preview,
            "words": words,
        })

    return docs, paths, aliases


def library() -> tuple[list[dict[str, Any]], dict[str, Path], dict[str, str]]:
    data_dir = settings.resolve(settings.DATA_DIR)
    state = _get_files_state(data_dir)
    return _build_library(state)


def pathFor(slug: str) -> Path:
    _, paths, aliases = library()
    target = paths.get(slug) or paths.get(aliases.get(slug, ""))
    if not target or not target.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return target


@router.get("", response_model=list[DocSummary])
def get_documents(_user=Depends(getCurrentUser)):
    docs, _, _ = library()
    return docs


@router.get("/{slug}", response_model=DocDetail)
def get_document(slug: str, _user=Depends(getCurrentUser)):
    path = pathFor(slug)
    fname = path.name
    ext = path.suffix.lstrip(".").lower()
    doc_slug = slugFor(fname)

    if "__" in fname:
        category = fname.split("__", 1)[0].lower()
    else:
        category = "general"

    text = extractText(path)
    lines = text.split("\n")
    first_line = lines[0].strip() if lines else ""
    if first_line and len(first_line) < 100 and not first_line.endswith((".", "!", "?")):
        title = first_line
    else:
        title = titleFromName(path)

    tables_data = readTables(path)
    tables = [TableOut(**t) for t in tables_data] if tables_data else None

    return DocDetail(
        slug=doc_slug,
        title=title,
        category=category,
        format=ext,
        text=text,
        tables=tables,
    )


@router.get("/{slug}/file")
def get_document_file(slug: str, _user=Depends(getCurrentUser)):
    path = pathFor(slug)
    return FileResponse(
        path=path,
        filename=path.name,
        media_type="application/octet-stream",
    )

