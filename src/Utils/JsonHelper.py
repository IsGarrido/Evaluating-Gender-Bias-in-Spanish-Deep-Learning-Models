import jsonpickle


class JsonHelper:

    @staticmethod
    def encode(obj):
        data = jsonpickle.encode(obj)
        return data

    @staticmethod
    def decode(json):
        obj = jsonpickle.decode(json)
        return obj