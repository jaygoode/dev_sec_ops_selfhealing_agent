import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self, persist_dir=".memory"):
        self.client = chromadb.Client(
            chromadb.config.Settings(persist_directory=persist_dir
        ))

        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.remediation = self.client.get_or_create_collection(
            name="remediation_patterns",
            embedding_function=self.embedder
        )

        self.failures = self.client.get_or_create_collection(
            name="failure_memory",
            embedding_function=self.embedder
        )
        