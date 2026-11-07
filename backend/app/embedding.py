from functools import lru_cache
from typing import Optional
from chromadb import Documents, EmbeddingFunction, Embeddings
from fastembed import TextEmbedding

from backend.app.config import settings


class FastEmbedEmbeddingFunction(EmbeddingFunction[Documents]):
    """ChromaDB compatible embedding function powered by FastEmbed (ONNX)."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or getattr(settings, "EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        self._model: Optional[TextEmbedding] = None

    def _get_model(self) -> TextEmbedding:
        if self._model is None:
            self._model = TextEmbedding(model_name=self.model_name)
        return self._model

    @staticmethod
    def name() -> str:
        return "fastembed"

    def __call__(self, input: Documents) -> Embeddings:
        model = self._get_model()
        return [vec.tolist() for vec in model.embed(input)]


@lru_cache(maxsize=1)
def get_embedding_function() -> FastEmbedEmbeddingFunction:
    """Singleton cached embedding function."""
    model_name = getattr(settings, "EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    return FastEmbedEmbeddingFunction(model_name=model_name)
