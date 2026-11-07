import os
import re
import shutil
import uuid
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.databases import getUsersDb, getUserdataDb
from backend.app.indexer import chunkCounts, queueIndex, removeNow, statusSnapshot
from backend.app.loaders import Supported, extractText, slugFor
from backend.app.models import Conversation, Feedback, Message, User
from backend.app.routers.documents import library, pathFor
from backend.app.security import requireAdmin
from backend.app import rag

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(requireAdmin)])

Editable = {".txt", ".md", ".csv"}
MaxUploadBytes = 25 * 1024 * 1024  # 25 MB


def get_trash_dir() -> Path:
    trash_dir = settings.resolve(Path("trash"))
    trash_dir.mkdir(parents=True, exist_ok=True)
    return trash_dir


def cleanPart(value: str, label: str) -> str:
    cleaned = value.lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    cleaned = cleaned[:80]
    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid {label}: must contain alphanumeric characters.",
        )
    return cleaned


def fileName(category: str, name: str, suffix: str) -> str:
    return f"{cleanPart(category, 'category')}__{cleanPart(name, 'name')}{suffix}"


# Schemas
class FeedbackPatchIn(BaseModel):
    status: Optional[Literal["open", "resolved"]] = None
    admin_note: Optional[str] = Field(default=None, max_length=2000)


class DocumentContentIn(BaseModel):
    text: str = Field(..., max_length=5_000_000)


class DocumentRenameIn(BaseModel):
    category: str
    name: str


@router.get("/stats")
def get_stats(
    users_db: Session = Depends(getUsersDb),
    userdata_db: Session = Depends(getUserdataDb),
):
    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)

    # Users stats
    total_users = users_db.query(User).count()
    verified_users = users_db.query(User).filter(User.email_verified_at.isnot(None)).count()
    admin_users = users_db.query(User).filter(User.is_admin.is_(True)).count()
    new_users_7d = users_db.query(User).filter(User.created_at >= seven_days_ago).count()

    # Questions (user role messages)
    total_questions = userdata_db.query(Message).filter(Message.role == "user").count()
    
    # Local server date for today and per_day calculation
    now_local = datetime.now()
    today_start = datetime.combine(now_local.date(), datetime.min.time())
    questions_today = (
        userdata_db.query(Message)
        .filter(Message.role == "user", Message.created_at >= today_start)
        .count()
    )
    questions_7d = (
        userdata_db.query(Message)
        .filter(Message.role == "user", Message.created_at >= seven_days_ago)
        .count()
    )

    # 14 days per_day breakdown
    per_day = []
    for day_offset in range(13, -1, -1):
        d = (now_local - timedelta(days=day_offset)).date()
        d_start = datetime.combine(d, datetime.min.time())
        d_end = datetime.combine(d, datetime.max.time())
        c = (
            userdata_db.query(Message)
            .filter(
                Message.role == "user",
                Message.created_at >= d_start,
                Message.created_at <= d_end,
            )
            .count()
        )
        per_day.append({"date": d.isoformat(), "count": c})

    # Conversations
    total_convs = userdata_db.query(Conversation).count()

    # Documents stats
    docs_summary, _, _ = library()
    total_docs = len(docs_summary)
    by_format = Counter(d["format"] for d in docs_summary)
    by_category = Counter(d["category"] for d in docs_summary)

    # Sort most common first
    by_format_sorted = dict(sorted(by_format.items(), key=lambda x: x[1], reverse=True))
    by_category_sorted = dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True))

    # Chroma chunks count
    try:
        chunks_count = rag.getCollection().count()
    except Exception:
        chunks_count = 0

    # Feedback stats
    helpful_fb = userdata_db.query(Feedback).filter(Feedback.rating == 1).count()
    not_helpful_fb = userdata_db.query(Feedback).filter(Feedback.rating == -1).count()
    open_fb = userdata_db.query(Feedback).filter(Feedback.rating == -1, Feedback.status == "open").count()

    return {
        "users": {
            "total": total_users,
            "verified": verified_users,
            "admins": admin_users,
            "new_7d": new_users_7d,
        },
        "questions": {
            "total": total_questions,
            "today": questions_today,
            "last_7d": questions_7d,
            "per_day": per_day,
        },
        "conversations": total_convs,
        "documents": {
            "total": total_docs,
            "by_format": by_format_sorted,
            "by_category": by_category_sorted,
        },
        "chunks": chunks_count,
        "feedback": {
            "helpful": helpful_fb,
            "not_helpful": not_helpful_fb,
            "open": open_fb,
        },
    }


@router.get("/users")
def get_users(
    users_db: Session = Depends(getUsersDb),
    userdata_db: Session = Depends(getUserdataDb),
):
    users = users_db.query(User).order_by(User.created_at.desc()).all()
    user_rows = []

    for u in users:
        conv_count = userdata_db.query(Conversation).filter(Conversation.user_id == u.id).count()
        q_count = (
            userdata_db.query(Message)
            .filter(Message.user_id == u.id, Message.role == "user")
            .count()
        )
        last_msg = (
            userdata_db.query(Message)
            .filter(Message.user_id == u.id)
            .order_by(Message.created_at.desc())
            .first()
        )
        last_active = last_msg.created_at.isoformat() if last_msg else None

        user_rows.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "is_admin": u.is_admin,
            "verified": u.email_verified_at is not None,
            "joined": u.created_at.isoformat(),
            "conversations": conv_count,
            "questions": q_count,
            "last_active": last_active,
        })

    return user_rows


@router.get("/feedback")
def get_feedback(
    rating: Literal["all", "helpful", "not_helpful"] = "not_helpful",
    state: Literal["all", "open", "resolved"] = "open",
    users_db: Session = Depends(getUsersDb),
    userdata_db: Session = Depends(getUserdataDb),
):
    query = userdata_db.query(Feedback)

    if rating == "helpful":
        query = query.filter(Feedback.rating == 1)
    elif rating == "not_helpful":
        query = query.filter(Feedback.rating == -1)

    if state == "open":
        query = query.filter(Feedback.status == "open")
    elif state == "resolved":
        query = query.filter(Feedback.status == "resolved")

    items = query.order_by(Feedback.updated_at.desc()).limit(200).all()

    # Pre-fetch user infos
    user_ids = {fb.user_id for fb in items}
    users_map = {}
    if user_ids:
        found_users = users_db.query(User).filter(User.id.in_(user_ids)).all()
        for u in found_users:
            users_map[u.id] = {"name": u.name, "email": u.email}

    result = []
    for fb in items:
        u_info = users_map.get(fb.user_id)
        result.append({
            "id": fb.id,
            "rating": fb.rating,
            "reason": fb.reason,
            "comment": fb.comment,
            "question": fb.question,
            "answer": fb.answer,
            "sources": fb.sources,
            "status": fb.status,
            "admin_note": fb.admin_note,
            "user": u_info,
            "created_at": fb.created_at.isoformat(),
            "updated_at": fb.updated_at.isoformat(),
        })

    return result


@router.patch("/feedback/{feedback_id}")
def patch_feedback(
    feedback_id: uuid.UUID,
    data: FeedbackPatchIn,
    userdata_db: Session = Depends(getUserdataDb),
):
    fb = userdata_db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if data.status is not None:
        fb.status = data.status
    if data.admin_note is not None:
        note = data.admin_note.strip()
        fb.admin_note = note if note else None

    userdata_db.commit()
    userdata_db.refresh(fb)

    return {
        "id": fb.id,
        "rating": fb.rating,
        "reason": fb.reason,
        "comment": fb.comment,
        "question": fb.question,
        "answer": fb.answer,
        "sources": fb.sources,
        "status": fb.status,
        "admin_note": fb.admin_note,
        "created_at": fb.created_at.isoformat(),
        "updated_at": fb.updated_at.isoformat(),
    }


@router.get("/documents")
def get_admin_documents():
    docs_summary, paths, _ = library()
    counts = chunkCounts()
    statuses = statusSnapshot()

    result = []
    for d in docs_summary:
        slug = d["slug"]
        path = paths[slug]
        fname = path.name

        size = path.stat().st_size if path.exists() else 0
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat() if path.exists() else None
        chunks = counts.get(fname, 0)
        editable = path.suffix.lower() in Editable

        status_info = statuses.get(fname)
        if status_info:
            index_state = status_info.get("state", "not indexed")
            index_detail = status_info.get("detail", "")
        elif chunks > 0:
            index_state = "ready"
            index_detail = ""
        else:
            index_state = "not indexed"
            index_detail = ""

        result.append({
            **d,
            "file": fname,
            "size": size,
            "modified": mtime,
            "chunks": chunks,
            "editable": editable,
            "index_state": index_state,
            "index_detail": index_detail,
        })

    return result


@router.get("/index-status")
def get_index_status():
    return statusSnapshot()


@router.post("/documents", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    name: Optional[str] = Form(None),
    replace: bool = Form(False),
):
    orig_name = file.filename or "uploaded_file"
    suffix = Path(orig_name).suffix.lower()

    if suffix not in Supported:
        allowed = ", ".join(sorted(Supported))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported file format '{suffix}'. Allowed: {allowed}",
        )

    base_name = name.strip() if name and name.strip() else Path(orig_name).stem
    target_filename = fileName(category, base_name, suffix)
    data_dir = settings.resolve(settings.DATA_DIR)
    data_dir.mkdir(parents=True, exist_ok=True)
    target_path = data_dir / target_filename

    if target_path.exists() and not replace:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Document '{target_filename}' already exists.",
        )

    temp_path = data_dir / f".upload-{target_filename}"
    bytes_read = 0

    try:
        with open(temp_path, "wb") as f_out:
            while True:
                chunk = await file.read(1024 * 1024)  # 1 MB chunk
                if not chunk:
                    break
                bytes_read += len(chunk)
                if bytes_read > MaxUploadBytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File exceeds maximum allowed upload size of 25 MB",
                    )
                f_out.write(chunk)

        # Atomic replace
        temp_path.replace(target_path)
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)

    # Queue indexing
    queueIndex(target_path)

    return {
        "file": target_filename,
        "slug": slugFor(target_filename),
    }


@router.get("/documents/{slug}/content")
def get_document_content(slug: str):
    path = pathFor(slug)
    if path.suffix.lower() not in Editable:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only plain text, markdown, and CSV files can be edited in the browser.",
        )

    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "file": path.name,
        "text": text,
    }


@router.put("/documents/{slug}/content")
def put_document_content(slug: str, data: DocumentContentIn):
    path = pathFor(slug)
    if path.suffix.lower() not in Editable:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only plain text, markdown, and CSV files can be edited in the browser.",
        )

    temp_path = path.parent / f".edit-{path.name}"
    try:
        temp_path.write_text(data.text, encoding="utf-8")
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)

    queueIndex(path)

    return {
        "file": path.name,
        "slug": slugFor(path.name),
    }


@router.patch("/documents/{slug}")
def rename_document(slug: str, data: DocumentRenameIn):
    old_path = pathFor(slug)
    old_fname = old_path.name
    suffix = old_path.suffix.lower()

    new_fname = fileName(data.category, data.name, suffix)
    new_path = old_path.parent / new_fname

    if new_path.exists() and new_path != old_path:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Target document '{new_fname}' already exists.",
        )

    old_path.rename(new_path)
    removeNow(old_fname)
    queueIndex(new_path)

    return {
        "file": new_fname,
        "slug": slugFor(new_fname),
    }


@router.delete("/documents/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(slug: str):
    path = pathFor(slug)
    fname = path.name

    trash_dir = get_trash_dir()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    trash_target = trash_dir / f"{timestamp}-{fname}"

    shutil.move(str(path), str(trash_target))
    removeNow(fname)

    return None

