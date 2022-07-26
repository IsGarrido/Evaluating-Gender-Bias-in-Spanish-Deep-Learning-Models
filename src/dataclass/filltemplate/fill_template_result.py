class FillTemplateResult:

    def __init__(self) -> None:
        self.data : 'list[dict[str,str]]'= []
        self.words: 'list[str]' = []
        self.other_words: 'list[str]' = []

    def add_all(self, words, unique_words, other_words):
        
        self.data.extend(words)
        self.words = unique_words
        self.other_words = other_words

