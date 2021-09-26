class CategorizacionConfig:

    def __init__(self, prefix, categories_source_file, sentences_path, check_is_adjective):
        self.prefix = prefix
        self.categories_source_file = categories_source_file
        self.categories_ready = categories_source_file != ''
        self.RESULT_PATH = self.prefix
        self.sentences_path = sentences_path
        self.check_is_adjective = check_is_adjective
