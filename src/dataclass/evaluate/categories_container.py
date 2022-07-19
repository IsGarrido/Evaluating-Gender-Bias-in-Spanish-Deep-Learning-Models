class CategoriesContainer:

    def __init__(self, categories: 'list[str]' = None) -> None:
        
        if categories is None:
            categories = [CategoriesContainer.UnknownCategory()]

        self.categories = categories
        self.data : 'dict[str, list[dict[str,str]]]'= {}

        for category in categories:
            self.data[category] = []

    def UnknownCategory():
        return "unknown"

    def add_all(self, words, category = None):
        if category is None:
            category = CategoriesContainer.UnknownCategory()
        
        self.data[category].extend(words)

