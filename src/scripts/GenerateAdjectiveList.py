from nltk import download
from nltk.corpus import cess_esp

from relhelpers.io.write_helper import WriteHelper as _write
from relhelpers.primitives.list_helper import ListHelper as _list
from relhelpers.io.project_helper import ProjectHelper as _project


# https://github.com/zelliott/maple/blob/11cfe6889e22e89715f91270bd854762574a8cd6/models/build_models.py
# https://sites.google.com/view/programacion-en-python/home/5-etiquetado-morfosint%C3%A1tico

class GenerateAdjectiveList:

    def __init__(self) -> None:
        download('cess_esp')
        adjetivos_tagged = list(filter(len, [word + "\t" + tag if tag.startswith("a") else "" for (word,tag) in cess_esp.tagged_words()]))
        adjetivos = list(filter(len, [word if tag.startswith("a") else "" for (word,tag) in cess_esp.tagged_words()]))

        path_adjectives = _project.data_path("adjectives", "cess_spanish_adjectives.json")
        path_adjectives_tagged = _project.data_path("adjectives", "cess_spanish_adjectives_tagged.json")

        _write.json(self.normalize(adjetivos), path_adjectives)
        _write.json(self.normalize(adjetivos_tagged), path_adjectives_tagged)


    def normalize(self, items):
        items = [item.lower() for item in items]
        items = _list.unique(items, True)
        return items


GenerateAdjectiveList()