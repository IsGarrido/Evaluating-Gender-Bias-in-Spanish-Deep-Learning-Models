def list_unique(source:list, sort: bool = False):
    items = list(dict.fromkeys(source))

    if sort:
        items.sort()

    return items

def list_as_file(source:list):
    items = list_unique(source, True)
    return "\n".join(items)

