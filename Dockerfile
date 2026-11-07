FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application and data corpus
COPY backend /app/backend
COPY data /app/data

EXPOSE 8000

ENV PORT=8000
ENV CHROMA_PATH=/app/chromaDB
ENV DATA_DIR=/app/data
ENV USERS_DB_URL=sqlite:////app/users.db
ENV USERDATA_DB_URL=sqlite:////app/userdata.db

# Use Render's dynamic $PORT
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
