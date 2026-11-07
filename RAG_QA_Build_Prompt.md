# BUILD PROMPT — "RAG Q&A": a private "chat with your documents" website (complete specification)

> Copy everything in this file into the AI that will build the project.

---

## 0. INSTRUCTIONS FOR THE AI THAT READS THIS

You are a senior full-stack engineer. Build the complete project described in this document **from scratch**, exactly as specified. The document has three main parts:

- **PART A — Overview** (what the product is, folder layout, how the pieces talk to each other)
- **PART B — Backend** (Python / FastAPI / PostgreSQL / ChromaDB / RAG pipeline)
- **PART C — Frontend** (Next.js / React / TypeScript / Tailwind CSS, including the full design system, colours, fonts and animations)
- **PART D — Evaluation, README and build order**

Rules:

1. Follow the names, file paths, endpoints, field names, numbers and colours **exactly** as written. They depend on each other.
2. Build in the phases listed in **PART D, section D3**. After each phase, stop. Tell me what you built, the exact commands to run it, and how to test it. Then wait for me to say "continue".
3. Write complete, working code. **No TODOs, no placeholder functions, no "implement this yourself".**
4. Keep comments short. Only explain *why* something is done when it is not obvious.
5. **Never hard-code secrets.** Every key, password, URL and model name comes from environment variables. I will supply my own values. Where this document writes `<PLACEHOLDER>`, leave it as a placeholder in `.env.example`.
6. If anything in this document is unclear or contradicts itself, **ask me before guessing**.

---

# PART A — OVERVIEW

## A1. What the product is

A **login-protected website** for a library of documents (about 250 files on topics such as history, science, food, health, geography and technology).

- Users **browse and read** every document in a beautiful, classic, "old library" style reader.
- Users **ask a chatbot** questions. It answers **only from the documents** using **RAG (Retrieval-Augmented Generation)**:
  1. it searches the documents for the most relevant passages,
  2. it gives those passages to an LLM,
  3. the LLM writes the answer from them, streaming it word by word,
  4. the answer shows **clickable source links** to the exact document sections.
- If the documents do not contain the answer, the bot **says so instead of guessing**.
- Users can **rate answers** (👍 / 👎 with a reason). Admins review the 👎 ones and fix the documents.
- Each user's chat history is **private**. Admins only see *counts*. The single exception: when a user rates an answer, that one question + answer is shared with the admins (the UI tells the user this).
- An **admin panel** shows statistics and lets admins upload, edit, rename, replace and delete documents. Changes are re-indexed automatically in the background.
- **Day / night theme** toggle, responsive layout (phones to large screens), accessible.

## A2. Tech stack

| Layer | Technology |
|---|---|
| Backend language | Python 3.12 |
| Web framework | FastAPI + Uvicorn |
| ORM / settings | SQLAlchemy 2.x, pydantic-settings, pydantic (with `EmailStr`, needs `email-validator`) |
| Databases | PostgreSQL 14+ — **two separate databases**: `users_db` and `userdata_db` |
| Vector store | ChromaDB (persistent client on disk), default embedding model **all-MiniLM-L6-v2** (384 dimensions; Chroma downloads it on first use) |
| Keyword search | `bm25s` (in-memory BM25 index) |
| Re-ranker | `fastembed` `TextCrossEncoder` with model **`Xenova/ms-marco-MiniLM-L-6-v2`** |
| LLM | Pluggable (see B6). Default: a **local model through Ollama** (`qwen2.5:1.5b`). Optional: any **OpenAI-compatible API** with my own key. |
| Password hashing | `pwdlib[argon2]` (Argon2) |
| Sessions | JWT (`pyjwt`, HS256) stored in an **httpOnly cookie** |
| File parsing | `pypdf`, `python-docx`, `python-pptx`, `openpyxl`, Python `csv`; optional LibreOffice (`soffice`) for old formats |
| Uploads | `python-multipart` |
| HTTP client (eval) | `httpx` |
| Frontend | **Next.js (App Router, v15/16) + React 19 + TypeScript + Tailwind CSS v4**, `react-markdown` |

Backend `requirements.txt` (pin current stable versions):
```
fastapi
uvicorn[standard]
sqlalchemy
psycopg[binary]
pyjwt
pwdlib[argon2]
pydantic-settings
email-validator
chromadb
ollama
openai            # only used when LLM_PROVIDER=openai
pypdf
python-pptx
python-docx
openpyxl
python-multipart
fastembed
bm25s
httpx
```

Frontend `package.json` dependencies: `next`, `react`, `react-dom`, `react-markdown`. Dev dependencies: `typescript`, `@types/node`, `@types/react`, `@types/react-dom`, `tailwindcss` (v4), `@tailwindcss/postcss`, `eslint`, `eslint-config-next`.

## A3. Folder layout

```
<project root>/
├── data/                         # the documents (input). Named  <category>__<name>.<ext>
│                                  #   e.g. history__apollo_11.txt, science__dna.md, food__potato.docx
├── chromaDB/                     # ChromaDB persistent storage (generated)
├── main.py                       # one-off script: read data/, chunk, store in ChromaDB
├── README.md
├── backend/
│   ├── .env.example  .gitignore  requirements.txt  setup_db.sql  make_admin.py
│   ├── outbox/                   # emails saved here when SMTP is not configured (generated, git-ignored)
│   ├── trash/                    # deleted documents are moved here (generated, git-ignored)
│   └── app/
│       ├── __init__.py  config.py  databases.py  models.py  security.py  mailer.py
│       ├── loaders.py  lexical.py  llm.py  rag.py  indexer.py  main.py
│       └── routers/ __init__.py  auth.py  documents.py  chat.py  admin.py
├── frontend/
│   ├── package.json  next.config.ts  postcss.config.mjs  tsconfig.json  proxy.ts (or middleware.ts)
│   ├── public/art/paper.svg
│   ├── public/images/  hero-shelves.webp  library-aisle.webp  food.webp  general.webp  geography.webp
│   │                   health.webp  history.webp  science.webp  technology.webp  CREDITS.md
│   ├── app/  layout.tsx  globals.css
│   │   ├── (auth)/ login/page.tsx  register/page.tsx  forgot-password/page.tsx  verify-email/page.tsx  reset-password/page.tsx
│   │   └── (site)/ layout.tsx  page.tsx  documents/[slug]/page.tsx  admin/page.tsx
│   ├── components/  Header.tsx  SiteFooter.tsx  BackToTop.tsx  ThemeToggle.tsx  UserProvider.tsx  icons.tsx
│   │                AuthShell.tsx  AuthForm.tsx  ResendVerification.tsx  ChatWidget.tsx  DocArt.tsx  DataTable.tsx
│   │                admin/ StatTile.tsx  QuestionsChart.tsx  UsersTable.tsx  FeedbackList.tsx  DocumentsManager.tsx
│   └── lib/  api.ts  theme.ts  docArt.ts
└── eval/  testset.json  run_eval.py  REPORT.md  results/
```

**File naming rule for documents:** the text before the first `__` is the **category** (`history__apollo_11.txt` → category `history`, name `apollo_11`). A file with no `__` belongs to category **`general`**.

## A4. How the pieces connect

```
Browser ──► Next.js (port 3000) ──/api/* rewrite──► FastAPI (port 8000) ──► PostgreSQL users_db / userdata_db
                                                         │
                                                         ├──► ChromaDB (vector search)  + BM25 (keyword search, in memory)
                                                         ├──► Cross-encoder re-ranker (local)
                                                         └──► LLM (Ollama locally, or an OpenAI-compatible API)
```

- The frontend calls **relative** URLs `/api/...`. Next.js rewrites them to the backend, so the browser sees one origin and the auth cookie works **without CORS**.
- The chat answer is streamed with **Server-Sent Events** over a `POST` request.

---

# PART B — BACKEND

## B1. Configuration — `backend/app/config.py`

Use `pydantic_settings.BaseSettings`, reading `backend/.env` (resolve the path relative to the `backend/` folder, so it works from any working directory). Define `BackendDir = Path(__file__).resolve().parent.parent`.

| Setting (env var) | Type | Default | Meaning |
|---|---|---|---|
| `USERS_DB_URL` | str | **required** | SQLAlchemy URL of `users_db`, e.g. `postgresql+psycopg://<DB_USER>:<DB_PASSWORD>@localhost:5432/users_db` |
| `USERDATA_DB_URL` | str | **required** | SQLAlchemy URL of `userdata_db` |
| `JWT_SECRET` | str | **required** | Long random string |
| `JWT_EXPIRE_MINUTES` | int | 1440 | Session length (24 h) |
| `COOKIE_SECURE` | bool | false | `true` in production over HTTPS |
| `COOKIE_NAME` | str | `access_token` | Name of the auth cookie |
| `CHROMA_PATH` | Path | `../chromaDB` | Relative paths resolve from `backend/` |
| `CHROMA_COLLECTION` | str | `myData` | Collection name |
| `DATA_DIR` | Path | `../data` | Documents folder |
| `LLM_PROVIDER` | str | `ollama` | `ollama` or `openai` (any OpenAI-compatible API) |
| `LLM_MODEL` | str | `qwen2.5:1.5b` | Model name for the chosen provider |
| `LLM_BASE_URL` | str | `""` | For `openai` provider: base URL of the compatible API. For Ollama: optional host (default `http://localhost:11434`) |
| `LLM_API_KEY` | str | `""` | My API key, only for the `openai` provider |
| `TOP_K` | int | 5 | Passages given to the LLM |
| `RERANK` | bool | true | Use the cross-encoder |
| `RERANK_MODEL` | str | `Xenova/ms-marco-MiniLM-L-6-v2` | |
| `CANDIDATES` | int | 30 | Vector-search candidates before re-ranking |
| `HYBRID` | bool | true | Also run BM25 keyword search and fuse |
| `KEYWORD_CANDIDATES` | int | 30 | BM25 candidates |
| `HISTORY_TURNS` | int | 6 | Previous messages sent to the LLM |
| `APP_URL` | str | `http://localhost:3000` | Used in email links |
| `REQUIRE_EMAIL_VERIFICATION` | bool | true | Block login until the email is verified |
| `VERIFY_TOKEN_HOURS` | int | 24 | |
| `RESET_TOKEN_MINUTES` | int | 60 | |
| `SMTP_HOST` | str | `""` | Empty = save emails to `backend/outbox/` instead of sending |
| `SMTP_PORT` | int | 587 | |
| `SMTP_USER`, `SMTP_PASSWORD` | str | `""` | |
| `SMTP_FROM` | str | `RAG Q&A <no-reply@localhost>` | |
| `SMTP_STARTTLS` | bool | true | |

Add a method `resolve(path)` that returns the path unchanged if absolute, otherwise `(BackendDir / path).resolve()`. Export a single `settings = Settings()`.

Create `backend/.env.example` listing **every** variable above, with placeholders such as `<DB_USER>`, `<DB_PASSWORD>`, `<GENERATE_A_LONG_RANDOM_STRING>`, `<YOUR_LLM_API_KEY>`, `<YOUR_SMTP_PASSWORD>`. Add a comment showing how to generate a JWT secret: `python -c "import secrets; print(secrets.token_urlsafe(48))"`.

`backend/.gitignore`: `.env`, `__pycache__/`, `outbox/`, `trash/`.

`backend/setup_db.sql` (with a placeholder password):
```sql
-- Run once:  sudo -u postgres psql -f backend/setup_db.sql
CREATE ROLE rag_app LOGIN PASSWORD '<DB_PASSWORD>';
CREATE DATABASE users_db OWNER rag_app;
CREATE DATABASE userdata_db OWNER rag_app;
```

## B2. Databases — `backend/app/databases.py`

- Two engines (`pool_pre_ping=True`): `usersEngine` from `USERS_DB_URL`, `userdataEngine` from `USERDATA_DB_URL`.
- Two session factories (`expire_on_commit=False`): `UsersSession`, `UserdataSession`.
- Two declarative bases: `UsersBase`, `UserdataBase` (so each set of tables is created in its own database).
- FastAPI dependencies `getUsersDb()` and `getUserdataDb()` that `yield` a session inside a `with` block.
- `createTables()`: import the models, `create_all` on both bases, then `migrateUsers()`. That function inspects the `users` table and, if they are missing, adds `email_verified_at TIMESTAMPTZ` (setting it to `created_at` for existing rows), `password_changed_at TIMESTAMPTZ` and `is_admin BOOLEAN NOT NULL DEFAULT false`, because `create_all` never adds columns to an existing table.

**Why two databases:** accounts and private chat data are isolated, so a leak of one does not expose the other. The `userdata_db` tables store `user_id` as a plain UUID column, with no cross-database foreign key.

## B3. Data models — `backend/app/models.py`

All timestamps are timezone-aware (`DateTime(timezone=True)`), with default `datetime.now(timezone.utc)`. All ids are `uuid4`.

**users_db**

`users`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| email | String(320) | unique, indexed, stored **lowercase** |
| name | String(100) | |
| password_hash | String(255) | Argon2 hash |
| created_at | timestamptz | |
| email_verified_at | timestamptz, nullable | null = not verified |
| password_changed_at | timestamptz, nullable | sessions issued before this are invalid |
| is_admin | Boolean | default false, `server_default="false"` |

`auth_tokens` (one-time links for email verification and password reset; **only a SHA-256 hash of the token is stored**)
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | FK → users.id, `ondelete=CASCADE`, indexed | |
| purpose | String(16) | `"verify"` or `"reset"` |
| token_hash | String(64) | unique, indexed (hex SHA-256) |
| expires_at | timestamptz | |
| used_at | timestamptz, nullable | |
| created_at | timestamptz | |

**userdata_db**

`conversations`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID | indexed (no FK — other database) |
| title | String(200) | first 80 characters of the first question |
| created_at, updated_at | timestamptz | `updated_at` has `onupdate=now` |
| messages | relationship | `cascade="all, delete-orphan"`, ordered by `Message.created_at` |

`messages`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| conversation_id | FK → conversations.id, `ondelete=CASCADE`, indexed | |
| user_id | UUID | composite index `(user_id, created_at)` named `ix_messages_user_created` |
| role | String(16) | `"user"` or `"assistant"` |
| content | Text | |
| sources | JSON, nullable | list of source objects (see B7) |
| created_at | timestamptz | |

`feedback` (one row per rated answer; keeps **copies** of the question, answer and sources so admins never need to read the conversation)
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| message_id | FK → messages.id, `ondelete=CASCADE`, **unique** | the rated assistant message |
| user_id | UUID, indexed | |
| rating | int | `1` helpful, `-1` not helpful |
| reason | String(32), nullable | `wrong`, `not_in_documents`, `incomplete`, `bad_sources`, `other` (only for -1) |
| comment | Text, nullable | max 1000 characters |
| question | Text | copy |
| answer | Text | copy |
| sources | JSON, nullable | copy |
| status | String(16) | `"open"` (default) or `"resolved"` |
| admin_note | Text, nullable | |
| created_at, updated_at | timestamptz | |

## B4. Security — `backend/app/security.py`

- `passwordHash = PasswordHash.recommended()` from `pwdlib` (Argon2). Functions: `hashPassword(password)` and `verifyPassword(password, hashed)`.
- **`setAuthCookie(response, userId)`:** create a JWT `{"sub": str(userId), "iat": now, "exp": now + JWT_EXPIRE_MINUTES}` signed with `JWT_SECRET`, HS256. Set it as a cookie named `COOKIE_NAME` with `httponly=True`, `secure=COOKIE_SECURE`, `samesite="lax"`, `max_age=JWT_EXPIRE_MINUTES*60` and `path="/"`.
- `clearAuthCookie(response)`: delete the cookie (`path="/"`).
- **`getCurrentUser`** (dependency): read the cookie, decode the JWT, load the user. Raise **401 "Not logged in"** if the cookie is missing, invalid or expired, or the user no longer exists. **Also raise 401 if `password_changed_at` is set and the token's `iat` is earlier than it**, because a password reset signs out every other session.
- **`requireAdmin`** (dependency): `getCurrentUser`, then **403 "Admins only"** if `is_admin` is false.
- `hashToken(token)`: `sha256(token).hexdigest()`.
- **`issueToken(db, user, purpose, lifetime)`:** mark every earlier unused token of the same user and purpose as used (`used_at = now`), so only the newest link works. Create `secrets.token_urlsafe(32)`, store only its hash, commit, and return the raw token.
- `recentlyIssued(db, user, purpose, seconds=60)`: true if a token of that purpose was created in the last 60 seconds. Use it to throttle emails.
- **`useToken(db, token, purpose)`:** find the token by hash and purpose. If it is unknown, already used or expired, raise **400 "This link is invalid or has expired. Please request a new one."**. Otherwise set `used_at = now` and return the user.

## B5. Email — `backend/app/mailer.py`

- `sendEmail(to, subject, text, html)`: build an `EmailMessage` with a plain-text body and an HTML alternative.
  - If `SMTP_HOST` is **empty**: create `backend/outbox/`, write the message as `<YYYYmmdd-HHMMSS-micro>-<to>.eml` and log the plain text (including the link) to the console. This makes local development work with no email account.
  - Otherwise send through `smtplib.SMTP(host, port, timeout=20)`, with `starttls()` if enabled and `login()` if a user is set. Log errors; never crash the request.
- `layout(title, intro, button, link, footer)` returns `(text, html)`. The HTML is a centred 480px card containing the title, intro, a big link button, the raw link (as a fallback) and a small footer.
- `sendVerification(user, token)`: link `{APP_URL}/verify-email?token={token}`, subject "Verify your email for RAG Q&A", footer "This link expires in 24 hours…".
- `sendPasswordReset(user, token)`: link `{APP_URL}/reset-password?token={token}`, subject "Reset your RAG Q&A password", footer "This link expires in 60 minutes and works once…".
- Send emails with FastAPI `BackgroundTasks`, so requests return immediately.

## B6. LLM abstraction — `backend/app/llm.py`

One small module, so the rest of the code never depends on a specific provider.

```python
def chatStream(messages: list[dict]) -> Iterator[str]   # yields text tokens
def chatJson(messages: list[dict], schema: dict, temperature=0.3, maxTokens=200) -> str  # returns JSON text
```

- **`LLM_PROVIDER=ollama`:** use the `ollama` Python client (`ollama.Client(host=LLM_BASE_URL)` if a base URL is set, otherwise the default host).
  - Streaming: `client.chat(model=LLM_MODEL, messages=messages, stream=True)`, yielding `chunk["message"]["content"]` whenever it is non-empty.
  - JSON: `client.chat(..., format=schema, options={"temperature": t, "num_predict": maxTokens})`.
- **`LLM_PROVIDER=openai`:** use `openai.OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL or None)`.
  - Streaming: `chat.completions.create(model=LLM_MODEL, messages=messages, stream=True)`, yielding `delta.content`.
  - JSON: `response_format={"type": "json_object"}`, with the schema described in the system prompt.
- Never log the API key.

## B7. Document loading — `backend/app/loaders.py`

**Goal:** turn every supported file into **one plain-text string**. The **first line is the document title**, followed by a blank line, and sections are marked with MediaWiki-style headings: `== Heading ==` (level 2), `=== Sub ===` (level 3), `==== Sub-sub ====` (level 4). Both the chunker and the document reader use this format.

Constants:
```python
Converted = {".ppt": ".pptx", ".odp": ".pptx", ".doc": ".docx", ".odt": ".docx", ".rtf": ".docx", ".xls": ".xlsx", ".ods": ".xlsx"}
Supported = {".txt", ".md", ".csv", ".pdf", ".pptx", ".docx", ".xlsx", *Converted}
RowsPerSection = 50
GenericTitles = {"powerpoint presentation", "presentation", "document", "untitled", "slide 1", "title"}
TableFormats = {".csv", ".xlsx", ".xls", ".ods"}
MaxTableRows = 500
```

Helpers:
- **`slugFor(filename)`:** a `.txt` file's slug is its stem (`history__apollo_11`). Any other format's slug is `<stem>-<ext>` (`history__apollo_11-pptx`). The slug is the URL id of a document.
- `titleFromName(path)`: the part after `__`, with `_` replaced by spaces, in Title Case.
- `withTitle(title, sections)`: `title + "\n\n" + "\n\n".join(non-empty sections)`.
- `realTitle(t)`: returns `""` if `t` is empty or in `GenericTitles`.
- `clean(text)`: normalise `\r\n` to `\n`, remove NUL characters, collapse runs of spaces and tabs.
- **`formatRow(header, row)`:** `"Col A: value; Col B: value"`, skipping empty values and `"None"`. An empty header becomes `Column N`.
- **`rowSections(header, rows, level="==")`:** groups rows into sections of 50, headed `== Rows 1–50 ==`, with one formatted row per paragraph. **Column names are repeated on every row so each chunk makes sense on its own.**

Readers:
- **`.txt`:** read as UTF-8 (`errors="replace"`) and normalise newlines.
- **`.md`:** a `#` heading that comes before any text is the title. Then `#` and `##` become `==`, `###` becomes `===`, and deeper headings become `====`.
- **`.csv`:** decode as `utf-8-sig`, falling back to `latin-1`. Detect the delimiter with `csv.Sniffer` (among `,;\t|`), drop empty rows, and use the first row as the header. Output a `== Columns ==` section listing the column names and "N rows.", followed by `rowSections`.
- **`.pdf`:** use `pypdf`. Take the title from the PDF metadata if it is real and 3–99 characters long, otherwise from the file name. For each page, write `== Page N ==`, re-join hyphenated line breaks (`-\n` followed by a word character) and turn single newlines into spaces, since PDF line breaks are layout, not paragraphs.
- **`.pptx`:** use `python-pptx`. Each slide becomes `== Slide N: <slide title> ==`, followed by the text of every shape (recurse into groups; table rows are joined with ` | `) and `Speaker notes: …`. The title comes from the core properties, then the first slide title, then the file name.
- **`.docx`:** use `python-docx`. Walk the body in order. A paragraph with style "Title" becomes the title. "Heading N" becomes a heading of `min(N+1, 5)` `=` signs. Other paragraphs become text. Tables become `formatRow` lines.
- **`.xlsx`:** use `openpyxl` (`read_only`, `data_only`). For each sheet, write `== Sheet: <name> ==` with "Columns: …. N rows.", then `rowSections(level="===")`. Integer floats such as `8849.0` print as `8849`.
- **Old formats:** convert with LibreOffice into a temporary directory (`soffice --headless --convert-to <ext> --outdir <tmp> <file>`, 180-second timeout), then read the converted file.
- **`extractText(path)`:** the public entry point, cached with `lru_cache(maxsize=512)` keyed on `(absolute path, modification time)`, so edited files are re-read.
- **`readTables(path)`:** for spreadsheet formats only, returns `[{name, columns, rows (first 500), totalRows}]`. Rows are padded to the same width and empty headers become `Column N`. Cached the same way (`maxsize=64`). For other formats it returns `None`.

## B8. Chunking and indexing — `main.py` (project root)

Constants: `ChunkSize = 700` characters, `Overlap = 100`, `MinSize = 50`, `BatchSize = 500`, `Collection = "myData"`, database folder `chromaDB`, data folder `data`.

1. **`loadDocs(folder)`:** for every supported file in sorted order, call `extractText`. Skip and print files that fail. Return `(filename, category, text)` for each.
2. **`getTitle(filename, text)`:** if the first line is non-empty, shorter than 100 characters and does not end in `.!?`, it is the title and the rest is the body. Otherwise the title comes from the file name.
3. **`splitSections(body)`:** walk the lines and track a **heading path**. A heading with `n` equals signs has level `n-1`, and the path becomes `path[:level-1] + [heading]`. Return `(path, sectionText)` for every non-empty section.
4. **Skip sections** whose top heading is (case-insensitive) one of: `see also`, `references`, `external links`, `further reading`, `notes`, `bibliography`, `sources`.
5. **`splitText(text, separators)`** is a recursive splitter. The separators, in order, are: paragraph (`\n\n`), line (`\n`), sentence (`(?<=[.!?])\s+`, re-joined with a space) and word (` `).
   - If the text is ≤ 700 characters, return it as is.
   - Otherwise split it on the current separator and greedily pack the parts into pieces of ≤ 700 characters.
   - Recurse into any part longer than 700 with the next separator. With no separators left, cut into hard 700-character slices.
6. **`addOverlap(pieces)`:** every piece after the first is prefixed with `"..." + last 100 characters of the previous piece` (trimmed to start at a word boundary) followed by a space.
7. Drop pieces shorter than 50 characters.
8. **Chunk format:** `text = f"{section}\n{piece}"`, where `section = " > ".join([title] + path)`, e.g. `Apollo 11 > Mission > Landing`. Each chunk is `{"id": f"{filename}-{i}", "text", "source": filename, "category", "section"}`.
9. **`storeInChroma(chunks)`:** open a `chromadb.PersistentClient`, `get_or_create_collection`, delete the existing chunks of every source being re-indexed (`where={"source": filename}`), then `upsert` in batches of 500 with metadata `{source, category, section}`. Print progress.
10. Make `createChunk(docs)` importable, so the backend's indexer can reuse **exactly the same chunking**. Run the script with `python main.py` from the project root.

## B9. Keyword search — `backend/app/lexical.py`

- An in-memory **BM25** index (`bm25s`) built from **all documents in the Chroma collection** (`collection.get(include=["documents"])`). It keeps a parallel list of chunk ids.
- Tokenizer: `bm25s.tokenization.Tokenizer(stopwords=..., splitter=r"[^\W_]+")`. The stopwords are bm25s's English list **plus** question words: `what who whom whose how when where which why does did do can could would should tell explain describe me about many much`.
- Thread safety: a `lock` around the current index and a `buildLock` so only one build runs at a time.
- `ensure(getCollection)`: build the index on first use (called at startup).
- **`scheduleRebuild(getCollection)`:** rebuild in the background on a single-thread executor. Several quick changes share one rebuild, using a "pending" `threading.Event`. Log failures.
- `search(question, n)`: tokenize the question (`update_vocab=False`). If no tokens remain, return `[]`. Otherwise retrieve the top `n` and return the chunk ids **with a score above 0**, best first.

## B10. Retrieval and answering — `backend/app/rag.py`

**System prompt** (exact text):
```
You are an AI assistant answering questions using a RAG pipeline.
Use the retrieved context to give an accurate answer to the user's question.
If the context doesn't contain enough information, say what is missing instead of guessing.
```

Functions:

1. `getCollection()` (cached with `lru_cache`): a `chromadb.PersistentClient` at `CHROMA_PATH`, then `get_collection(CHROMA_COLLECTION)`.
2. `getReranker()` (cached): `fastembed.rerank.cross_encoder.TextCrossEncoder(model_name=RERANK_MODEL)`.
3. **`fuse(rankings, k=60)`:** Reciprocal Rank Fusion. Every id scores `1/(k + rank)` in each list it appears in (rank starts at 1). Return ids sorted by total score, highest first.
4. **`candidates(question)`:**
   - Run a vector query: `collection.query(query_texts=[question], n_results=CANDIDATES)`. If re-ranking is off, use `TOP_K` instead. This gives `(id → (text, metadata, distance))`.
   - If `HYBRID` is on, also run `lexical.search(question, KEYWORD_CANDIDATES)`. Fetch any keyword ids missing from the vector results with `collection.get(ids=…)` (their distance is `None`).
   - Return `fuse([vectorIds, keywordIds])`, cut to the candidate count, as `(text, metadata, distance)` tuples.
5. **`dropCopies(passages, overlap=0.8)`:** the same article often exists in several formats (`food__beer.txt` and `food__beer.md`). Two passages count as copies when they come from the **same article stem** and their word sets (ignoring the first, section line) share **≥ 80% of the smaller set**. Keep only the first of each.
6. **`search(question, topK=None)`:** `dropCopies(candidates(question))`. Then, if `RERANK` is on and there is more than one passage, score them with `getReranker().rerank(question, texts)` and sort by score, highest first. Keep the top `TOP_K` and return `(documents, metadatas, distances)`.
7. **`collectSources(metadatas, distances)`:** one entry per document, in rank order: `{"slug": slugFor(meta["source"]), "section": meta["section"], "category": meta["category"], "distance": round(d, 4) or None}`.
8. **`buildMessages(question, documents, history)`:** `[system prompt] + history (role, content) + one user message`. That user message is:
   ```
   Retrieved Context:
   <documents joined with "\n---\n">

   User Query:
   <question>
   ```
9. `streamAnswer(messages)`: yields tokens from `llm.chatStream`.
10. **`suggestFollowups(question, answer, sources, count=3)`:** call `llm.chatJson` with the schema `{"type":"object","properties":{"questions":{"type":"array","items":{"type":"string"}}},"required":["questions"]}`, temperature 0.3 and 200 max tokens. The system prompt is:
    ```
    Suggest {count} short follow-up questions the user might ask next, based on the conversation below.
    Each question must be under 15 words, stand on its own (no "it" or "this" without saying what),
    not repeat the question already asked, and be answerable from the same documents.
    Reply with JSON only: {"questions": ["...", "..."]}
    ```
    The user message is `"Question: …\n\nAnswer: …\n\nDocument sections used: <sorted unique sections>"`. Parse the JSON safely (return `[]` on error), keep questions of 6–150 characters, drop the original question and duplicates, add a missing `?`, and return at most `count`.
11. `getKeywordIndex()` calls `lexical.ensure`. `refreshKeywordIndex()` calls `lexical.scheduleRebuild` when `HYBRID` is on.

## B11. Background indexer — `backend/app/indexer.py`

Keeps ChromaDB and the BM25 index in step with single-file changes made from the admin panel.

- Import `main.py`'s chunking (add the project root to `sys.path`) so admin uploads are chunked **exactly** like a full re-index.
- A **single-worker** `ThreadPoolExecutor`, so files are indexed one after another and there is never more than one writer.
- `statuses`: a dict of file name → `{"state": "queued"|"indexing"|"ready"|"error", "detail", "chunks", "at"}`, guarded by a lock, plus a `version` counter that is bumped on every change.
- **`indexNow(path)`:** set the status to `indexing`, then extract and chunk the file, delete its old chunks and upsert the new ones in batches of 200. **Before each batch, check that the file still exists.** If it was deleted or renamed meanwhile, delete what was written, clear its status and stop. Finish with `ready` (and the chunk count), or `error` with the message.
- `queueIndex(path)`: set the status to `queued`, then submit `indexNow`, followed by `rag.refreshKeywordIndex()`.
- `removeNow(name)`: delete the file's chunks **immediately** (not behind the queue), refresh the keyword index and clear its status.
- `chunkCounts()`: a `Counter` of chunks per source, read from Chroma metadata and cached until `version` changes.
- `statusSnapshot()`: a copy of `statuses`.

## B12. Application entry — `backend/app/main.py`

FastAPI app titled "RAG Q&A" with a **lifespan** that, at startup, calls `createTables()` and `rag.getCollection()`, plus `rag.getReranker()` if `RERANK` is on and `rag.getKeywordIndex()` if `HYBRID` is on. This makes the first question fast. Include the four routers, plus `GET /api/health` returning `{"status": "ok", "chunks": collection.count()}`.

Run it with `cd backend && uvicorn app.main:app --port 8000`.

## B13. API — Auth (`/api/auth`, `routers/auth.py`)

Request bodies (pydantic): `RegisterIn {name: 1–100 characters, email: EmailStr, password: 8–128 characters}`, `LoginIn {email, password}`, `EmailIn {email}`, `TokenIn {token: 10–200 characters}`, `ResetIn {token, password: 8–128 characters}`. Response: `UserOut {id, name, email, is_admin}`.

| Method & path | Behaviour |
|---|---|
| `POST /register` → 201 `{verification_required, user?}` | Lowercase the email. Return **409** "An account with this email already exists" if it is taken. Create the user with an Argon2 hash. If verification is required, issue a `verify` token, email it in the background and return `{verification_required: true}`. Otherwise set `email_verified_at`, set the cookie and return the user. |
| `POST /login` → `UserOut` | Return **401** "Invalid email or password" for a wrong email or password (the same message for both). If verification is required and the account is unverified, return **403** "Please verify your email first. Check your inbox for the link." Otherwise set the cookie. |
| `POST /verify-email` `{token}` | `useToken(…, "verify")`. Set `email_verified_at` if it is empty, **log the user in** (set the cookie) and return the user. |
| `POST /resend-verification` `{email}` | If the user exists, is unverified and had no link in the last 60 s, issue and email a new one. **Always** return `{"message": "If an account exists for that email, we've sent it a link."}`, so the endpoint never reveals which emails exist. |
| `POST /forgot-password` `{email}` | Same pattern with a `reset` token (60 min) and the same generic reply. |
| `POST /reset-password` `{token, password}` | `useToken(…, "reset")`. Set the new hash and `password_changed_at = now` (**which signs out every other session**). Set `email_verified_at` if it is empty, since the link proved the user owns the email. Set the cookie and return the user. |
| `POST /logout` → 204 | Clear the cookie. |
| `GET /me` | The current user (401 if not logged in). |
| `DELETE /me` → 204 | Delete the user's feedback, messages and conversations from `userdata_db`, then the user from `users_db`, and clear the cookie. |

## B14. API — Documents (`/api/documents`, `routers/documents.py`, login required for all)

- **`library()`:** list the supported files in `DATA_DIR` and build the library with `lru_cache(maxsize=8)`, keyed on a tuple of `(file name, modification time)` pairs. **It is rebuilt only when a file is added, removed or changed.** For each file:
  - `readDoc(path)` returns `{slug, title, category, format (extension without the dot, lowercase), text}`. The title is the first line if it looks like a title (non-empty, under 100 characters, not ending in `.!?`), otherwise it comes from the file name.
  - **preview:** the first 200 characters of the body with heading lines removed and whitespace collapsed (dropping the title line if the body starts with it). **For spreadsheets**, the preview is instead a size summary such as `163 rows × 18 columns (Name, Year, …)`.
  - **words:** the word count of the body.
  - Also build `paths` (slug → path) and `aliases` (file stem → slug), so an old `.txt` slug still opens the file after a format change.
- `pathFor(slug)`: look the slug up in `paths`, then `aliases`. **Return 404 "Document not found" if it is missing. Only files listed in the library can ever be served, so no path from the URL reaches the disk (no path traversal).**
- `GET /api/documents` → a list of `{slug, title, category, format, preview, words}`.
- `GET /api/documents/{slug}` → `{slug, title, category, format, text, tables}`, where `tables` comes from `readTables`, or `null` for other formats.
- `GET /api/documents/{slug}/file` → the original file (`FileResponse`, with the real file name).

## B15. API — Chat (`/api`, `routers/chat.py`, login required for all)

Body models: `ChatIn {message: 1–2000 characters, conversation_id?: UUID}`, `SearchIn {query: 1–2000 characters, top_k?: 1–20}`, `FeedbackIn {rating: 1 | -1, reason?: Reason, comment?: ≤ 1000 characters}`.

**`ownConversation(db, id, user)`:** load the conversation only if `user_id == current user`, else 404. **Every query in this router filters by the current user's id.**

**`POST /api/chat` — the main endpoint**
1. Strip the question. Use the existing conversation if `conversation_id` was given; otherwise create one with `title = question[:80]`.
2. Load the **last `HISTORY_TURNS` messages** of this conversation (oldest first).
3. Save the user message and update `conversation.updated_at`. Commit.
4. **Search query** = the previous user question + `"\n"` + the new question. This makes follow-ups like "Who were its astronauts?" still find the right document.
5. `documents, metadatas, distances = rag.search(searchQuery)`, then `sources = collectSources(...)`, then `messages = buildMessages(question, documents, history)`.
6. Return a `StreamingResponse` with `media_type="text/event-stream"` and the headers **`Cache-Control: no-cache, no-transform`** and **`X-Accel-Buffering: no`**. The `no-transform` header stops proxies, including Next.js's gzip, from buffering the stream. Each event is written as `event: <name>\ndata: <json>\n\n`. The events are:
   - `meta` → `{"conversation_id": "...", "sources": [...]}` (sent first)
   - `token` → `{"text": "..."}` (one per token)
   - `error` → `{"message": "Model error: … Is the LLM running?"}`, followed by `done {}`
   - `done` → `{"message_id": "<uuid of the saved answer>"}`
7. Save the assistant message (content + sources) **after** the stream finishes, using a **new** `UserdataSession`, because the request session is closed by then. **Never save an error as an answer**, or it would be fed back as history.

**Other chat endpoints**
| Method & path | Behaviour |
|---|---|
| `POST /api/search` `{query, top_k?}` | Retrieval only: `[{text, source, section, category, distance}]`. Nothing is saved. Used by the evaluation. |
| `GET /api/conversations` | `[{id, title, updated_at}]` for the current user, newest first. |
| `GET /api/conversations/{id}` | `[{id, role, content, sources, created_at, rating, reason}]`. Include the rating and reason from `feedback` where they exist. |
| `DELETE /api/conversations/{id}` → 204 | Delete the conversation; cascading deletes its messages and feedback. |
| `POST /api/conversations/{id}/followups` → `list[str]` | Only if the last two messages are a user message followed by an assistant message, else `[]`. **Close the DB session before calling the LLM.** Any error returns `[]`, since suggestions are optional. |
| `PUT /api/messages/{id}/feedback` | The message must be the current user's own **assistant** message (else 404). Find the user question just before it. Create or update the feedback row with the copies, rating, reason (only when the rating is -1) and comment, and set **status back to `open`**. Returns `{rating, reason}`. |
| `DELETE /api/messages/{id}/feedback` → 204 | Remove the rating, and with it the copy shared with the admins. |

## B16. API — Admin (`/api/admin`, `routers/admin.py`, **every route requires `requireAdmin`**)

Constants: `Editable = {".txt", ".md", ".csv"}`, `MaxUploadBytes = 25 MB`, `Trash = backend/trash`.

`cleanPart(value, label)`: lowercase, replace any non `[a-z0-9]` run with `_`, collapse repeated `_`, strip leading and trailing `_`, and cap at 80 characters. Return 422 if nothing is left. `fileName(category, name, suffix)` = `f"{cleanPart(category)}__{cleanPart(name)}{suffix}"`.

| Method & path | Behaviour |
|---|---|
| `GET /stats` | `users {total, verified, admins, new_7d}`; `questions {total, today, last_7d, per_day: [{date: "YYYY-MM-DD", count}] for the last 14 days in the server's local time zone}`; `conversations` (count); `documents {total, by_format, by_category}` (most common first); `chunks` (Chroma count); `feedback {helpful, not_helpful, open (not helpful and open)}`. |
| `GET /users` | Every account, newest first: `{id, name, email, is_admin, verified, joined, conversations (count), questions (count), last_active}`. **Counts only — never the content of conversations.** |
| `GET /feedback?rating=all\|helpful\|not_helpful&state=all\|open\|resolved` | Defaults `not_helpful` and `open`. Newest `updated_at` first, limit 200. Each item is `{id, rating, reason, comment, question, answer, sources, status, admin_note, user: {name, email} or null, created_at, updated_at}`. |
| `PATCH /feedback/{id}` `{status?, admin_note? ≤ 2000}` | Update and return the item. An empty note becomes `null`. |
| `GET /documents` | Each library document plus `{file, size, modified, chunks, editable, index_state, index_detail}`. `index_state` is the indexer status, or `ready` if it has chunks, or `not indexed`. |
| `GET /index-status` | `indexer.statusSnapshot()` |
| `POST /documents` (multipart: `file`, `category`, `name` optional, `replace` bool) → 201 | Check the extension is in `Supported` (else 422 listing the allowed types). The target is `data/<fileName>`. Return 409 if it exists and `replace` is false. **Stream the upload to a temporary file `.upload-<name>` in 1 MB chunks, aborting with 413 if it passes 25 MB, then atomically `replace()` it into place**, so the library never sees a half-written file. Queue indexing. Return `{file, slug}`. |
| `GET /documents/{slug}/content` | Editable formats only (else 422): `{file, text}`. |
| `PUT /documents/{slug}/content` `{text ≤ 5,000,000}` | Write to `.edit-<name>`, atomically replace the file and queue indexing. |
| `PATCH /documents/{slug}` `{category, name}` | Rename on disk (409 if the target exists), `removeNow(old)` and queue indexing of the new file. Return `{file, slug}`. |
| `DELETE /documents/{slug}` | **Move** the file to `backend/trash/<YYYYmmdd-HHMMSS>-<name>`, so it can be recovered, and `removeNow(name)`. |

**`backend/make_admin.py`** (CLI): `python make_admin.py someone@example.com` grants admin, `… --remove` removes it, and `--list` shows the admins. It calls `createTables()` first.

---

# PART C — FRONTEND

## C1. Project setup

- Next.js App Router, TypeScript (`strict`), path alias `@/*` → project root, Tailwind CSS v4 through `@tailwindcss/postcss` (`postcss.config.mjs`: `plugins: { "@tailwindcss/postcss": {} }`).
- **`next.config.ts`:**
  ```ts
  const backendUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";
  export default {
    experimental: { proxyTimeout: 600_000 }, // the model can take >30 s before its first word on CPU
    async rewrites() { return [{ source: "/api/:path*", destination: `${backendUrl}/api/:path*` }]; },
  };
  ```
- **Route guard** (`proxy.ts` exporting `proxy()` in Next.js 16; in Next.js 15 use `middleware.ts` exporting `middleware()`):
  - `authPages = ["/login", "/register", "/forgot-password"]`; `emailLinkPages = ["/verify-email", "/reset-password"]` (always allowed).
  - Logged in means the cookie `access_token` exists.
  - A logged-out user on a non-auth page goes to `/login?next=<path+query>`, with `next` omitted when the path is `/`.
  - A logged-in user on an auth page goes to `/`.
  - Matcher: `["/((?!api|art/|images/|_next/static|_next/image|favicon.ico).*)"]`, so images and art also load on the login page.

## C2. API client — `lib/api.ts`

- **Types:**
  - `User`, `DocSummary {slug,title,category,format,preview,words}`, `Doc {slug,title,category,format,text,tables: Table[] | null}`, `Table {name,columns,rows,totalRows}`
  - `Source {slug,section,category,distance}`, `Conversation {id,title,updated_at}`, `Rating = 1 | -1`, `FeedbackReason`
  - `ChatMessage {id?, role, content, sources?, rating?, reason?}`
  - `AdminStats`, `AdminUser`, `AdminDoc`, `AdminFeedback` (matching B16)
- `reasonLabels`: `wrong` → "Wrong answer", `not_in_documents` → "Said it's not in the documents", `incomplete` → "Incomplete", `bad_sources` → "Wrong sources", `other` → "Other".
- `class ApiError extends Error { status }`.
- **`api<T>(path, init & {json?})`:** fetch `/api${path}`. When `json` is given, JSON-encode it and set the `Content-Type` header. On a **401** (except from `/auth/login`), call `/api/auth/logout` and redirect to `/login`. When the response isn't OK, throw `ApiError` with the server's `detail` message (or the first validation message). A 204 returns `undefined`.
- **`streamChat(body, handlers, signal)`:** `POST /api/chat` with an `AbortSignal`. Read `res.body.getReader()`, decode the text, split on `\n\n`, parse the `event:` and `data:` lines, and call `onMeta`, `onToken`, `onError` or `onDone`.
- Helpers:
  - `categoryLabel(c)`: capitalised.
  - `sectionAnchor(s)`: lowercase, runs of non `[a-z0-9]` → `-`, leading and trailing `-` trimmed.
  - `sourceHref(source)`: `/documents/<slug>#<anchor of the LAST part of the section path>`.
  - `sourceLabel(source)`: the slug after `__`, with `_` → space.

## C3. Theme data — `lib/theme.ts` and `lib/docArt.ts`

`lib/theme.ts`: per-category cover colour, photo and one-line blurb:

| category | color | image | blurb |
|---|---|---|---|
| food | `#8a4a2b` | `/images/food.webp` | Cuisine, ingredients and the craft of the kitchen |
| general | `#4b3d5e` | `/images/general.webp` | Notes and miscellany from the stacks |
| geography | `#2e5a4c` | `/images/geography.webp` | Places, peoples and the shape of the earth |
| health | `#7a2c3a` | `/images/health.webp` | The body, medicine and wellbeing |
| history | `#6a5226` | `/images/history.webp` | Empires, revolutions and turning points |
| science | `#1f3b5e` | `/images/science.webp` | From atoms to galaxies |
| technology | `#2c3a4b` | `/images/technology.webp` | Machines, software and the networked world |

`categoryStyle(c)` falls back to `general`.

Document types for the filter, in this order: Text `[txt]`, Markdown `[md]`, PDF `[pdf]`, Slides `[pptx, ppt, odp]`, Word `[docx, doc, odt, rtf]`, Spreadsheet `[csv, xlsx, xls, ods]`. `docType(format)` returns `{key, label, formats}`, or the format in capitals for unknown formats. Also export `docTypeOrder`, and `readingTime(words) = max(1, round(words / 230))`.

`lib/docArt.ts`:
- `categoryShades`:
  - food `["#8a4a2b","#7a3f24","#93573a"]`
  - general `["#4b3d5e","#3f3350","#58496b"]`
  - geography `["#2e5a4c","#264d41","#3a6757"]`
  - health `["#7a2c3a","#6a2432","#863a47"]`
  - history `["#6a5226","#5c4620","#775e30"]`
  - science `["#1f3b5e","#1a3252","#2a4a70"]`
  - technology `["#2c3a4b","#243140","#384858"]`
- `titleFromSlug(slug)`: remove a trailing `-ext`, take the part after `__`, replace `_` with spaces, and Title Case it.
- **`seededRandom(seed)`:** a deterministic PRNG, so a document always gets the same art:
  ```ts
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) h = Math.imul(h ^ seed.charCodeAt(i), 16777619);
  return () => { h = Math.imul(h ^ (h >>> 15), h | 1); h ^= h + Math.imul(h ^ (h >>> 7), h | 61); return ((h ^ (h >>> 14)) >>> 0) / 4294967296; };
  ```

## C4. DESIGN SYSTEM (implement exactly)

### C4.1 Design direction
**"Classic library / editorial."** Ivory paper and ink-navy in the day; a warm, lamp-lit reading room at night. The main accent is an oxblood (burgundy) red, with small gold details: thin gold rules, "◆" lozenge ornaments, gold-tooled book covers and small uppercase gold labels. Serif display headings, a serif reading font for documents, and a clean sans-serif for the interface. Real photographs. No emoji anywhere in the interface; use SVG line icons instead. Soft shadows, gentle hover lifts and slow image zooms.

### C4.2 Fonts (load with `next/font/google` in `app/layout.tsx`)
| Role | Font | Options | CSS variable |
|---|---|---|---|
| Interface / sans | **Inter** | subsets latin | `--font-inter` |
| Display headings | **Cormorant Garamond** | weights 500, 600, 700; styles normal + italic | `--font-cormorant` |
| Reading (document body, chat suggestions) | **Source Serif 4** | normal + italic | `--font-source-serif` |
| Code | **Geist Mono** | | `--font-geist-mono` |

Put all four variables on `<html>` together with `h-full antialiased`. Set `<body className="flex min-h-full flex-col font-sans">`.

### C4.3 Theme (day/night) mechanics
- `<html lang="en" data-theme="light" suppressHydrationWarning>`.
- **Inline script in `<head>`** (it runs before the first paint, so the wrong theme never flashes):
  ```js
  (function(){try{var t=localStorage.getItem("theme");if(t!=="light"&&t!=="dark")t=matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";document.documentElement.setAttribute("data-theme",t)}catch(e){}})()
  ```
- `metadata`: title `{ default: "RAG Q&A · The Library", template: "%s · RAG Q&A" }`, description "Browse the document library and ask questions about it."
- `viewport.themeColor`: `#f6f1e7` for light and `#10131a` for dark.
- **`ThemeToggle`** (client component):
  - It has **no React state**. Its look comes entirely from `dark:` classes, so it can never mismatch on hydration.
  - In `useLayoutEffect`, re-apply the stored or system theme (React's development remount can clear the attribute) and listen for OS theme changes, following them only while the user hasn't chosen a theme.
  - Clicking it flips `data-theme`, saves it to `localStorage("theme")`, and adds the class `theme-switching` to `<html>` for 400 ms to cross-fade the colours.
  - Look: a pill `h-9 w-[68px] rounded-full border border-border-strong bg-surface-2 p-1` with a sliding knob `h-7 w-7 rounded-full bg-navy shadow-md`. The knob moves with `transition-transform duration-300 ease-[cubic-bezier(.2,.7,.2,1)]` and gets `dark:translate-x-[30px] dark:bg-accent`.
  - Sun icon (15px) on the left: `text-gold`, `dark:text-muted`, rotating 45° on hover. Moon icon (14px) on the right: `text-muted`, `dark:text-on-accent`, rotating -12° on hover.
  - `aria-label="Toggle day and night mode"`, and on hover `hover:border-text`.

### C4.4 `app/globals.css` — use this file exactly

```css
@import "tailwindcss";

/* `dark:` follows the theme toggle (data-theme on <html>), not only the OS setting. */
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));

/* Tailwind v4 dropped the pointer cursor on buttons; restore it for everything clickable. */
@layer base {
  a[href], button:not(:disabled), [role="button"]:not([aria-disabled="true"]), summary, label[for], select,
  input[type="checkbox"], input[type="radio"], input[type="file"], input[type="submit"], input[type="button"] {
    cursor: pointer;
  }
  button:disabled, [aria-disabled="true"] { cursor: not-allowed; }
}

/* ---------- Colour tokens: "day" (paper & ink) ---------- */
:root {
  color-scheme: light;
  --bg: #f6f1e7;
  --bg-deep: #ede4d3;
  --surface: #fffdf9;
  --surface-2: #f8f3ea;
  --text: #1d2433;
  --muted: #5c6170;
  --faint: #8b8d95;
  --border: #e3dac8;
  --border-strong: #c8baa0;
  --accent: #7b1e2b;
  --accent-hover: #611520;
  --on-accent: #fff8ef;
  --accent-soft: #f5e9e5;
  --gold: #9c7630;
  --gold-soft: #f3ead6;
  --navy: #1c2a43;
  --on-navy: #f6f1e7;
  --success: #2f6b4f;
  --danger: #a4262c;
  --warning: #9a6a16;
  --chart: #7b1e2b;
  --shadow-sm: 0 1px 2px rgb(29 36 51 / 0.05), 0 1px 1px rgb(29 36 51 / 0.03);
  --shadow-md: 0 10px 24px -12px rgb(29 36 51 / 0.25), 0 2px 6px rgb(29 36 51 / 0.05);
  --shadow-lg: 0 28px 50px -20px rgb(29 36 51 / 0.38), 0 6px 14px -6px rgb(29 36 51 / 0.1);
}

/* ---------- "Night" (lamplit reading room) ---------- */
:root[data-theme="dark"] {
  color-scheme: dark;
  --bg: #10131a;
  --bg-deep: #0b0d12;
  --surface: #171b24;
  --surface-2: #1d222d;
  --text: #ece6da;
  --muted: #a8a397;
  --faint: #7a776f;
  --border: #282e3a;
  --border-strong: #3a4252;
  --accent: #d6a85c;
  --accent-hover: #e6bb74;
  --on-accent: #1b1407;
  --accent-soft: rgb(214 168 92 / 0.12);
  --gold: #d6a85c;
  --gold-soft: rgb(214 168 92 / 0.12);
  --navy: #0d1424;
  --on-navy: #ece6da;
  --success: #74c39a;
  --danger: #ee8085;
  --warning: #e3b25e;
  --chart: #d6a85c;
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.4);
  --shadow-md: 0 12px 26px -12px rgb(0 0 0 / 0.7), 0 2px 6px rgb(0 0 0 / 0.3);
  --shadow-lg: 0 30px 60px -20px rgb(0 0 0 / 0.85), 0 6px 14px -6px rgb(0 0 0 / 0.4);
}

@theme inline {
  --color-bg: var(--bg);
  --color-bg-deep: var(--bg-deep);
  --color-surface: var(--surface);
  --color-surface-2: var(--surface-2);
  --color-text: var(--text);
  --color-muted: var(--muted);
  --color-faint: var(--faint);
  --color-border: var(--border);
  --color-border-strong: var(--border-strong);
  --color-accent: var(--accent);
  --color-accent-hover: var(--accent-hover);
  --color-on-accent: var(--on-accent);
  --color-accent-soft: var(--accent-soft);
  --color-gold: var(--gold);
  --color-gold-soft: var(--gold-soft);
  --color-navy: var(--navy);
  --color-on-navy: var(--on-navy);
  --color-success: var(--success);
  --color-danger: var(--danger);
  --color-warning: var(--warning);
  --color-chart: var(--chart);
  --color-ink: #1d2433;
  --font-sans: var(--font-inter);
  --font-serif: var(--font-source-serif);
  --font-display: var(--font-cormorant);
  --font-mono: var(--font-geist-mono);
}

html { scroll-behavior: smooth; }

body {
  color: var(--text);
  background-color: var(--bg);
  background-image:
    radial-gradient(1200px 500px at 50% -200px, var(--surface), transparent 70%),
    url("/art/paper.svg");
  background-attachment: fixed;
  font-feature-settings: "kern", "liga", "calt";
}

::selection { background: var(--accent); color: var(--on-accent); }

:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* Smooth cross-fade while switching day/night (added for a moment by the toggle only). */
.theme-switching, .theme-switching *, .theme-switching *::before, .theme-switching *::after {
  transition: background-color 0.35s ease, border-color 0.35s ease, color 0.35s ease, fill 0.35s ease !important;
}

/* ---------- Components ---------- */
@layer components {
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    box-shadow: var(--shadow-sm);
  }
  .card-hover {
    transition: transform 0.3s cubic-bezier(0.2, 0.7, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
  }
  .card-hover:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--border-strong);
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    border-radius: 10px;
    border: 1px solid transparent;
    padding: 0.55rem 1rem;
    font-size: 0.875rem;
    font-weight: 600;
    line-height: 1.25rem;
    white-space: nowrap;
    transition: background-color 0.2s, border-color 0.2s, color 0.2s, box-shadow 0.2s, transform 0.2s;
  }
  .btn:disabled { opacity: 0.55; }
  .btn:not(:disabled):active { transform: translateY(1px); }
  .btn-primary { background: var(--accent); color: var(--on-accent); box-shadow: var(--shadow-sm); }
  .btn-primary:not(:disabled):hover { background: var(--accent-hover); box-shadow: var(--shadow-md); transform: translateY(-1px); }
  .btn-secondary { background: var(--surface); color: var(--text); border-color: var(--border-strong); }
  .btn-secondary:not(:disabled):hover { background: var(--surface-2); border-color: var(--text); }
  .btn-ghost { color: var(--muted); }
  .btn-ghost:not(:disabled):hover { background: var(--surface-2); color: var(--text); }
  .btn-danger { background: transparent; color: var(--danger); border-color: color-mix(in srgb, var(--danger) 40%, transparent); }
  .btn-danger:not(:disabled):hover { background: color-mix(in srgb, var(--danger) 10%, transparent); border-color: var(--danger); }
  .btn-sm { padding: 0.3rem 0.65rem; font-size: 0.75rem; border-radius: 8px; gap: 0.35rem; }
  .btn-lg { padding: 0.75rem 1.35rem; font-size: 0.95rem; }

  .field {
    width: 100%;
    border-radius: 10px;
    border: 1px solid var(--border-strong);
    background: var(--surface);
    color: var(--text);
    padding: 0.55rem 0.8rem;
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .field::placeholder { color: var(--faint); }
  .field:hover { border-color: var(--muted); }
  .field:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }

  .chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    border-radius: 999px;
    border: 1px solid var(--border-strong);
    background: var(--surface);
    padding: 0.32rem 0.85rem;
    font-size: 0.8125rem;
    font-weight: 500;
    color: var(--muted);
    transition: all 0.2s ease;
  }
  .chip:hover { color: var(--text); border-color: var(--text); }
  .chip[aria-pressed="true"] { background: var(--navy); border-color: var(--navy); color: var(--on-navy); }
  :root[data-theme="dark"] .chip[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    border-radius: 6px;
    border: 1px solid var(--border-strong);
    padding: 0.1rem 0.45rem;
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    white-space: nowrap;
  }
  .badge-success { color: var(--success); border-color: color-mix(in srgb, var(--success) 45%, transparent); background: color-mix(in srgb, var(--success) 8%, transparent); }
  .badge-warning { color: var(--warning); border-color: color-mix(in srgb, var(--warning) 45%, transparent); background: color-mix(in srgb, var(--warning) 8%, transparent); }
  .badge-danger { color: var(--danger); border-color: color-mix(in srgb, var(--danger) 45%, transparent); background: color-mix(in srgb, var(--danger) 8%, transparent); }
  .badge-accent { color: var(--accent); border-color: color-mix(in srgb, var(--accent) 45%, transparent); background: var(--accent-soft); }

  .eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
  }

  .link {
    color: var(--accent);
    font-weight: 600;
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
    text-decoration-color: color-mix(in srgb, var(--accent) 40%, transparent);
    transition: text-decoration-color 0.2s;
  }
  .link:hover { text-decoration-color: var(--accent); }

  /* Animated underline for nav-style links */
  .underline-grow { background: linear-gradient(currentColor, currentColor) 0 100% / 0 1px no-repeat; transition: background-size 0.3s ease; }
  .underline-grow:hover { background-size: 100% 1px; }

  /* A thin rule with a gold lozenge in the middle: ——— ◆ ——— */
  .ornament { display: flex; align-items: center; gap: 0.9rem; color: var(--gold); }
  .ornament::before, .ornament::after { content: ""; height: 1px; flex: 1; background: linear-gradient(90deg, transparent, var(--border-strong), transparent); }

  .skeleton {
    background: linear-gradient(100deg, var(--surface-2) 30%, var(--bg-deep) 50%, var(--surface-2) 70%);
    background-size: 300% 100%;
    animation: shimmer 1.6s ease-in-out infinite;
    border-radius: 8px;
  }

  /* Long-form reading */
  .prose-doc { font-family: var(--font-serif); font-size: 1.0625rem; line-height: 1.85; color: var(--text); }
  .prose-doc p { text-wrap: pretty; }
  .drop-cap::first-letter {
    float: left;
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 4.1em;
    line-height: 0.8;
    padding: 0.08em 0.1em 0 0;
    color: var(--accent);
  }

  /* Image that zooms gently inside its frame on hover of the parent .group */
  .zoom-img { transition: transform 0.9s cubic-bezier(0.2, 0.7, 0.2, 1), filter 0.5s ease; }
  .group:hover .zoom-img { transform: scale(1.06); }
}

@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
@keyframes pop-in { from { opacity: 0; transform: translateY(12px) scale(0.98); } to { opacity: 1; transform: none; } }
@keyframes shimmer { from { background-position: 100% 0; } to { background-position: 0 0; } }
@keyframes blink {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.35; }
  40% { transform: scale(1); opacity: 1; }
}
@keyframes slide-in-right { from { opacity: 0; transform: translateX(28px); } to { opacity: 1; transform: none; } }
@keyframes ken-burns { from { transform: scale(1.08); } to { transform: scale(1); } }

.animate-fade { animation: fade 0.25s ease-out; }
.animate-rise { animation: rise 0.6s cubic-bezier(0.2, 0.7, 0.2, 1) both; }
.animate-pop-in { animation: pop-in 0.28s cubic-bezier(0.2, 0.7, 0.2, 1); transform-origin: bottom right; }
.animate-slide-in-right { animation: slide-in-right 0.3s cubic-bezier(0.2, 0.7, 0.2, 1); }
.animate-ken-burns { animation: ken-burns 14s ease-out both; }
.dot { animation: blink 1.2s infinite ease-in-out; }
.dot:nth-child(2) { animation-delay: 0.15s; }
.dot:nth-child(3) { animation-delay: 0.3s; }

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .animate-fade, .animate-rise, .animate-pop-in, .animate-slide-in-right, .animate-ken-burns, .dot, .skeleton { animation: none; }
  .card-hover:hover, .btn-primary:not(:disabled):hover { transform: none; }
  .group:hover .zoom-img { transform: none; }
}

/* Sign-in pages: tighten the card on short windows so the page never needs to scroll. */
@media (max-height: 780px) {
  .auth-pane { padding-top: 1.75rem; padding-bottom: 1.75rem; }
  .auth-pane h1 { font-size: 2.1rem; }
  .auth-pane form { margin-top: 1.25rem; }
  .auth-pane form > * + * { margin-top: 0.85rem; }
  .auth-pane .ornament { margin-top: 1.1rem; }
  .auth-pane .ornament + p, .auth-pane form + p { margin-top: 0.9rem; }
  .auth-art p.font-display { font-size: 2.1rem; }
}
@media (max-height: 640px) {
  .auth-pane .ornament { display: none; }
  .auth-pane h1 + p { display: none; }
}
@media (max-width: 767px) {
  .auth-pane form { margin-top: 1.25rem; }
  .auth-pane form > * + * { margin-top: 0.9rem; }
  .auth-pane .ornament { margin-top: 1.1rem; }
  .auth-pane .ornament + p { margin-top: 0.9rem; }
}

/* Thin, quiet scrollbars */
* { scrollbar-width: thin; scrollbar-color: var(--border-strong) transparent; }

/* Markdown inside chat answers */
.md > * + * { margin-top: 0.5rem; }
.md ul { list-style: disc; padding-left: 1.25rem; }
.md ol { list-style: decimal; padding-left: 1.25rem; }
.md li::marker { color: var(--gold); }
.md code { font-family: var(--font-mono); font-size: 0.85em; background: var(--surface-2); border: 1px solid var(--border); padding: 0.05rem 0.3rem; border-radius: 4px; }
.md pre { background: var(--surface-2); border: 1px solid var(--border); padding: 0.75rem; border-radius: 8px; overflow-x: auto; }
.md pre code { padding: 0; border: 0; background: none; }
.md a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
.md strong { font-weight: 650; }

/* Chat PDF export: only the transcript is printed, always in light colours. */
.print-transcript { display: none; }
@media print {
  @page { margin: 16mm; }
  body { background: #fff !important; }
  body > *:not(.print-transcript) { display: none !important; }
  .print-transcript { display: block; color: #1d2433; font-family: var(--font-serif), Georgia, serif; font-size: 11pt; line-height: 1.55; }
  .print-transcript h1 { font-family: var(--font-display), Georgia, serif; font-size: 22pt; font-weight: 700; }
  .print-meta { color: #666; font-size: 9pt; margin-bottom: 12pt; }
  .print-msg { padding: 8pt 0; border-top: 1px solid #ddd; break-inside: avoid-page; }
  .print-role { font-family: var(--font-inter), sans-serif; font-weight: 700; font-size: 8pt; text-transform: uppercase; letter-spacing: 0.12em; color: #7b1e2b; margin-bottom: 4pt; }
  .print-user .print-role { color: #9c7630; }
  .print-transcript .md code, .print-transcript .md pre { background: #f6f1e7; border-color: #e3dac8; }
  .print-transcript .md pre { white-space: pre-wrap; }
  .print-transcript .md a { color: #1d2433; }
  .print-sources { margin-top: 6pt; padding-left: 12pt; list-style: disc; font-size: 9pt; color: #555; }
}
```

### C4.5 Static art — `public/art/paper.svg` (subtle paper grain, tiled behind every page)
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
  <filter id="grain" x="0" y="0">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch" />
    <feColorMatrix type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0.07 0" />
  </filter>
  <rect width="240" height="240" filter="url(#grain)" />
</svg>
```

### C4.6 Photographs — `public/images/`
Download free photos from **Unsplash** (Unsplash License), resize them and save as **WebP** (quality about 74). List each photo's source URL in `public/images/CREDITS.md`.

| File | Subject | Max width |
|---|---|---|
| `hero-shelves.webp` | Close-up of old leather-bound books on wooden library shelves | 1600 |
| `library-aisle.webp` | A long, dim library aisle lit by hanging bulbs (used on the auth pages) | 1100 |
| `food.webp` | Top-down shot of plated food on rustic wood | 1200 |
| `general.webp` | Many open book pages laid out flat | 1200 |
| `geography.webp` | Mountain valley landscape with pine trees | 1200 |
| `health.webp` | Stethoscope (black-and-white works well) | 1200 |
| `history.webp` | The Colosseum in Rome | 1200 |
| `science.webp` | Laboratory glassware (beakers, pipette) | 1200 |
| `technology.webp` | Close-up of a circuit board | 1200 |

Use `next/image` with `fill`, a correct `sizes` value, `object-cover` and `priority` for above-the-fold images.

### C4.7 Icons — `components/icons.tsx`
A small set of SVG line icons, so the interface never relies on emoji. The base `Icon` component draws on a 24×24 viewBox with `fill="none"`, `stroke="currentColor"`, `strokeWidth={1.6}`, round caps and joins, `aria-hidden`, and a `size` prop defaulting to 18.

Icons needed: Sun, Moon, Search, Book (open book), Download, ArrowLeft, ArrowRight, ArrowUp, Chat (speech bubble with lines), Close (X), Send (paper plane), History (clock with a back arrow), Plus, Trash, Clock, Settings (three sliders), Logout, File, List, ThumbUp, ThumbDown, Quill. Add **`CategoryIcon({category})`**:
- food: fork and knife
- geography: mountain
- health: heart with a pulse line
- history: classical columns
- science: flask
- technology: chip
- default: book

**`Emblem`** (the logo seal, 48×48 viewBox):
- A navy circle (r 22.5, `fill="var(--navy)"`) with two thin gold rings (r 19.5 at stroke 0.9 and r 17.8 at stroke 0.5, `stroke="var(--gold)"`).
- An open book made of two gold page shapes, the right one at 75% opacity, with a navy spine line.
- A small gold five-point star above the book.

### C4.8 Generated book covers — `components/DocArt.tsx`
Every document card shows a **"clothbound book cover"** SVG, generated deterministically from its slug with `seededRandom(slug)`.

- **Props:** `slug`, `category`, `className`, `portrait?`. Landscape uses a `240×120` viewBox (cards); portrait uses `180×240` (the document page). Use `preserveAspectRatio="xMidYMid slice"`, `aria-hidden`, and unique ids from `useId()` for the patterns and gradients.
- `gold = "#d9b46a"`. The cloth colour is a random pick from `categoryShades[category]`.
- **Layers, from back to front:**
  1. A cloth-coloured rectangle.
  2. A **linen weave**: a 3×3 pattern of white `M0 0h3M0 0v3` lines at stroke 0.35 and opacity 0.18.
  3. A **gold ornament pattern**, one of 5 chosen at random: diamond lattice (16px), dots (14px), a fine cross grid (20px, stroke 0.4), fan arcs (24px), or four-point stars (18px). Its placement is one of 3 layouts: the full field (opacity 0.22), side panels 26% wide (opacity 0.3), or top and bottom bands 22% high (opacity 0.32).
  4. A **vignette**: a radial gradient from transparent at 55% to black at opacity 0.38.
  5. A **double gold frame**: a rect inset 9 at stroke 0.9 and opacity 0.75, then a rect inset 12.5 at stroke 0.5 and opacity 0.55.
  6. A **central medallion** at (W/2, 60), or (W/2, 100) in portrait. It's a cloth-filled circle (r 27) stroked with a gold linear gradient (`#f1d79b` → `#d9b46a` → `#a8823e`), plus an inner ring (r 23.5, stroke 0.45). Inside is the **first letter of the title** in the display font: italic, weight 600, size 34, filled with the gold gradient. In landscape, add two short horizontal rules (`M-48 0h15M33 0h15`) and two small diamonds (`M-53 0l3-3 3 3-3 3zM53 0l-3-3-3 3 3 3z`) on either side.
  7. **Portrait only:** a 60-unit gold rule at y 145, the title wrapped at 16 characters (at most 3 lines, display font, size 15, weight 600, starting at y 165 with 17-unit line spacing), and a small diamond near the bottom.

### C4.9 Layout components
- **`(site)/layout.tsx`:** `UserProvider` → `Header` → `<main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6">` → `SiteFooter` → `BackToTop` → `ChatWidget`.
- **`UserProvider`** (client): fetch `/auth/me` on mount and provide the user through context (`useUser()`). Until it loads, show a centred `Emblem` (44px, `animate-pulse`) with "Opening the library…".
- **`Header`** (client):
  - `sticky top-0 z-10 border-b bg-bg/85 backdrop-blur-md`. After scrolling more than 8px, add `border-border` and a soft shadow `shadow-[0_8px_24px_-18px_rgb(0_0_0/0.5)]`; at the top, `border-transparent`.
  - A **3px gradient strip** at the very top: `linear-gradient(90deg, var(--navy), var(--accent) 50%, var(--gold))`.
  - **Left:** the logo link, an `Emblem` (38px) that rotates -8° on hover over 500ms, beside the wordmark "RAG *Q&A*". The wordmark is `font-display text-[1.6rem] font-semibold`, with "Q&A" italic in the accent colour. Under it, "THE DOCUMENT LIBRARY" (0.62rem, tracking 0.28em, faint, hidden on mobile).
  - **Right:** nav links with icons ("Library" hidden below md, and "Admin" for admins only). Each is `rounded-lg px-3 py-1.5 text-sm font-medium`, styled `bg-surface-2 text-text` when active and `text-muted hover:bg-surface-2 hover:text-text` otherwise.
  - After the links: a 1px vertical divider, the `ThemeToggle`, a user avatar (an 8×8 navy circle with a gold border and the gold initial in the display font, plus the name, shown on lg and up), and a "Log out" ghost button with an icon. Log out calls `POST /auth/logout`, then goes to `/login`.
- **`SiteFooter`:** `mt-20 border-t border-border bg-surface-2/60`, centred:
  - an `Emblem` (34px);
  - the italic display quote "“A library is not a luxury but one of the necessities of life.”" with "HENRY WARD BEECHER" underneath (xs, tracking 0.2em, faint);
  - an `ornament` (max-w-xs, containing "◆");
  - a small line: "RAG Q&A · Answers are generated from the library's documents — check the cited sources. Photography from Unsplash." The Unsplash link uses `underline-grow`.
- **`BackToTop`:** a round 40px button, `fixed right-[1.6rem] bottom-24 z-[14]`, with a border, a surface background and `shadow-md`. It appears once `scrollY > 700`, fading in and sliding up 12px (`transition-all duration-300`), and lifts 2px on hover. Clicking it scrolls to the top.

## C5. Pages

### C5.1 Auth pages — `AuthShell`, `AuthForm`, `ResendVerification`
**`AuthShell`:**
- `<main className="relative flex flex-1 items-center justify-center px-4 py-4 sm:py-6">` with the `ThemeToggle` placed in an `absolute top-4 right-4 z-10` wrapper. Wrap the toggle in this div; don't put `absolute` on the toggle itself.
- The card: `animate-rise grid w-full max-w-5xl overflow-hidden rounded-[22px] border border-border bg-surface shadow-lg md:grid-cols-[1.05fr_1fr]`.
- **Left art panel** (`auth-art`): `relative isolate flex min-h-32 flex-col justify-between overflow-hidden bg-navy p-6 text-[#ece6da] md:min-h-[min(600px,calc(100dvh-3rem-2px))] md:p-10`. The `-2px` accounts for the card's border.
  - The `library-aisle.webp` photo, with `animate-ken-burns` (a slow 14s zoom-out).
  - A gradient overlay `linear-gradient(180deg, rgb(13 20 36/.55) 0%, rgb(13 20 36/.35) 40%, rgb(13 20 36/.92) 100%)`.
  - An inset gold hairline frame: `absolute inset-3 rounded-[14px] border border-[#d9b46a]/25`.
  - **Top:** the `Emblem` (40px) and wordmark (gold italic "Q&A" `#e6c483`, with "THE DOCUMENT LIBRARY" underneath).
  - **Bottom** (md and up): "Ask the library." followed by an italic gold line "It answers, with sources." (`font-display text-[2.6rem] leading-[1.05]`), and a small paragraph: "A reading room of documents on history, science, food, health and more — and a librarian who has read every page."
- **Right pane:** `auth-pane flex flex-col justify-center p-6 sm:p-12`.
- **The auth pages must never scroll.** Test them at window heights of 900, 768, 650 and 600px and at 390×844 on mobile. The `.auth-pane` and `.auth-art` media queries in globals.css handle short windows.
- Exports: `inputClass = "field"`, `buttonClass = "btn btn-primary btn-lg w-full"`, `linkClass = "link"`.
- **`StatusMark`:** a round 56px icon badge, toned `accent` or `success`.
- **`Notice`:** an alert box with `border border-l-4`. The error tone is `border-danger/40 bg-danger/[0.07] text-danger`; the success tone is `border-success/40 bg-success/[0.08]`. Use `role="alert"` for errors and `role="status"` for success.

**`AuthForm`** (mode `login` | `register`):
- **Login:** the eyebrow "MEMBERS' ENTRANCE", the h1 "Welcome back" (`font-display text-[2.6rem] font-semibold`) and the subtitle "Log in to pick up where you left off."
- **Register:** the eyebrow "NEW READER", the h1 "Join the library" and the subtitle "Create an account to start asking."
- **Fields:** Name (register only), Email and Password. In login mode the password label row has a "Forgot password?" link on the right. In register mode, show the hint "At least 8 characters." The button reads "Log in →" or "Create account →" (with an arrow icon), and "One moment…" while busy.
- Then an `ornament` and the footer link: "New here? Create an account" or "Already have an account? Log in".
- A 403 error (unverified account) also shows a `ResendVerification` button inside the error notice.
- After registering with verification on, show "Check your inbox". This has a mail-icon `StatusMark`, the email address in bold, "The link expires in 24 hours", a resend button and "Already verified? Log in".
- After logging in, go to `next` if it's a safe relative path (starts with `/` and not `//`), otherwise `/`.

**Other auth pages:**
- `/forgot-password`: the eyebrow "ACCOUNT RECOVERY", the h1 "Forgot your password?", an email field, and the button "Send reset link". On success, show a success notice with the server's message plus "The link expires in 1 hour."
- `/reset-password?token=`: "Choose a new password", with a new-password field and a repeat field (showing "The two passwords don't match." when they differ). On success, show a lock `StatusMark`, "Password changed" and "any other sessions were signed out", then redirect to `/` after 1.5 s. Errors include a "Request a new link" link.
- `/verify-email?token=`: show "Verifying your email…" (pulsing) while it calls the API **once**, guarded with a ref against React's development double-run. On success, show a check `StatusMark`, "Email verified" and redirect to `/` after 1.5 s. On failure, show "Link not valid" with an email field and a resend button.
- **`ResendVerification`:** `btn btn-secondary btn-sm`. It shows "Sending…" while the request runs, then "Sent! Check your inbox", disabled for 60 s.

### C5.2 Library home — `(site)/page.tsx`
1. **Hero:**
   - The container: `relative isolate overflow-hidden rounded-[22px] bg-navy text-on-navy shadow-lg`.
   - The background is `hero-shelves.webp` with `animate-ken-burns`, under a gradient `linear-gradient(100deg, rgb(13 20 36/.96) 0%, rgb(13 20 36/.86) 45%, rgb(13 20 36/.35) 100%)`, inside an inset gold hairline frame (`inset-3 sm:inset-4 rounded-[16px] border-[#d9b46a]/25`).
   - Content (`animate-rise`, `px-6 py-12 sm:px-12 sm:py-16 lg:py-20`): the eyebrow "THE READING ROOM" in `#d9b46a`, then the h1 "Every answer, *properly sourced.*" (`font-display text-[2.6rem] sm:text-6xl lg:text-[4.2rem] leading-[1.02] font-semibold`, with the italic part in `#e6c483`).
   - The paragraph: "Browse a curated collection of documents on history, science, food, health and more — or ask the librarian, who answers only from these pages and cites every source." (`text-[#ece6da]/80`).
   - Buttons:
     - **"Ask the librarian"** (gold `#d9b46a` background, dark text `#1b1407`, chat icon, lifts on hover) calls `openChat()`.
     - **"Browse the collection →"** (outline style, `border-[#ece6da]/35`, `hover:bg-white/10`) scrolls to the collection.
   - A stats row `<dl>` above a top gold hairline. Each stat has a small uppercase label (tracking 0.22em) and a big gold display-font number (`text-3xl text-[#e6c483] tabular-nums`): **Documents**, **Subjects**, **Words indexed**. Show "—" while loading.
2. **"Browse by subject":**
   - A centred section heading: the eyebrow, then the display-font title "The Shelves" (`text-4xl sm:text-[2.75rem]`), then an ornament (max 220px).
   - One **photo tile per category**, in a 7-column grid on xl, 4 on lg and 3 on sm. On mobile they become a horizontal snap-scrolling row of 160px tiles.
   - Each tile: `h-52 rounded-[14px] shadow-md`, lifting 4px with `shadow-lg` on hover. The photo uses `zoom-img`, under a gradient overlay from transparent at 15% to the category colour at 92% (opacity 0.8, falling to 0.65 on hover) and a 15% black layer.
   - Inside the tile: a round glass icon badge at the top (`border-white/40 bg-black/20 backdrop-blur-sm`), the category name in the display font (`text-2xl`) and "N volumes".
   - Clicking a tile filters the list by that category (clicking again clears it) and scrolls to the collection. The active tile gets `ring-2 ring-accent ring-offset-2 ring-offset-bg`. Tiles animate in with `animate-rise`, staggered 60ms each.
3. **"The Collection"** (the same heading style, eyebrow "THE CATALOGUE"). Then a `card p-4 sm:p-5` toolbar:
   - A **search input** (`field` with a left search icon and a right `<kbd>/</kbd>` hint). Pressing **`/` anywhere** focuses it, unless the user is already typing in a field, and `Esc` clears it. It filters by title.
   - **Category chips:** "All subjects" plus one per category with its `CategoryIcon`. These use the `chip` class with `aria-pressed`.
   - Below a divider: **format chips** ("FORMAT" label, "All (n)", and each type with counts based on the current subject and search; types with 0 matches are disabled), plus a **Sort by** select: "Title (A–Z)", "Longest first", "Shortest first".
   - Under the toolbar: "Showing **X** of Y documents" (`aria-live="polite"`), plus a "Clear filters" link when any filter is active.
4. **Document grid:** 1 column, 2 on sm and 3 on lg, with `gap-5 sm:gap-6`. **Card** = `card card-hover group animate-rise flex flex-col overflow-hidden`, with an `animationDelay` of `min(i, 11) * 40ms`:
   - Top: `DocArt` (landscape, `h-36`, `zoom-img`), plus a small format badge at the top right for non-txt files (`bg-black/35 backdrop-blur-sm`, gold `#f1d79b` uppercase 10px text, tracking 0.12em).
   - Body (`p-5`): an eyebrow with the category icon and label, then the title (`font-display text-[1.6rem] leading-[1.1] font-semibold`, which turns accent-coloured on hover). Then the preview (3-line clamp, sm, muted).
   - Footer row (xs, faint): a clock icon with "N min read · N words", and on the right "Read →" in the accent colour, hidden until hover, when it fades in and slides 2px right.
5. **Loading:** 6 skeleton cards (a `skeleton` block `h-36`, then skeleton lines).
6. **Empty state:** a card with a gold search icon, "Nothing on the shelves matches that.", a hint, and an "Ask the librarian" primary button.

### C5.3 Document reader — `(site)/documents/[slug]/page.tsx`
- Fetch `/documents/{slug}` and set `document.title` to "<title> · RAG Q&A". When the URL has a `#hash`, scroll to that section after loading.
- **Text parsing:** drop the first line if it equals the title. Lines matching `^(=+)\s*(.+?)\s*\1$` are headings (level = the number of `=`). Blank lines separate paragraphs, and **each source line inside a paragraph is rendered as its own `<p>`**, so text isn't one dense block.
- **Reading-progress bar:** `fixed inset-x-0 top-0 z-20 h-[3px]`. The inner `bg-accent` bar uses `scaleX(progress)` with `origin-left` and a 150ms transition, where progress = scrollY / (scrollHeight − innerHeight).
- **Breadcrumb:** "← Library / <Category> / <Title>". The arrow slides left on hover, and the title is hidden on mobile.
- **Title banner:**
  - `relative isolate mt-5 overflow-hidden rounded-[22px] text-white shadow-lg`.
  - The background is the category photo with `animate-ken-burns`, under a gradient in the **category colour**: `linear-gradient(100deg, <color>f2 0%, <color>d9 45%, <color>66 100%)`. Add an inset hairline frame in `border-white/20`.
  - **Left** (`animate-rise`): an eyebrow in gold `#f1d79b` with the category icon, label and a bordered format tag. Then the h1 (`font-display text-[2.6rem] sm:text-6xl leading-[1.02] font-semibold`). Then a meta row: a clock icon with "N min read" (not for tables), "N words" or "N tables", and "N sections".
  - Buttons: **"Ask about this document"** (`#f1d79b` background, chat icon) calls `openChat("What are the key points of “<title>”?")`. **"Download original (.ext)"** is an outline link to `/api/documents/{slug}/file` with the `download` attribute.
  - **Right** (lg and up): the **portrait `DocArt`** as a 224px-wide book, `rotate-2 rounded-md`, with the shadow `0 24px 40px -12px rgb(0 0 0/.6)` and `ring-1 ring-black/30`. It straightens (`rotate-0`) on hover over 500ms.
- **Body:**
  - Spreadsheets: one `DataTable` per table.
  - Otherwise a grid, `lg:grid-cols-[1fr_250px]` when there is more than one top-level section.
  - The **article** is `card prose-doc px-6 py-10 sm:px-14 sm:py-14` with the text column at `max-w-[68ch]`, `space-y-5`.
  - **The first paragraph gets the `drop-cap` class.**
  - h2 (level ≤ 2): display font, `text-[2rem]`, a bottom border, `!mt-12`. Level 3 and deeper: `text-[1.45rem]` italic, `!mt-8`. Every heading has `id = sectionAnchor(text)` and `scroll-mt-24`.
  - End the article with an ornament "◆ ◆ ◆".
- **Table of contents** (lg and up): a sticky card (`top-24`) with the eyebrow "CONTENTS" (list icon), a left-bordered list of the h2 sections, and the **current section highlighted** (`border-l-2 border-accent text-accent font-medium`). Track it with an IntersectionObserver using `rootMargin: "-90px 0px -65% 0px"`.
- **Loading:** a skeleton of the breadcrumb, banner and text lines. **Error:** a card reading "This volume is missing", with the error and a "Back to the library" button.
- **`DataTable`:**
  - A card whose header shows the table name in the display font and "N ROWS × N COLUMNS" (xs, uppercase, faint).
  - The body is scrollable (`max-h-[70vh]`) with a **sticky header row whose background is the category colour**, white uppercase xs semibold text and a row-number column.
  - Rows alternate `bg-surface` / `bg-surface-2`, with `hover:bg-gold-soft`.
  - **Numeric columns** (where every value matches `^[-+]?[\d,]*\.?\d+%?$`) are right-aligned with `tabular-nums`. The first column is `font-medium`.
  - snake_case column names are prettified to "Sentence case".
  - Show a "Showing the first N of M rows" footer when the rows are truncated.

### C5.4 Chat widget — `components/ChatWidget.tsx` (client)
- Export **`openChat(question?: unknown)`**. It dispatches a `CustomEvent("open-chat", {detail: question if it's a string})`, and the widget listens for it, opens on the chat tab, pre-fills the input and focuses it.
- **Launcher:** a round 60px button at `fixed right-5 bottom-5 z-[31]`, `bg-navy text-[#d9b46a] shadow-lg ring-1 ring-[#d9b46a]/40`, with an inner hairline ring. It lifts 4px on hover, when the ring turns solid gold. In dark mode it's `bg-accent text-on-accent`.
  - It shows the chat icon, which scales up 110% on hover. While the panel is open it shows a close icon that rotates 90° on hover, and **the button stays visible on desktop to close the panel**. On mobile it's hidden while open.
- **Hint pill** (sm and up, before the chat is first opened): "*Ask the librarian* →" next to the launcher at `fixed right-24 bottom-[1.85rem]`, rounded-full, surface background, `shadow-md`, rising in after 600ms. It **disappears after 9 s or once the page has scrolled more than 400px**.
- **Panel position:** it opens **to the LEFT of the launcher, at full window height**: `fixed inset-0 z-30 … sm:inset-auto sm:top-3 sm:bottom-3 sm:right-[5.75rem] sm:w-[420px] sm:rounded-2xl sm:border sm:border-border`. On mobile it fills the screen.
  - It uses `animate-slide-in-right` and `bg-surface shadow-lg`.
  - Behind it sits a backdrop `fixed inset-0 z-[25] bg-black/30 backdrop-blur-[2px] animate-fade`. Clicking the backdrop or pressing **Esc** closes the panel.
  - **While it's open, lock the page scroll** (`document.documentElement.style.overflow = "hidden"`, restored on close).
- **Panel header** (`bg-navy`, `text-[#ece6da]`):
  - The `Emblem` (42px), the title "The Librarian" (`font-display text-xl`), and the subtitle "Answers from the library, with sources" with a small green status dot.
  - Header buttons (`border-[#ece6da]/25`, xs): "⬇ PDF" (only when there are messages) and "+ New". There is also a close X, shown on mobile only.
  - A segmented tab control (`bg-black/25 p-1 rounded-lg`) with "Chat" and "History". The active tab is `bg-[#d9b46a] text-[#1b1407]`.
  - A gold gradient hairline along the bottom edge.
- **Message list:** `flex flex-1 flex-col gap-4 overflow-y-auto bg-bg/40 p-4`.
  - **Only scroll this list, never the page**: set `scrollTop = scrollHeight` when messages change and there is at least one message. Do not use `scrollIntoView`.
  - **Empty state** (vertically centred with `my-auto`, and it **must fit without scrolling** down to 600px-tall windows):
    - The `Emblem` (56px), then a **time-based greeting**: "Good morning/afternoon/evening, <first name>." (`font-display text-[1.6rem]`).
    - "I've read every document in the library. What would you like to know?"
    - An ornament, hidden below a window height of 680px.
    - 4 suggestion buttons: "When was Kubernetes first released?", "What causes earthquakes?", "Who were the Vikings?" and "Is caffeine bad for you?". These are full-width rows in the serif italic font, each with a send icon on the right that turns accent-coloured on hover, as does the border, and the row lifts 1px. Below a window height of 680px, tighten them (`py-2`, `space-y-1.5`).
  - **User bubble:** right-aligned, `max-w-[85%] rounded-2xl rounded-br-md bg-navy text-on-navy`, and in dark mode `bg-accent text-on-accent`.
  - **Assistant:** the `Emblem` (28px) beside a bubble `rounded-2xl rounded-tl-md border border-border bg-surface shadow-sm`, rendering **Markdown** (`.md` styles, leading-6).
    - While it's waiting: three bouncing accent dots (`.dot`) and an italic "Consulting the shelves…".
    - **Sources:** below a top border, an eyebrow "SOURCES" and up to 4 chips (a file icon and the source label in capitalised words, `rounded-md border bg-surface-2`, accent border and text on hover). Each chip links to `sourceHref`, with a `title` showing the section.
  - **Feedback** under each saved answer:
    - Round 28px 👍/👎 icon buttons (`aria-pressed`). Clicking the active one removes the rating.
    - 👎 opens a panel with "What was wrong?", the reason chips, an optional comment ("What should the answer have said? (optional)", max 1000) and the note "This question and answer will be shared with the library admins so they can fix the documents.", with "Send" and "Skip" buttons.
    - After rating, show "Thanks! Shared with the library admins · <reason>".
  - **Follow-ups:** after an answer finishes, call `/conversations/{id}/followups`. Show "YOU COULD ALSO ASK" with question buttons that send the question when clicked. Discard stale results using a request counter.
- **Input bar** (`border-t bg-surface p-3`): a `field` with the placeholder "Ask the library anything…" (max 2000) and a primary send button with a send icon, disabled when the input is empty. While an answer is streaming, the button becomes a secondary "Stop" button, which aborts the `AbortController`.
- **Streaming:** append the user message plus an empty assistant message. `onMeta` sets the conversation id and sources, `onToken` appends text, `onDone` stores the `message_id`, and `onError` replaces the content with the error. A network error shows its message, unless the user aborted.
- **History tab:** load `/conversations` when opened. Show a list of cards (title in semibold, which turns accent on hover, and the date). Clicking one loads its messages. A trash button, faded until hover, turns red on hover and deletes the conversation (if it's the open one, start a new chat). Empty state: a gold history icon and "No conversations yet. Ask me something!".
- **PDF export:** render a portal into `document.body` with `.print-transcript`. It contains an h1 with the title, "The Librarian · exported <date>", and each message with a role label ("You" or "The Librarian"), the content as Markdown, and its sources (with full URLs). Temporarily set `document.title` to "The Librarian - <title>", call `window.print()`, and restore the title on `afterprint`.

### C5.5 Admin panel — `(site)/admin/page.tsx` and `components/admin/*`
- Non-admins see a centred gold settings icon, "Admins only" and "Ask an admin to give your account access."
- **Header:** the eyebrow "LIBRARY MANAGEMENT" and the h1 "Admin panel" (`font-display text-4xl sm:text-5xl`).
- **Underline tabs** (`border-b`; the active tab is `border-b-2 border-accent text-accent`): Overview, Users (count pill), Feedback (an **accent-coloured count pill** of open items), Documents (count pill).
- **Overview:**
  - 5 **StatTiles** (`card card-hover`, with a 3px top accent→gold gradient bar, a faint eyebrow label and a big display number `text-4xl tabular-nums`, plus a detail line):
    - **Users:** "N verified · N new this week"
    - **Questions asked:** "N today · N this week"
    - **Conversations**
    - **Documents:** "N searchable chunks"
    - **Answers rated helpful:** a percentage, with "N helpful · N not helpful · N to review"
  - **QuestionsChart** (`card p-6`): the title "Questions per day · last 14 days" and a "View as chart/table" toggle link.
    - 14 bars with rounded tops in `bg-chart`, a y-axis of 0 / half / nice max (4, or the next value in the 1-2-5 × 10ⁿ series), and dashed gridlines.
    - Date labels on every other day. The peak value is labelled above its bar.
    - **Hovering or focusing a bar dims the others to 40% and shows a tooltip card** with the date and count. Bars are focusable with aria-labels.
    - The table view lists day and count.
  - Two **Breakdown** cards ("Documents by type", "Documents by category"), each a table of label, a thin bar (`h-1.5 bg-chart` on `bg-surface-2`, width animated over 700ms) and the count.
- **Users:** a card table with the columns User (name and email), Joined, Status (badges: success "Verified", warning "Unverified", accent "Admin"), Conversations, Questions and Last active. Rows highlight on hover. The header note reads "Counts only — what users asked stays private to them."
- **Feedback:**
  - Filter chips: "To review", "Resolved", "Helpful" and "All", with the note "Only answers that users rated are shown — rating shares that question and answer."
  - Each item is a card with:
    - a round rating icon (green 👍 or red 👎 line icon), a reason badge (danger), a status badge ("Open" warning or "Resolved" success), and the user and date;
    - the question as the title (display font, xl);
    - a collapsible `<details>` with "Answer given" (Markdown), and the user's comment as a gold left-bordered italic serif quote;
    - "SOURCES USED", each with "View" and "**Fix**" buttons. Fix switches to the Documents tab and opens that document in the editor, or the Replace dialog if it isn't editable;
    - an admin-note textarea, a "Save note" button (shown when the note has changed), and "Mark resolved" (primary) or "Reopen".
  - Empty state: "All caught up — no open “not helpful” ratings."
- **Documents** (`DocumentsManager`):
  - An **upload card** with File (max 25 MB, with a styled file button), Category (a select of the existing categories plus "New category…", which reveals a text input), an optional Name, a "Replace if it exists" checkbox and an "Upload" primary button.
  - Success and error notices.
  - A **table card** with a search box and a category select, plus the columns Document (title and monospace file name), Category, Type, Size, Chunks, Search index (badges: ready = success, queued or indexing = warning, error = danger with the detail as its title, not indexed = warning) and Actions (View, Edit for txt/md/csv only, Rename, Replace, and Delete as a danger button with a confirm dialog explaining that the file moves to `backend/trash/`).
  - **While any document is queued or indexing, poll the list every 2 s.**
  - **Modal** (`animate-rise`, backdrop `bg-black/40 backdrop-blur-[2px]`, Esc closes it):
    - **Edit:** a full-height monospace textarea, with format hints ("Lines like == Heading == become sections", "# and ## headings become sections" or "The first row holds the column names"), the character count, and Save.
    - **Rename:** category and name fields, with the warning "Old links to this document will stop working."
    - **Replace:** a file input restricted to the same extension.
  - After any change, reload the documents and the stats.

### C5.6 Accessibility and responsiveness checklist
- Every icon-only button has an `aria-label` and a `title`.
- Visible focus rings (`:focus-visible` uses the accent outline).
- `prefers-reduced-motion` turns off the animations and hover transforms.
- The text contrast passes in both themes.
- Layouts work from **360px phones to 1440px+ desktops**.
- **There is no horizontal page scroll**, and the **auth pages and the empty chat panel never need vertical scrolling**.

---

# PART D — EVALUATION, README AND BUILD ORDER

## D1. Evaluation — `eval/`
- **`testset.json`: 50 questions.** Write them from randomly sampled passages of the actual documents, and check each one against the text:
  - **40 facts:** 5 per category, plus one from each non-txt format sample (PDF, slides, Word, CSV, Excel, Markdown).
  - **4 follow-ups:** a two-turn conversation where the second question depends on the first, e.g. "Who were its astronauts?".
  - **6 unanswerable:** topics verified to be absent from the documents.
  - Each item is `{id, type: "fact"|"followup"|"unanswerable", turns: [...], gold: [article stems], reference, facts: [[accepted spellings], ...]}`.
- **`run_eval.py`**, with sub-commands `retrieval`, `answers` and `speed`, writing JSON results to `eval/results/`:
  - **retrieval:** call `/api/search` with top_k 10 and compute **Hit@1, Hit@3, Hit@5, Hit@10 and MRR**. A hit is any chunk whose source's article stem is in `gold`, so format copies count.
  - **answers:** log in, run every question through the **real streamed chat**, and grade it:
    - the key-fact check (every fact group must match one spelling, case-insensitively);
    - unanswerable questions must match a refusal pattern (such as "not contain", "no information", "cannot" or "not mentioned");
    - follow-ups run in the same conversation.
  - **speed:** search latency p50 and p95 over many queries, time to the first token, total time and words per second for single-user answers, and a **4 simultaneous users** test reporting errors and average and maximum wait.
- Write `eval/REPORT.md` with a summary table and notes on each miss.
- **Targets:** Hit@10 ≥ 95%, MRR ≥ 0.9, ≥ 85% of answers fully correct, 0 invented facts, and 100% of unanswerable questions refused.

## D2. README.md
Include:
- what the project is and its architecture;
- requirements (Python 3.12, Node.js 20.9+, PostgreSQL 14+, Ollama or an LLM API key, optional LibreOffice, ~8 GB RAM);
- **one-time setup:**
  1. create a venv and install requirements;
  2. copy `.env.example` to `.env` and fill it in (generate a JWT secret);
  3. run `setup_db.sql` with your own password;
  4. pull the model, `ollama pull qwen2.5:1.5b`, or set `LLM_PROVIDER=openai` with your key;
  5. run `npm install` in `frontend/`;
  6. run `python main.py` to build the index;
- **running it**, in three terminals: `ollama serve`; `cd backend && ../.venv/bin/uvicorn app.main:app --port 8000`; `cd frontend && npm run dev`. Then open http://localhost:3000;
- how email works (the outbox when SMTP is empty, with a Gmail app-password example);
- how to make an admin (`make_admin.py`);
- an API table;
- tuning settings (`TOP_K`, `HYBRID`, `RERANK`, `CANDIDATES`);
- **production notes:** `COOKIE_SECURE=true` over HTTPS, fresh secrets, a reverse proxy, and rate limiting on `/api/auth/*` and `/api/chat`.

## D3. Build order — stop after each phase and wait for "continue"
1. **Loaders and indexing:** `loaders.py`, `main.py`, plus a tiny CLI to run a test search.
2. **Retrieval pipeline:** `lexical.py`, `llm.py`, `rag.py`, plus a CLI that asks one question and streams the answer.
3. **Backend core:** config, databases, models, security, mailer, the auth router and the documents router.
4. **Chat API:** the chat router with SSE, history, feedback and follow-ups.
5. **Admin API:** the admin router, `indexer.py` and `make_admin.py`.
6. **Frontend foundation:** project setup, `globals.css`, fonts, the theme script and toggle, icons, the route guard, the API client, and the auth pages (verify they don't scroll at a 600px window height).
7. **Library home and document reader:** the site layout, header, footer, back-to-top, `DocArt`, `DataTable`, the home page and the document page.
8. **Chat widget:** the full chat panel.
9. **Admin panel.**
10. **Evaluation and README.**

## D4. Final acceptance checklist
- [ ] Registering, verifying the email (link from the outbox), logging in, the forgot/reset password flow and logging out all work. A reset signs out other sessions.
- [ ] Signed-out users are redirected to `/login?next=…` and return to the right page after logging in.
- [ ] The library lists every document, with working search (and the `/` shortcut), subject tiles, chips, format filters with counts, sorting and skeletons.
- [ ] The reader shows the banner, portrait cover, drop cap, table of contents with the active section, progress bar and download. Spreadsheets render as tables.
- [ ] Chat streams answers with sources that link to the exact section. It refuses when the documents lack the answer, offers follow-ups, ratings, history, delete, PDF export and Stop, and opens left of the launcher at full height without scrolling.
- [ ] Admins see stats, the chart, users (counts only), feedback triage with Fix, and document upload/edit/rename/replace/delete with live index status. Non-admins get a 403 from every `/api/admin/*` route.
- [ ] The day/night toggle has no flash on reload, remembers the choice and follows the OS until one is made.
- [ ] Reduced motion is respected, keyboard focus is visible and the layout works on phones.
- [ ] No secrets are in the code; everything comes from `.env`.
