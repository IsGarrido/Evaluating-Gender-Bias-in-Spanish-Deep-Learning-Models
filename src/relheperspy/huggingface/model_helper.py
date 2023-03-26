from transformers import AutoTokenizer, AutoModelForMaskedLM

from relhelperspy.primitives.annotations import log_time

class HuggingFaceModelHelper:

    def __init__(self) -> None:
        pass

    @staticmethod
    def load_model(name: str):
        return HuggingFaceModelHelper.load_modal(name, name)

    @log_time
    @staticmethod
    def load_model(model_name: str, tokenizer_name: str):
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        model = AutoModelForMaskedLM.from_pretrained(model_name).to('cuda')
        model.eval()
        return (model, tokenizer)

    @staticmethod
    def lower(line: str) -> str:
        return line.lower().replace("[mask]", "[MASK]")
