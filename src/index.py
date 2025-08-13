import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from .chunk import chunk_segments

class Indexer:
    def __init__(self, persist_dir="store", collection_name="episodes"):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir, settings=Settings(allow_reset=True))
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.persist_dir = persist_dir

    def add_episode(self, episode_id, audio_path, segments):
        chunks = chunk_segments(segments)
        texts = [c["text"] for c in chunks]
        metas = [{"episode": episode_id, "start_time": c["start"], "end_time": c["end"], "audio_path": audio_path} for c in chunks]
        ids = [f"{episode_id}:{i}" for i in range(len(chunks))]
        embs = self.embedder.encode(texts, normalize_embeddings=True).tolist()
        self.collection.add(ids=ids, documents=texts, metadatas=metas, embeddings=embs)

    def persist(self):
        pass

    def reset(self):
        self.client.reset()
        self.collection = self.client.get_or_create_collection("episodes")