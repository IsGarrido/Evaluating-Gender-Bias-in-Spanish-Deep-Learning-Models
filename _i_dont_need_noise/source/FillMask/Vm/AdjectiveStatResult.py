class AdjectiveStatResult:

    def __init__(self, model, sentence, sentence_index, type, n_words, n_adjectives):
        self.model = model
        self.sentence = sentence
        self.sentence_index = sentence_index
        self.type = type
        self.n_words = n_words
        self.n_adjectives = n_adjectives
        self.proportion = (n_adjectives / n_words) * 100
