import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request, Response
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.databases import getUsersDb
from backend.app.models import AuthToken, User

passwordHash = PasswordHash.recommended()


def hashPassword(password: str) -> str:
    """Hash password using Argon2."""
    return passwordHash.hash(password)


def verifyPassword(password: str, hashed: str) -> bool:
    """Verify password against Argon2 hash."""
    return passwordHash.verify(password, hashed)


def setAuthCookie(response: Response, userId: uuid.UUID | str):
    """Create JWT and set as httpOnly cookie."""
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(userId),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
    )


def clearAuthCookie(response: Response):
    """Clear authentication cookie."""
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        path="/",
        httponly=True,
        samesite="lax",
    )


def getCurrentUser(
    request: Request,
    db: Session = Depends(getUsersDb),
) -> User:
    """Dependency: Read auth cookie, decode JWT, and validate user session."""
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not logged in")

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id_str = payload.get("sub")
        iat = payload.get("iat")
        if not user_id_str or iat is None:
            raise HTTPException(status_code=401, detail="Not logged in")
        user_id = uuid.UUID(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=401, detail="Not logged in")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not logged in")

    # If password changed after session was issued, invalidate session
    if user.password_changed_at:
        pwd_changed = user.password_changed_at
        if pwd_changed.tzinfo is None:
            pwd_changed = pwd_changed.replace(tzinfo=timezone.utc)
        pwd_changed_ts = int(pwd_changed.timestamp())
        if iat < pwd_changed_ts:
            raise HTTPException(status_code=401, detail="Not logged in")

    return user


def requireAdmin(user: User = Depends(getCurrentUser)) -> User:
    """Dependency: Restrict route to admin users."""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return user


def hashToken(token: str) -> str:
    """SHA-256 hex digest of a token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def issueToken(db: Session, user: User, purpose: str, lifetime: timedelta) -> str:
    """Mark earlier unused tokens of same purpose as used, issue new one, store hash."""
    now = datetime.now(timezone.utc)
    db.query(AuthToken).filter(
        AuthToken.user_id == user.id,
        AuthToken.purpose == purpose,
        AuthToken.used_at.is_(None),
    ).update({"used_at": now})

    raw_token = secrets.token_urlsafe(32)
    t_hash = hashToken(raw_token)
    expires_at = now + lifetime

    token_obj = AuthToken(
        user_id=user.id,
        purpose=purpose,
        token_hash=t_hash,
        expires_at=expires_at,
        created_at=now,
    )
    db.add(token_obj)
    db.commit()
    return raw_token


def recentlyIssued(db: Session, user: User, purpose: str, seconds: int = 60) -> bool:
    """True if a token of that purpose was created within the last N seconds."""
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=seconds)
    recent = db.query(AuthToken).filter(
        AuthToken.user_id == user.id,
        AuthToken.purpose == purpose,
        AuthToken.created_at >= cutoff,
    ).first()
    return recent is not None


def useToken(db: Session, token: str, purpose: str) -> User:
    """Find token by hash & purpose. If valid, mark used and return the associated user."""
    t_hash = hashToken(token)
    now = datetime.now(timezone.utc)

    token_obj = db.query(AuthToken).filter(
        AuthToken.token_hash == t_hash,
        AuthToken.purpose == purpose,
    ).first()

    if not token_obj or token_obj.used_at is not None:
        raise HTTPException(
            status_code=400,
            detail="This link is invalid or has expired. Please request a new one.",
        )

    expires_at = token_obj.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise HTTPException(
            status_code=400,
            detail="This link is invalid or has expired. Please request a new one.",
        )

    token_obj.used_at = now
    user = db.query(User).filter(User.id == token_obj.user_id).first()
    db.commit()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="This link is invalid or has expired. Please request a new one.",
        )

    return user
