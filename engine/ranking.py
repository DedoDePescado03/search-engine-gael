import math

class BM25:
    """
    Implements the BM25 (Best Match 25) ranking algorithm.

    BM25 is the industry standard for document ranking in search engines.
      - Frequency saturation: beyond a certain point, repeating a term more
        times in a document yields diminishing score increases.
      - Length normalization: penalizes very long documents that accumulate
        terms simply due to size, not relevance.

    f(t,d): frequency of term t in document d
    |d|: length of document d (in tokens)
    avgdl: average document length in the corpus
    k1: controls frequency saturation
    b: controls length normalization
    IDF(t): measures how rare the term is across the corpus
    """

    def __init__(self, index, doc_lengths, avg_doc_len):
        """
        Parameters:
            index (dict): Inverted index {term → {doc_id → frequency}}.
            doc_lengths (dict): Length of each document {doc_id → num_tokens}.
            avg_doc_len (float): Average document length across the corpus.
        """
        self.index = index
        self.doc_lengths = doc_lengths
        self.avg_doc_len = avg_doc_len

        #k1: Controls term frequency saturation.
        #Higher values give more weight to frequent terms.
        self.k1 = 1.5

        #b: Controls how much document length is penalized.
        self.b = 0.75

        #Total number of documents in the corpus
        self.N = len(doc_lengths)

    def score(self, query_tokens):
        """
        Calculates the BM25 score for all documents relevant to a query.

        Parameters:
            query_tokens (list): List of already-preprocessed query tokens.

        Returns:
            list: List of (doc_id, score) tuples sorted from highest to lowest score.
        """
        scores = {}  #Score accumulator per document: {doc_id -> total_score}

        for token in query_tokens:

            #If the term is not in the index, no document contains it
            if token not in self.index:
                continue

            postings = self.index[token]  #{doc_id -> frequency} for this term

            #number of documents containing the term
            df = len(postings)

            #IDF: rarer terms score higher.
            #The +1 prevents negative values for very common terms.
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)

            for doc_id, freq in postings.items():
                doc_len = self.doc_lengths[doc_id]

                #Term frequency with saturation applied
                numerator = freq * (self.k1 + 1)

                #Applies TF saturation and length normalization.
                denominator = freq + self.k1 * (
                    1 - self.b + self.b * (doc_len / self.avg_doc_len)
                )

                #Score for this token in this document
                score = idf * (numerator / denominator)

                #The final score is the sum of the scores for each query term
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += score

        #Sort results from highest to lowest score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return ranked