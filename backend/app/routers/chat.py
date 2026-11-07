import json
import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.databases import getUserdataDb, UserdataSession
from backend.app.models import Conversation, Feedback, Message, User
from backend.app.security import getCurrentUser
from backend.app import rag

logger = logging.getLogger("rag.chat")

router = APIRouter(prefix="/api", tags=["chat"])

ReasonType = Literal["wrong", "not_in_documents", "incomplete", "bad_sources", "other"]


# Schemas
class ChatIn(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[uuid.UUID] = None


class SearchIn(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    top_k: Optional[int] = Field(default=None, ge=1, le=20)


class FeedbackIn(BaseModel):
    rating: Literal[1, -1]
    reason: Optional[ReasonType] = None
    comment: Optional[str] = Field(default=None, max_length=1000)


SUBJECT_WORDS = {
    "coffee", "caffeine", "tea", "bread", "chocolate", "potato", "olive", "oil",
    "viking", "vikings", "apollo", "moon", "roman", "rome", "egypt", "pyramid",
    "everest", "mountain", "amazon", "sahara", "desert", "trench", "mariana", "reef",
    "dna", "rna", "element", "elements", "earthquake", "earthquakes", "tectonics",
    "kubernetes", "internet", "microprocessor", "processor", "ai", "intelligence",
    "cloud", "computing", "sleep", "heart", "cardiovascular", "immune", "antibiotic",
    "alexandria", "library", "gutenberg", "printing", "solar", "energy", "silk", "road",
}

REFERENTIAL_WORDS = {
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "he", "him", "his", "she", "her", "hers",
    "this", "that", "these", "those",
    "there", "then", "also", "too", "else", "other",
}

CONTINUATION_PREFIXES = (
    "what about", "how about", "and what", "and how", "what else",
    "tell me more", "why so", "why then", "what then",
    "and who", "who then", "where then", "and why",
)


def isFollowUp(question: str) -> bool:
    """Detect if question is a conversational follow-up or a standalone topic."""
    q_clean = question.lower().strip()
    words = set(re.findall(r"\b[a-z0-9]+\b", q_clean))

    if words & REFERENTIAL_WORDS:
        return True
    if any(q_clean.startswith(prefix) for prefix in CONTINUATION_PREFIXES):
        return True
    if words & SUBJECT_WORDS:
        return False
    if len(words) <= 4:
        return True
    return False


def ownConversation(db: Session, conv_id: uuid.UUID, user: User) -> Conversation:
    """Load conversation only if owned by user, else 404."""
    conv = db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == user.id,
    ).first()
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conv


@router.post("/chat")
def post_chat(
    data: ChatIn,
    user: User = Depends(getCurrentUser),
    db: Session = Depends(getUserdataDb),
):
    question = data.message.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # 1. Get or create conversation
    if data.conversation_id:
        conversation = ownConversation(db, data.conversation_id, user)
    else:
        conversation = Conversation(
            user_id=user.id,
            title=question[:80],
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    conv_id = conversation.id

    # 2. Load last HISTORY_TURNS messages
    history_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .order_by(Message.created_at.desc())
        .limit(settings.HISTORY_TURNS)
        .all()
    )
    # Oldest first
    history_messages.reverse()

    # 3. Save the new user message & update conversation.updated_at
    now = datetime.now(timezone.utc)
    user_msg = Message(
        conversation_id=conv_id,
        user_id=user.id,
        role="user",
        content=question,
        created_at=now,
    )
    db.add(user_msg)
    conversation.updated_at = now
    db.commit()

    # 4. Search query = previous user question + "\n" + new question (only for genuine follow-ups)
    prev_user_q = ""
    for msg in reversed(history_messages):
        if msg.role == "user":
            prev_user_q = msg.content
            break

    if prev_user_q and isFollowUp(question):
        search_query = f"{prev_user_q}\n{question}".strip()
    else:
        search_query = question

    # 5. RAG search
    try:
        documents, metadatas, distances = rag.search(search_query)
        sources = rag.collectSources(metadatas, distances)
    except Exception as e:
        logger.error("RAG search error: %s", e)
        documents, metadatas, distances, sources = [], [], [], []

    history_dicts = [{"role": m.role, "content": m.content} for m in history_messages]
    rag_messages = rag.buildMessages(question, documents, history_dicts)

    # 6. Stream SSE response
    def sse_generator():
        # First event: meta
        meta_data = {
            "conversation_id": str(conv_id),
            "sources": sources,
        }
        yield f"event: meta\ndata: {json.dumps(meta_data)}\n\n"

        tokens_accumulated = []
        had_error = False

        try:
            for token in rag.streamAnswer(rag_messages):
                tokens_accumulated.append(token)
                yield f"event: token\ndata: {json.dumps({'text': token})}\n\n"
        except Exception as e:
            had_error = True
            logger.error("LLM streaming error: %s", e)
            err_msg = f"Model error: {e}. Is the LLM running?"
            yield f"event: error\ndata: {json.dumps({'message': err_msg})}\n\n"
            yield f"event: done\ndata: {{}}\n\n"
            return

        # 7. Save assistant message after stream finishes
        if not had_error:
            assistant_content = "".join(tokens_accumulated)
            saved_msg_id = None
            try:
                with UserdataSession() as save_db:
                    now_ast = datetime.now(timezone.utc)
                    assistant_msg = Message(
                        conversation_id=conv_id,
                        user_id=user.id,
                        role="assistant",
                        content=assistant_content,
                        sources=sources,
                        created_at=now_ast,
                    )
                    save_db.add(assistant_msg)
                    conv_row = save_db.query(Conversation).filter(Conversation.id == conv_id).first()
                    if conv_row:
                        conv_row.updated_at = now_ast
                    save_db.commit()
                    save_db.refresh(assistant_msg)
                    saved_msg_id = str(assistant_msg.id)
            except Exception as e:
                logger.error("Failed to save assistant message: %s", e)

            yield f"event: done\ndata: {json.dumps({'message_id': saved_msg_id or ''})}\n\n"

    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/search")
def post_search(
    data: SearchIn,
    _user: User = Depends(getCurrentUser),
):
    """Retrieval only endpoint used by evaluation."""
    documents, metadatas, distances = rag.search(data.query, topK=data.top_k)
    results = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        results.append({
            "text": doc,
            "source": meta.get("source", ""),
            "section": meta.get("section", ""),
            "category": meta.get("category", ""),
            "distance": round(dist, 4) if dist is not None else None,
        })
    return results


@router.get("/conversations")
def get_conversations(
    user: User = Depends(getCurrentUser),
    db: Session = Depends(getUserdataDb),
):
    convs = (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    return [
        {
            "id": c.id,
            "title": c.title,
            "updated_at": c.updated_at,
        }
        for c in convs
    ]


@router.get("/conversations/{conversation_id}")
def get_conversation_messages(
    conversation_id: uuid.UUID,
    user: User = Depends(getCurrentUser),
    db: Session = Depends(getUserdataDb),
):
    conv = ownConversation(db, conversation_id, user)
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.created_at.asc())
        .all()
    )

    out = []
    for m in messages:
        fb = db.query(Feedback).filter(Feedback.message_id == m.id).first()
        out.append({
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "sources": m.sources,
            "created_at": m.created_at,
            "rating": fb.rating if fb else None,
            "reason": fb.reason if fb else None,
        })
    return out


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: uuid.UUID,
    user: User = Depends(getCurrentUser),
    db: Session = Depends(getUserdataDb),
):
    conv = ownConversation(db, conversation_id, user)
    db.delete(conv)
    db.commit()
    return None


@router.post("/conversations/{conversation_id}/followups", response_model=list[str])
def get_followups(
    conversation_id: uuid.UUID,
    user: User = Depends(getCurrentUser),
    db: Session = Depends(getUserdataDb),
):
    conv = ownConversation(db, conversation_id, user)
    # Check last two messages
    last_two = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.created_at.desc())
        .limit(2)
        .all()
    )
    if len(last_two) < 2:
        return []

    assistant_msg = last_two[0]
    user_msg = last_two[1]
    if assistant_msg.role != "assistant" or user_msg.role != "user":
        return []

    q_text = user_msg.content
    a_text = assistant_msg.content
    sources = assistant_msg.sources or []

    # Close DB session before calling LLM
    db.close()

    try:
        return rag.suggestFollowups(q_text, a_text, sources, count=3)
    except Exception as e:
        logger.warning("Followups generation error: %s", e)
        return []


@router.put("/messages/{message_id}/feedback")
def put_feedback(
    message_id: uuid.UUID,
    data: FeedbackIn,
    user: User = Depends(getCurrentUser),
    db: Session = Depends(getUserdataDb),
):
    msg = (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.user_id == user.id,
            Message.role == "assistant",
        )
        .first()
    )
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    # Find the user question just before it
    prev_user_msg = (
        db.query(Message)
        .filter(
            Message.conversation_id == msg.conversation_id,
            Message.created_at < msg.created_at,
            Message.role == "user",
        )
        .order_by(Message.created_at.desc())
        .first()
    )
    question_text = prev_user_msg.content if prev_user_msg else ""

    fb = db.query(Feedback).filter(Feedback.message_id == msg.id).first()
    assigned_reason = data.reason if data.rating == -1 else None

    if fb:
        fb.rating = data.rating
        fb.reason = assigned_reason
        fb.comment = data.comment
        fb.status = "open"
        fb.question = question_text
        fb.answer = msg.content
        fb.sources = msg.sources
    else:
        fb = Feedback(
            message_id=msg.id,
            user_id=user.id,
            rating=data.rating,
            reason=assigned_reason,
            comment=data.comment,
            question=question_text,
            answer=msg.content,
            sources=msg.sources,
            status="open",
        )
        db.add(fb)

    db.commit()
    return {"rating": fb.rating, "reason": fb.reason}


@router.delete("/messages/{message_id}/feedback", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(
    message_id: uuid.UUID,
    user: User = Depends(getCurrentUser),
    db: Session = Depends(getUserdataDb),
):
    fb = (
        db.query(Feedback)
        .filter(Feedback.message_id == message_id, Feedback.user_id == user.id)
        .first()
    )
    if fb:
        db.delete(fb)
        db.commit()
    return None

