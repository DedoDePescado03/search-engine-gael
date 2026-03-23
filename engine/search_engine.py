import json
import re
from .text_processing import TextProcessor
from .indexer import InvertedIndex
from .ranking import BM25


class SearchEngine:
    """
    Initialization flow:
        corpus.json -> TextProcessor -> InvertedIndex -> BM25

    Search flow:
        query (str) -> TextProcessor -> BM25.score() -> results with highlighting
    """

    def __init__(self, corpus_path):
        """
        Indexing happens once when the Flask server starts.
        Subsequent searches operate on the already-built in-memory index.

        Parameters:
            corpus_path (str): Path to the JSON file containing the corpus documents.
                               Expected format: list of dicts with keys id, title, text, source.
        """
        #Load all corpus documents into memory
        with open(corpus_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        #Initialize the text preprocessor
        self.processor = TextProcessor()

        #Build the inverted index over the entire corpus.
        self.indexer = InvertedIndex()
        self.indexer.build(self.documents, self.processor)

        #Initialize the BM25 ranker with data from index
        self.ranker = BM25(
            self.indexer.index,
            self.indexer.doc_lengths,
            self.indexer.avg_doc_len
        )

    def highlight_terms(self, text, query_words):
        """
        Wraps query terms in <mark> tags to highlight them in the UI.

        Regex with \b (word boundary) to highlight only whole words
        or words that start with the term (thanks to \w*).
        The re.IGNORECASE flag makes highlighting case-insensitive.
        """
        for word in query_words:
            pattern = re.compile(rf"\b({word}\w*)\b", re.IGNORECASE)
            text = pattern.sub(r"<mark>\1</mark>", text)

        return text

    def search(self, query):
        #(tokenize -> remove stopwords -> stem)
        tokens = self.processor.process(query)

        #Keep the original query words (without stemming) for highlighting,
        query_words = query.lower().split()

        #Documents ranked by BM25: list of (doc_id, score)
        ranked = self.ranker.score(tokens)

        results = []

        for doc_id, score in ranked:
            #Retrieve the full document by its ID
            #Linear scan: O(n) per result
            doc = next(d for d in self.documents if d["id"] == doc_id)

            results.append({
                "title": self.highlight_terms(doc["title"], query_words),
                "text": self.highlight_terms(doc["text"], query_words),
                "source": doc["source"],
                "score": round(score, 4)
            })

        return results