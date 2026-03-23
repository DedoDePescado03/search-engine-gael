class InvertedIndex:

    def __init__(self):
        self.index = {}
        self.doc_lengths = {}
        self.N = 0
        self.avg_doc_len = 0


    def build(self, documents, processor):
        total_length = 0
        self.N = len(documents)

        for doc in documents:

            doc_id = doc["id"]

            text = doc["title"] + " " + doc["text"]

            tokens = processor.process(text)

            self.doc_lengths[doc_id] = len(tokens)

            total_length += len(tokens)

            term_freq = {}

            for token in tokens:
                term_freq[token] = term_freq.get(token, 0) + 1

            for term, freq in term_freq.items():
                if term not in self.index:
                    self.index[term] = {}

                self.index[term][doc_id] = freq

        self.avg_doc_len = total_length / self.N