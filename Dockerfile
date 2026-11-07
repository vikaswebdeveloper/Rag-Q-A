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

# Copy application directories
COPY backend /app/backend
COPY chromaDB /app/chromaDB
COPY data /app/data
COPY users.db /app/users.db
COPY userdata.db /app/userdata.db

# Default Hugging Face Spaces port is 7860
EXPOSE 7860

ENV PORT=7860
ENV CHROMA_PATH=/app/chromaDB
ENV DATA_DIR=/app/data
ENV USERS_DB_URL=sqlite:////app/users.db
ENV USERDATA_DB_URL=sqlite:////app/userdata.db

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]

