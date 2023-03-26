class FillMaskHelper:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def to_lower_but_mask(sentence: str) -> str:
        return sentence.lower().replace("[mask]", "[MASK]")
    
    def to_robert_mask(sentence: str) -> str:
        return sentence.replace("[MASK]", '<mask>')