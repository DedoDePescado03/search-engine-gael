import re

class TextProcessor:

    def __init__(self):

        self.stopwords = {
            "the","is","and","a","an","of","to","in","for","on",
            "with","at","by","from","up","about","into","over",
            "after","before","between","out","against","during",
            "without","within","along","following","across"
        }

    def tokenize(self, text):
        text = text.lower()
        tokens = re.findall(r"\b\w+\b", text)

        return tokens


    def remove_stopwords(self, tokens):

        return [t for t in tokens if t not in self.stopwords]


    def stem(self, tokens):
        suffixes = ["ing", "edly", "edly", "ed", "ly", "ment", "es", "s"]
        stemmed_tokens = []

        for token in tokens:

            for suffix in suffixes:
                if token.endswith(suffix) and len(token) > len(suffix) + 2:
                    token = token[:-len(suffix)]
                    break

            stemmed_tokens.append(token)

        return stemmed_tokens


    def process(self, text):
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.stem(tokens)

        return tokens