class SimpleTestResult:

    def __init__(self, test_uid, score_m, score_f, masked_sentence_m, masked_sentence_f, target_value_m, target_value_f):
        self.test_uid = test_uid
        self.score_m = score_m
        self.score_f = score_f
        self.masked_sentence_m = masked_sentence_m
        self.masked_sentence_f = masked_sentence_f
        self.target_value_m = target_value_m
        self.target_value_f = target_value_f
        self.type = 'simple'

    def as_dict(self):
        return {
            'type': self.type,
            'test_uid': self.test_uid,
            'score_m': self.score_m,
            'score_f': self.score_f,
            'masked_sentence_m': self.masked_sentence_m,
            'masked_sentence_f': self.masked_sentence_f,
            'target_value_m': self.target_value_m,
            'target_value_f': self.target_value_f
        }
