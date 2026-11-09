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

# Copy application files, data, pre-indexed vectors, and scripts
COPY backend /app/backend
COPY data /app/data
COPY chromaDB /app/chromaDB
COPY main.py /app/main.py

ENV PYTHONPATH=/app
ENV PORT=8000
ENV CHROMA_PATH=/app/chromaDB
ENV DATA_DIR=/app/data

EXPOSE 8000

# Use Render's dynamic $PORT
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
