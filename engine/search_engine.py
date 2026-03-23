import json
import re
from .text_processing import TextProcessor
from .indexer import InvertedIndex
from .ranking import BM25


class SearchEngine:

    def __init__(self, corpus_path):
        with open(corpus_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        self.processor = TextProcessor()

        self.indexer = InvertedIndex()
        self.indexer.build(self.documents, self.processor)

        self.ranker = BM25(
            self.indexer.index,
            self.indexer.doc_lengths,
            self.indexer.avg_doc_len
        )

    def highlight_terms(self, text, query_words):
        for word in query_words:
            pattern = re.compile(rf"\b({word}\w*)\b", re.IGNORECASE)
            text = pattern.sub(r"<mark>\1</mark>", text)

        return text

    def search(self, query):
        tokens = self.processor.process(query)
        query_words = query.lower().split()
        ranked = self.ranker.score(tokens)

        results = []

        for doc_id, score in ranked:

            doc = next(d for d in self.documents if d["id"] == doc_id)

            results.append({
                "title": self.highlight_terms(doc["title"], query_words),
                "text": self.highlight_terms(doc["text"], query_words),
                "source": doc["source"],
                "score": round(score, 4)
            })

        return results