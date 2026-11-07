# RAG Q&A — Private "Chat With Your Documents" Library

A full-stack, login-protected digital library and question-answering website built with **FastAPI**, **Next.js 15 (App Router)**, **PostgreSQL**, **ChromaDB**, and **hybrid BM25 + Cross-Encoder RAG**.

Users can browse, search, and read documents in a classic editorial "library desk" aesthetic, or converse with an AI Librarian that streams verifiable answers grounded strictly in the library's catalog, citing the exact document section and page.

---

## Architecture Overview

```
Browser ──► Next.js (port 3000) ──/api/* rewrite──► FastAPI (port 8000) ──► PostgreSQL (users_db, userdata_db)
                                                         │
                                                         ├──► ChromaDB (dense vector search, all-MiniLM-L6-v2)
                                                         ├──► BM25 (sparse lexical search, in-memory)
                                                         ├──► Cross-Encoder (Xenova/ms-marco-MiniLM-L-6-v2)
                                                         └──► LLM (local Ollama or OpenAI-compatible endpoint)
```

- **Dual-Database Isolation**: User authentication & credentials live in `users_db`; conversations, messages, and ratings live in `userdata_db` referencing users solely by UUID without cross-database foreign keys.
- **Hybrid Retrieval & RRF**: Combines dense vector retrieval (ChromaDB) and sparse keyword retrieval (`bm25s`), fused via Reciprocal Rank Fusion ($k=60$), deduped by word overlap, and re-ranked with a local cross-encoder (`fastembed`).
- **Pluggable LLM**: Out-of-the-box support for local inference via Ollama (`qwen2.5:1.5b`) or any cloud OpenAI-compatible provider.
- **Editorial Design System**: Custom paper & lamplit night themes, zero-flash hydration theme script, drop caps, SVG book cloth covers, interactive reading progress, and slide-in librarian assistant with SSE streaming.

---

## System Requirements

- **Python**: 3.12+ (Python 3.12 or 3.13 recommended)
- **Node.js**: 20.9+ (v22 LTS recommended) & npm 10+
- **PostgreSQL**: 14+ (dual databases: `users_db` and `userdata_db`)
- **LLM**: Local [Ollama](https://ollama.com/) with model `qwen2.5:1.5b` (or an OpenAI-compatible API key)
- **RAM**: ~8 GB recommended for local embedding + cross-encoder re-ranking
- **Optional**: LibreOffice (`soffice`) for legacy `.doc`/`.ppt`/`.xls` conversion

---

## One-Time Setup

### 1. Python Virtual Environment & Dependencies

From the project root:

```bash
# Create and activate virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Environment Configuration

Copy the sample environment file to `backend/.env`:

```bash
cp backend/.env.example backend/.env
```

Generate a secure 256-bit JWT secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Edit `backend/.env` with your database credentials and generated secret:
```env
USERS_DB_URL=postgresql+psycopg://rag_app:your_password@localhost:5432/users_db
USERDATA_DB_URL=postgresql+psycopg://rag_app:your_password@localhost:5432/userdata_db
JWT_SECRET=your_generated_secret_string
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:1.5b
```

### 3. PostgreSQL Database Setup

Run the initialization script using `psql` (adjust user as needed):

```bash
# On Linux/macOS:
sudo -u postgres psql -f backend/setup_db.sql

# On Windows (Command Prompt / PowerShell):
psql -U postgres -f backend/setup_db.sql
```

*(Replace `<DB_PASSWORD>` inside `backend/setup_db.sql` or create the databases and role manually).*

### 4. Language Model Setup

**Option A — Local Ollama (Default):**
```bash
ollama serve
ollama pull qwen2.5:1.5b
```

**Option B — OpenAI or Compatible API:**
In `backend/.env`:
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.openai.com/v1
```

### 5. Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 6. Index Library Documents

Populate the ChromaDB vector database and test retrieval:

```bash
# Windows
.\.venv\Scripts\python.exe main.py

# Linux/macOS
python main.py
```

This parses documents from `data/`, chunks them into 700-character segments with 100-character overlap, and stores them in `chromaDB/`.

---

## Running the Application

Run the services in three terminal tabs:

### Terminal 1 — Ollama (if using local LLM)
```bash
ollama serve
```

### Terminal 2 — Backend FastAPI
```bash
cd backend
# Linux/macOS:
../.venv/bin/uvicorn app.main:app --port 8000 --reload

# Windows:
..\.venv\Scripts\uvicorn.exe app.main:app --port 8000 --reload
```

FastAPI docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Terminal 3 — Frontend Next.js
```bash
cd frontend
npm run dev
```

Open **[http://localhost:3000](http://localhost:3000)** in your browser.

---

## Email & Verification Flow

- **Development Fallback (Default)**: When `SMTP_HOST` is left empty in `.env`, the system automatically captures all verification and password reset emails to the `backend/outbox/` directory as `.eml` files. Open them in any text editor or email client to retrieve verification and password-reset links.
- **Production SMTP (e.g. Gmail)**:
  ```env
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=your_email@gmail.com
  SMTP_PASSWORD=your_16_character_app_password
  SMTP_FROM="RAG Q&A Library <your_email@gmail.com>"
  SMTP_STARTTLS=true
  ```

---

## Admin Accounts & User Management

To grant admin privileges to an account, use the `make_admin.py` CLI:

```bash
# Grant admin rights
python backend/make_admin.py your_email@example.com

# Revoke admin rights
python backend/make_admin.py your_email@example.com --remove

# List all current admins
python backend/make_admin.py --list
```

Admins gain access to the `/admin` portal containing system telemetry, 14-day question histograms, user audit tables, feedback triage, and the live document manager.

---

## API Reference

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register new account (sends verification email) | No |
| `POST` | `/api/auth/login` | Authenticate user & set httpOnly session cookie | No |
| `GET`  | `/api/auth/verify-email` | Verify email with token | No |
| `POST` | `/api/auth/resend-verification` | Request a new email verification token | No |
| `POST` | `/api/auth/forgot-password` | Request password reset token | No |
| `POST` | `/api/auth/reset-password` | Reset password using one-time token | No |
| `POST` | `/api/auth/logout` | Clear session cookie & invalidate session | Yes |
| `GET`  | `/api/auth/me` | Fetch active user profile and admin status | Yes |
| `GET`  | `/api/documents` | List documents with category/search filters | Yes |
| `GET`  | `/api/documents/{slug}` | Read document text, sections, and extracted tables | Yes |
| `GET`  | `/api/documents/{slug}/download` | Download raw original document file | Yes |
| `POST` | `/api/chat` | SSE streamed Q&A answer with sources | Yes |
| `POST` | `/api/search` | Search documents (BM25 + Vector + Re-ranking) | Yes |
| `GET`  | `/api/conversations` | List user's conversation threads | Yes |
| `GET`  | `/api/conversations/{id}` | Get conversation messages and sources | Yes |
| `DELETE`| `/api/conversations/{id}` | Delete conversation thread | Yes |
| `GET`  | `/api/conversations/{id}/followups` | Suggest follow-up questions | Yes |
| `POST` | `/api/messages/{id}/feedback` | Rate answer (👍/👎 with reason & triage comment) | Yes |
| `GET`  | `/api/admin/stats` | System telemetry, counts & breakdown metrics | Admin |
| `GET`  | `/api/admin/users` | User list with question counts (private) | Admin |
| `GET`  | `/api/admin/feedback` | Feedback triage queue with source links | Admin |
| `PATCH`| `/api/admin/feedback/{id}` | Update triage status or admin notes | Admin |
| `GET`  | `/api/admin/documents` | Live document catalog with index status | Admin |
| `POST` | `/api/admin/documents` | Upload new document (streaming, max 25MB) | Admin |
| `PUT`  | `/api/admin/documents/{slug}` | Atomic text edit (.txt, .md, .csv) | Admin |
| `POST` | `/api/admin/documents/{slug}/rename` | Rename document and category | Admin |
| `POST` | `/api/admin/documents/{slug}/replace`| Replace file with updated version | Admin |
| `DELETE`| `/api/admin/documents/{slug}` | Soft delete document to `backend/trash/` | Admin |
| `GET`  | `/api/health` | Health check endpoint | No |

---

## Tuning & Configuration Parameters

Edit these variables in `backend/.env` to adjust retrieval behavior:

| Variable | Default | Purpose |
|---|---|---|
| `TOP_K` | `5` | Number of final re-ranked context passages fed to the LLM |
| `HYBRID` | `true` | Combine dense ChromaDB vector search with sparse BM25s |
| `RERANK` | `true` | Apply Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) re-ranking |
| `CANDIDATES` | `30` | Candidate passages retrieved from ChromaDB before re-ranking |
| `KEYWORD_CANDIDATES` | `30` | Candidate passages retrieved from BM25 before re-ranking |
| `HISTORY_TURNS` | `6` | Prior conversation turns sent to LLM for conversational context |
| `RERANK_MODEL` | `Xenova/ms-marco-MiniLM-L-6-v2` | FastEmbed cross-encoder model |

---

## Production Deployment Notes

1. **HTTPS & Secure Cookies**: Set `COOKIE_SECURE=true` in `backend/.env` so authentication cookies carry the `Secure` flag.
2. **Reverse Proxy**: Place Next.js and FastAPI behind Nginx, Caddy, or Cloudflare with TLS termination and gzip/brotli compression. Next.js handles `/api/*` rewrites directly, ensuring a unified origin and avoiding cross-site cookie restrictions.
3. **Rate Limiting**: Protect `/api/auth/*` (e.g., 5 requests/minute for login and password resets) and `/api/chat` (e.g., 20 requests/minute per IP) using Nginx `limit_req` or Redis rate limiters.
4. **Secrets Management**: Generate fresh, random strings for `JWT_SECRET` and database passwords. Never check `backend/.env` into source control.

