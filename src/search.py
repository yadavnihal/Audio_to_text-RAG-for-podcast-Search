import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class QueryEngine:
    def __init__(self, persist_dir="store", collection_name="episodes"):
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(path=persist_dir, settings=Settings(allow_reset=True))
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def refresh(self):
        self.client = chromadb.PersistentClient(path=self.persist_dir, settings=Settings(allow_reset=True))
        self.collection = self.client.get_or_create_collection("episodes")

    def search(self, query, top_k=5):
        q = self.embedder.encode([query], normalize_embeddings=True).tolist()
        res = self.collection.query(query_embeddings=q, n_results=top_k, include=["documents","metadatas"])
        out = []
        if res and res.get("documents"):
            docs = res["documents"][0]
            mets = res["metadatas"][0]
            for d, m in zip(docs, mets):
                out.append({"text": d, "metadata": m})
        return out