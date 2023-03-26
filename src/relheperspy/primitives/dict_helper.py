class DictHelper:

    @staticmethod
    def exclude_key(d, keys):
        return {x: d[x] for x in d if x not in keys}

    @staticmethod
    def as_lookup(d: 'dict[str, list[str]]') -> 'dict[str, str]':
        
        res: dict[str, str] = {}

        for key in d:
            items: list[str] = d[key]
        
            for item in items:
                res[item] = key

        return res

    @staticmethod
    def keys(d: 'dict') -> 'list[str]':
        return list(d.keys())