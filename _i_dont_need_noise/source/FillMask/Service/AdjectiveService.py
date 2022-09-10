import relhelperspy.io.read_helper as _read

class AdjectiveService:

    def __init__(self):
        self.adjective_dict = _read.read_as_dict("~/data/Adjectives/adjetivos.txt")

    def has(self, adjective):
        return adjective in self.adjective_dict
