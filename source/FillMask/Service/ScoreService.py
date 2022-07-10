from src.FillMask.Vm.AdjectiveStatResult import AdjectiveStatResult
from src.FillMask.Vm.TaskPrediction import TaskPrediction
from src.FillMask.Vm.TaskResult import TaskResult

class ScoreService:

    def __init__(self):
        x = 0

    def get_stats_for_task(self, sentence_task: TaskResult, qty):
        predictions = sentence_task.first_n_predictions(qty)
        adjectives = filter(lambda prediction: prediction.is_adjective, predictions)
        n_words = len(predictions)
        n_adj = len(adjectives)

        res = AdjectiveStatResult(sentence_task.model, sentence_task.sentence, sentence_task.sentence_index, sentence_task.type, n_adj, n_words)
        return res


    def get_scores_for_sentence(self, sentence):
        predictions = sentence.predictions

    def get_score_for_sentence_task(self, task_sentences: 'dict[list[TaskPrediction]]'):
        for task_key in task_sentences:
            sentence = task_sentences[task_key]
            self.get_scores_for_sentence(sentence)

    def get_scores_for_model(self, model_predictions: 'dict[dict[list[TaskPrediction]]]'):
        for model_key in model_predictions:
            sentences = model_predictions[model_key]
            self.get_score_for_sentence_task(sentences)
