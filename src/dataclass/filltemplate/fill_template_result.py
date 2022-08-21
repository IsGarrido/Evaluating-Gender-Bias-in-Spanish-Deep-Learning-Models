class FillTemplateResult:

    def __init__(self) -> None:
        self.data : 'list[dict[str,str]]'= []
        self.words: 'list[str]' = []
        self.sentences: 'dict[str, list[str]]' #  { m: [ 29 ], f: [29] }
        self.models: 'list[str]'

    def add_all(self, words, unique_words, templates, models):
        
        self.data.extend(words)
        self.words = unique_words
        self.sentences = templates
        self.models = models

