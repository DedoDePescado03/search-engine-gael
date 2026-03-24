class InvertedIndex:
    """
    Index structure:
        {
            "python": {"doc1": 3, "doc5": 1}, "python" appears 3 times in doc1, 1 in doc5
            "engine": {"doc2": 2, "doc7": 4},
            ...
        }
    """

    def __init__(self):
        #Main index: term → {doc_id → frequency}
        self.index = {}

        #Length of each document in tokens: {doc_id → num_tokens}
        #Used by BM25 to normalize scores by document length.
        self.doc_lengths = {}

        #Total number of documents in the corpus
        self.N = 0

        #Average document length in tokens (required by BM25)
        self.avg_doc_len = 0

    def build(self, documents, processor):
        """
        Parameters:
            documents (list): List of dicts with keys "id", "title", "text".
            processor (TextProcessor): Instance of the text preprocessor.
        """
        total_length = 0
        self.N = len(documents)

        for doc in documents:
            doc_id = doc["id"]

            #Combine title and body to index all document content.
            text = doc["title"] + " " + doc["text"]

            #Process the text: tokenize -> remove stopwords -> stem
            tokens = processor.process(text)

            #Store the length of this document (in processed tokens)
            self.doc_lengths[doc_id] = len(tokens)
            total_length += len(tokens)

            #Count the frequency of each term in the document (term frequency)
            term_freq = {}
            for token in tokens:
                term_freq[token] = term_freq.get(token, 0) + 1

            #Add each term to the inverted index
            for term, freq in term_freq.items():
                if term not in self.index:
                    self.index[term] = {}

                #Record how many times this term appears in this document
                self.index[term][doc_id] = freq

        #Calculate the average corpus document length (used by BM25 for normalization)
        self.avg_doc_len = total_length / self.N