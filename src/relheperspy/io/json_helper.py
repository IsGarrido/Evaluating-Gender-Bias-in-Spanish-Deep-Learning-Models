import os
import jsonpickle

class JsonHelper:

    @staticmethod
    def encode(obj) -> str:
        data = jsonpickle.encode(obj)
        return data

    @staticmethod
    def decode(json):
        obj = jsonpickle.decode(json)
        return obj