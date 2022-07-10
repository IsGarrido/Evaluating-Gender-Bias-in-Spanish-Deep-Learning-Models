from dataclasses import dataclass

@dataclass(frozen=True)
class ModelConfig(object):

    id: int
    name: str
    tokenizer: str
    mask: str
    cased: bool