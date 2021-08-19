class ScorerConfig:

    type = 'simple'

    def __init__(self, index_masked_sentence_m, index_masked_sentence_f, index_target_value_m, index_target_value_f):
        self.index_masked_sentence_m = index_masked_sentence_m
        self.index_masked_sentence_f = index_masked_sentence_f
        # self.index_target_m = index_target_m
        # self.index_target_f = index_target_f
        self.index_target_value_m = index_target_value_m
        self.index_target_value_f = index_target_value_f
        self.type = 'simple'

