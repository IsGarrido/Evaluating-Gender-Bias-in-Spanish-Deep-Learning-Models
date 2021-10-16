from transformers import AutoModelForMaskedLM, AutoTokenizer

class HuggingHelper:

    @staticmethod
    def lower(line: str) -> str:
        return line.lower().replace("[mask]", "[MASK]")

    @staticmethod
    def get_model(model_name, tokenizer_name):
        model = AutoModelForMaskedLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        return model, tokenizer
