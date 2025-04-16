import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class JsonlSemanticRetriever:
    def __init__(self, jsonl_path, index_path="vector_store/jsonl.index", model_name='all-MiniLM-L6-v2'):
        self.jsonl_path = jsonl_path
        self.index_path = index_path
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []

        self.load_or_create_index()

    def load_or_create_index(self):
        if os.path.exists(self.index_path) and os.path.exists("vector_store/texts.npy"):
            self.index = faiss.read_index(self.index_path)
            self.texts = np.load("vector_store/texts.npy", allow_pickle=True).tolist()
        else:
            self._build_index()

    def _build_index(self):
        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                if "question" in data and "answer" in data:
                    self.texts.append(f"Q: {data['question']}\nA: {data['answer']}")

        embeddings = self.model.encode(self.texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        os.makedirs("vector_store", exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        np.save("vector_store/texts.npy", self.texts)

    def retrieve(self, query, k=3):
        query_vec = self.model.encode([query]).astype("float32")
        D, I = self.index.search(query_vec, k)
        return [self.texts[i] for i in I[0]]
