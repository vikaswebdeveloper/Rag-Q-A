import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.databases import getUsersDb, getUserdataDb
from backend.app.mailer import sendPasswordReset, sendVerification
from backend.app.models import Conversation, Feedback, Message, User
from backend.app.security import (
    clearAuthCookie,
    getCurrentUser,
    hashPassword,
    issueToken,
    recentlyIssued,
    setAuthCookie,
    useToken,
    verifyPassword,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# Pydantic Schemas
class RegisterIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class EmailIn(BaseModel):
    email: EmailStr


class TokenIn(BaseModel):
    token: str = Field(..., min_length=10, max_length=200)


class ResetIn(BaseModel):
    token: str = Field(..., min_length=10, max_length=200)
    password: str = Field(..., min_length=8, max_length=128)


class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True


class RegisterOut(BaseModel):
    verification_required: bool
    user: Optional[UserOut] = None


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterOut)
def register(
    data: RegisterIn,
    response: Response,
    background_tasks: BackgroundTasks,
    db: Session = Depends(getUsersDb),
):
    email = data.email.lower().strip()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    pwd_hash = hashPassword(data.password)
    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=pwd_hash,
    )

    if settings.REQUIRE_EMAIL_VERIFICATION:
        db.add(user)
        db.commit()
        db.refresh(user)
        lifetime = timedelta(hours=settings.VERIFY_TOKEN_HOURS)
        token = issueToken(db, user, "verify", lifetime)
        background_tasks.add_task(sendVerification, user, token)
        return RegisterOut(verification_required=True, user=None)
    else:
        user.email_verified_at = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        db.refresh(user)
        setAuthCookie(response, user.id)
        return RegisterOut(verification_required=False, user=UserOut.model_validate(user))


@router.post("/login", response_model=UserOut)
def login(
    data: LoginIn,
    response: Response,
    db: Session = Depends(getUsersDb),
):
    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verifyPassword(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if settings.REQUIRE_EMAIL_VERIFICATION and user.email_verified_at is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email first. Check your inbox for the link.",
        )

    setAuthCookie(response, user.id)
    return UserOut.model_validate(user)


@router.post("/verify-email", response_model=UserOut)
def verify_email(
    data: TokenIn,
    response: Response,
    db: Session = Depends(getUsersDb),
):
    user = useToken(db, data.token.strip(), "verify")
    if user.email_verified_at is None:
        user.email_verified_at = datetime.now(timezone.utc)
        db.commit()

    setAuthCookie(response, user.id)
    return UserOut.model_validate(user)


@router.post("/resend-verification")
def resend_verification(
    data: EmailIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(getUsersDb),
):
    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if user and user.email_verified_at is None:
        if not recentlyIssued(db, user, "verify", seconds=60):
            lifetime = timedelta(hours=settings.VERIFY_TOKEN_HOURS)
            token = issueToken(db, user, "verify", lifetime)
            background_tasks.add_task(sendVerification, user, token)

    return {"message": "If an account exists for that email, we've sent it a link."}


@router.post("/forgot-password")
def forgot_password(
    data: EmailIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(getUsersDb),
):
    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if user:
        if not recentlyIssued(db, user, "reset", seconds=60):
            lifetime = timedelta(minutes=settings.RESET_TOKEN_MINUTES)
            token = issueToken(db, user, "reset", lifetime)
            background_tasks.add_task(sendPasswordReset, user, token)

    return {"message": "If an account exists for that email, we've sent it a link."}


@router.post("/reset-password", response_model=UserOut)
def reset_password(
    data: ResetIn,
    response: Response,
    db: Session = Depends(getUsersDb),
):
    user = useToken(db, data.token.strip(), "reset")
    now = datetime.now(timezone.utc)
    user.password_hash = hashPassword(data.password)
    user.password_changed_at = now
    if user.email_verified_at is None:
        user.email_verified_at = now
    db.commit()

    setAuthCookie(response, user.id)
    return UserOut.model_validate(user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    clearAuthCookie(response)
    return None


@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(getCurrentUser)):
    return UserOut.model_validate(user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    response: Response,
    user: User = Depends(getCurrentUser),
    users_db: Session = Depends(getUsersDb),
    userdata_db: Session = Depends(getUserdataDb),
):
    # Delete userdata
    userdata_db.query(Feedback).filter(Feedback.user_id == user.id).delete()
    userdata_db.query(Message).filter(Message.user_id == user.id).delete()
    userdata_db.query(Conversation).filter(Conversation.user_id == user.id).delete()
    userdata_db.commit()

    # Delete user
    users_db.delete(user)
    users_db.commit()

    clearAuthCookie(response)
    return None

