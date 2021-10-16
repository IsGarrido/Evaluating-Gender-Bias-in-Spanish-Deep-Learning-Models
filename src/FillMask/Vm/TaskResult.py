from __future__ import annotations
from src.FillMask.Vm.TaskPrediction import TaskPrediction


class TaskResult:

    model:str
    sentence:str
    predictions:list[TaskPrediction]
    type:str = "undefined"

    def __init__(self, model:str, sentence:str, predictions:list[TaskPrediction]):
        self.model = model
        self.sentence = sentence
        self.predictions = predictions

    def withType(self, type):
        self.type = type
        return self

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

    def __str__(self):
        return dir(self)