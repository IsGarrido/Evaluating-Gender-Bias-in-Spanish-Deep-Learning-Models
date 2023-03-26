class ListHelper:
    def __init__(self) -> None:
        pass

    def unique(source:list, sort: bool = False):
        items = list(dict.fromkeys(source))

        if sort:
            items.sort()

        return items

    def list_as_file(source:list, sort: bool = True):
        items = ListHelper.unique(source, sort)
        return "\n".join(items)

    def list_as_str_list(source:list):
        return list(map(str, source))

    def apply( items: list, fn ):
        return [fn(item) for item in items]

