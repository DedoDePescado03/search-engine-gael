import math

class BM25:

    def __init__(self, index, doc_lengths, avg_doc_len):
        self.index = index
        self.doc_lengths = doc_lengths
        self.avg_doc_len = avg_doc_len

        self.k1 = 1.5
        self.b = 0.75

        self.N = len(doc_lengths)

    def score(self, query_tokens):
        scores = {}

        for token in query_tokens:

            if token not in self.index:
                continue

            postings = self.index[token]
            df = len(postings)
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)

            for doc_id, freq in postings.items():
                doc_len = self.doc_lengths[doc_id]

                numerator = freq * (self.k1 + 1)
                
                denominator = freq + self.k1 * (
                    1 - self.b + self.b * (doc_len / self.avg_doc_len)
                )

                score = idf * (numerator / denominator)

                if doc_id not in scores:
                    scores[doc_id] = 0

                scores[doc_id] += score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return ranked