from transformers import FillMaskPipeline

from src.FillMask.Vm.TaskResult import TaskResult


class FillMaskTask:

    def __init__(self, model, tokenizer, result_qty):

        self.model = model.to('cuda')
        self.model.eval()
        self.tokenizer = tokenizer

        self.pipeline = FillMaskPipeline(self.model, self.tokenizer, top_k=result_qty, device=self.model.device.index)

    def fill(self, line, mask = "[MASK]") -> TaskResult:

        if mask != "[MASK]":
            line = str.replace(line, "[MASK]", mask)

        model_res = self.pipeline(line)
        res = TaskResult.fromPipeline(self.model.name_or_path, line, model_res)
        return res

    def fill_sentences(self, sentences, mask = "[MASK]") -> list[TaskResult]:

        results = []
        for sentence in sentences:
           res = self.fill(sentence, mask)
           results.append(res)
        return results
