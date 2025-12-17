from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .ingest import Chunk


class Retriever:
    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        self.texts = [c.text for c in chunks]

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.embeddings = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query: str, k: int = 3) -> List[Chunk]:
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.embeddings)[0]

        top_indices = scores.argsort()[-k:][::-1]
        return [self.chunks[i] for i in top_indices]
