import logging
from collections.abc import Generator
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from pathlib import Path
from backend.app.config import settings

logger = logging.getLogger("rag.databases")

def _normalize_db_url(url: str) -> str:
    if url.startswith("sqlite:///") and not url.startswith("sqlite:////"):
        sub = url[len("sqlite:///"):]
        if not (len(sub) > 1 and sub[1] == ":") and not sub.startswith("/"):
            resolved = settings.resolve(Path(sub))
            return f"sqlite:///{resolved.as_posix()}"
    return url

usersEngine = create_engine(_normalize_db_url(settings.USERS_DB_URL), pool_pre_ping=True)
userdataEngine = create_engine(_normalize_db_url(settings.USERDATA_DB_URL), pool_pre_ping=True)

UsersSession = sessionmaker(bind=usersEngine, expire_on_commit=False)
UserdataSession = sessionmaker(bind=userdataEngine, expire_on_commit=False)

UsersBase = declarative_base()
UserdataBase = declarative_base()


def getUsersDb() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a users_db session."""
    with UsersSession() as session:
        yield session


def getUserdataDb() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a userdata_db session."""
    with UserdataSession() as session:
        yield session


def migrateUsers():
    """Inspect the users table and add missing columns if needed."""
    try:
        inspector = inspect(usersEngine)
        if not inspector.has_table("users"):
            return

        existing_cols = {c["name"] for c in inspector.get_columns("users")}
        is_sqlite = usersEngine.dialect.name == "sqlite"

        with usersEngine.begin() as conn:
            if "email_verified_at" not in existing_cols:
                logger.info("Migrating: adding email_verified_at to users table")
                conn.execute(text("ALTER TABLE users ADD COLUMN email_verified_at TIMESTAMPTZ"))
                conn.execute(text("UPDATE users SET email_verified_at = created_at"))

            if "password_changed_at" not in existing_cols:
                logger.info("Migrating: adding password_changed_at to users table")
                conn.execute(text("ALTER TABLE users ADD COLUMN password_changed_at TIMESTAMPTZ"))

            if "is_admin" not in existing_cols:
                logger.info("Migrating: adding is_admin to users table")
                if is_sqlite:
                    conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"))
                else:
                    conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT false"))

    except Exception as e:
        logger.error("Error migrating users table: %s", e)


def createTables():
    """Import models, create tables in both databases, and run migration."""
    # Import models so declarative bases register all tables
    import backend.app.models  # noqa: F401

    UsersBase.metadata.create_all(bind=usersEngine)
    UserdataBase.metadata.create_all(bind=userdataEngine)
    migrateUsers()

