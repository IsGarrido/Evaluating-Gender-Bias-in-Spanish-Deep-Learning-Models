from __future__ import annotations
from src.FillMask.Vm.TaskPrediction import TaskPrediction


class TaskResult:

    model:str
    sentence:str
    predictions:list[TaskPrediction]
    type:str = "undefined"
    sentence_index:int = -1

    def __init__(self, model:str, sentence:str, predictions:list[TaskPrediction]):
        self.model = model
        self.sentence = sentence
        self.predictions = predictions

    def withType(self, type):
        self.type = type
        return self

    def first_n_predictions(self, n:int):
        return self.predictions[:n]

    @staticmethod
    def fromPipeline(model, sentence, predictions) -> TaskResult:

        prediction_items = []
        for index, prediction in enumerate(predictions):
            pred = TaskPrediction(prediction["token_str"], prediction["token"], prediction["score"], index)
            prediction_items.append(pred)

        return TaskResult(model, sentence, prediction_items)

    @staticmethod
    def assignTypes(type_list, result_list) -> list[TaskResult]:

        arr = []
        for index, result in enumerate(result_list):
            type = type_list[index]
            result.type = type
            arr.append(result)

        return arr

    @staticmethod
    def assignIndex(sentence_index, result_list) -> list[TaskResult]:

        arr = []
        for index, result in enumerate(result_list):
            result.sentence_index = sentence_index
            arr.append(result)

        return arr

    def __str__(self):
        return dir(self)