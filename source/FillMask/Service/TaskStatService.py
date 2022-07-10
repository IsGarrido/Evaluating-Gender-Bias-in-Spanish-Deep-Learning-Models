from src.FillMask.Vm.AdjectiveStatResult import AdjectiveStatResult
from src.FillMask.Vm.TaskResult import TaskResult

class TaskStatService:

    def get_stats_for_task(self, sentence_task: TaskResult, qty):
        predictions = sentence_task.first_n_predictions(qty)
        adjectives = list(filter(lambda prediction: prediction.is_adjective, predictions))
        n_words = len(predictions)
        n_adj = len(adjectives)

        res = AdjectiveStatResult(sentence_task.model, sentence_task.sentence, sentence_task.sentence_index, sentence_task.type, n_words, n_adj)
        return res