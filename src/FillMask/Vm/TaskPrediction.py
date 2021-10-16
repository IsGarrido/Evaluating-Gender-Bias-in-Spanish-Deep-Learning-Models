class TaskPrediction:

    def __init__(self, token_str:str, token, score, index):
        self.token_str = token_str.strip()
        self.token = token
        self.score = score
        self.index = index