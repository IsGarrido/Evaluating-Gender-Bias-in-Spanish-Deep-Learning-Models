class AdjectiveSummaryStat:

    def __init__(self, model, type, n_words, n_adjectives, n_results):
        self.model = model
        self.type = type
        self.n_words = n_words
        self.n_adjectives = n_adjectives
        self.n_results = n_results
        self.proportion = (n_adjectives / n_words) * 100
