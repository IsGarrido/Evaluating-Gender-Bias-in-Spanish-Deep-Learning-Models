class CategorizacionConfig:

    def __init__(self, prefix, categories_source_file):
        self.prefix = prefix
        self.categories_source_file = categories_source_file
        self.categories_ready = categories_source_file != ''
        self.RESULT_PATH = self.prefix
