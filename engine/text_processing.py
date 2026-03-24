import re

class TextProcessor:
    """
    Responsible for cleaning and normalizing text before indexing or searching.
    Applies three steps in order: tokenization -> stopword removal -> stemming.
    """

    def __init__(self):
        self.stopwords = {
            "the","is","and","a","an","of","to","in","for","on",
            "with","at","by","from","up","about","into","over",
            "after","before","between","out","against","during",
            "without","within","along","following","across"
        }

    def tokenize(self, text):
        """
        1. Lowercases everything so "Python" and "python" map to the same token.
        2. Uses a regex to extract only alphanumeric sequences (\w+), ignoring punctuation, whitespace and special characters.
        """
        text = text.lower()
        tokens = re.findall(r"\b\w+\b", text)
        return tokens

    def remove_stopwords(self, tokens):
        return [t for t in tokens if t not in self.stopwords]

    def stem(self, tokens):
        """
        Applies basic stemming: strips common suffixes to reduce word variants
        to a shared root.

        Suffixes are checked in order; only the first match is stripped.
        A minimum root length is also enforced to avoid overly aggressive trimming.
        """
        suffixes = ["ing", "edly", "edly", "ed", "ly", "ment", "es", "s"]
        stemmed_tokens = []

        for token in tokens:
            for suffix in suffixes:
                #Only strip if the token ends with the suffix AND
                #the resulting root is long enough
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