class RunResult:
    def __init__(self, cat, count, prc_count, retrieval_status_value, prc_retrieval_status_value, probability, prc_probability):
        self.cat = cat
        self.count = count
        self.prc_count = prc_count
        self.retrieval_status_value = retrieval_status_value
        self.prc_retrieval_status_value = prc_retrieval_status_value
        self.probability = probability
        self.prc_probability = prc_probability