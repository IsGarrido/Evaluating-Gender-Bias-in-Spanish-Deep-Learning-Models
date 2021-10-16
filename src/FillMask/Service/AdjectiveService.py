from src.Utils.FileReaderHelper import FileReaderHelper


class AdjectiveService:

    def __init__(self):
        self.adjective_dict = FileReaderHelper.read_as_dict("~/data/Adjectives/adjetivos.txt")

    def has(self, adjective):
        return adjective in self.adjective_dict
