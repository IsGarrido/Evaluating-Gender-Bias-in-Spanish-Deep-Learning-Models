from __future__ import annotations
from src.Utils.HuggingHelper import HuggingHelper

class FillMaskModel:

    uid: int = 0

    def __init__(self, model: str, tokenizer: str, mask: str, cased):
        self.model = model
        self.tokenizer = tokenizer
        self.mask = mask
        self.cased = cased

    def with_uid(self, uid):
        self.uid = uid
        return self

    def get(self):
        return HuggingHelper.get_model(self.model, self.tokenizer)

    @staticmethod
    def from_tsv(s: list[str]) -> FillMaskModel:
        return FillMaskModel(s[1], s[2], s[3], s[4] == 'cased').with_uid(s[0])