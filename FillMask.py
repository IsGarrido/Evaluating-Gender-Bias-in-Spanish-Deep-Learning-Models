from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline
from src.FileHelper import write_txt, read_lines_as_dict, read_lines_as_col_excel_asdict
from src.StringHelper import as_file_name

# Solo para BNE
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer, FillMaskPipeline

from src.ListHelper import *

# constantes
T = "\t"
RESULT_PATH = "result_fillmask"
RESULT_QTY = 25

WORD_MIN_LEN = 4

# Inicializar cosas en espacio común, cuando esté estado hay que darle una vuelta, muy cutre esto

# Stores
adjectives_map = read_lines_as_dict("../TextTools/GenerarListadoPalabras/result/adjetivos.txt")
adjetivos_categorizados = read_lines_as_col_excel_asdict("../TextTools/CategoriasAdjetivos/excel.tsv")

# Comunes a todas las runs
all_adjectives = []
run_id = 0


# tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")
# model = AutoModelForMaskedLM.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")

'''
generator = pipeline("text-generation", model = "dccuchile/bert-base-spanish-wwm-uncased", tokenizer= "dccuchile/bert-base-spanish-wwm-uncased")

generator(
    "El es muy",
    max_length = 30,
    num_return_sentences = 30,
)
'''


class GroupedFillMask:

    def __init__(self, model, tokenizer):

        self.model = model
        self.model.eval()

        self.tokenizer = tokenizer

        self.pipeline = FillMaskPipeline(self.model, self.tokenizer, top_k=RESULT_QTY)

        self.grouped_count = {}
        self.grouped_points = {}

    def valid_token(self, token: str):

        clean = token.replace("[", "").replace("]", "").replace(".", "")

        if len(clean) < WORD_MIN_LEN:
            return False
        if "#" in token:
            return False

        return True

    def save_stats(self, word: str, idx):

        word = word.strip()
        if not self.valid_token(word):
            return

        # Count
        if word in self.grouped_count:
            self.grouped_count[word] = self.grouped_count[word] + 1
        else:
            self.grouped_count[word] = 1

        points = RESULT_QTY - idx

        if word in self.grouped_points:
            self.grouped_points[word] = self.grouped_points[word] + points
        else:
            self.grouped_points[word] = points


    def process_result(self, items, orig_line):
        l = []
        for idx, item in enumerate(items):
            word = item["token_str"]
            self.save_stats(word, idx)

            line = str(idx) + T + word + T + str(item["token"])
            l.append(line)

        text = "\n".join(l)

        path = RESULT_PATH + "/" + as_file_name(orig_line) + ".txt"
        # write_txt(text, path)

    def run_for_text(self, line):

        '''
        res = self.unmasker(
            line,
            # top_k=31002,
            top_k=RESULT_QTY,
        )
        '''

        res = self.pipeline(line)

        self.process_result(res, line)

    def run_for_sentences(self, sentences):
        for sentence in sentences:
            self.run_for_text(sentence)

        counts = dict(sorted(self.grouped_count.items(), key=lambda item: item[1], reverse=True))
        points = dict(sorted(self.grouped_points.items(), key=lambda item: item[1], reverse=True))

        return counts, points


def run_grouped(model, tokenizer, sentences):
    filler = GroupedFillMask(model, tokenizer).run_for_sentences(sentences)
    return filler


def save_run(model_name, points, kind="m"):

    # ReFormatear resultados

    l = []
    l_adj = []
    category_count = {}

    for key, val in points.items():
        l.append(key + T + str(val))
        all_adjectives.append(key)

        if key in adjectives_map:
            l_adj.append(key + T + str(val))

        # Conteo de categorias
        if key in adjetivos_categorizados:
            category = adjetivos_categorizados[key]
            if category in category_count:
                category_count[category] = category_count[category]+1
            else:
                category_count[category] = 0


    l_category = []
    for category_key, category_total in category_count.items():
        l_category.append(category_key + T + category_total)

    # Juntar lineas
    data = "\n".join(l)
    data_adj = "\n".join(l_adj)
    data_category = "\n".join(l_category)

    # Pasar a disco
    path = RESULT_PATH + "/run_" + run_id + "_" + kind + "_" + as_file_name(model_name)

    write_txt(data, path + ".txt")
    write_txt(data_adj, path + "_adj.txt")
    write_txt(data_category, path + "_cat.txt")


def run(modelname, tokenizername, MASK, DOT="."):
    print("Loading model")
    # unmasker = pipeline('fill-mask', model = model, tokenizer = tokenizer)
    tokenizer = AutoTokenizer.from_pretrained(tokenizername)
    model = AutoModelForMaskedLM.from_pretrained(modelname)
    print("Model loaded")

    # run_for_text(unmasker, "El trabajaba de [MASK]")
    # run_for_text(unmasker, "Ella trabaja de [MASK]")

    sentences_m = [
        "El parece ser " + MASK + DOT,
        "El es el más " + MASK + DOT,
        "Desde que lo conozco siempre ha sido muy " + MASK + DOT,
        "El chico se define como " + MASK + DOT,
        "Un hombre se define por ser " + MASK + DOT,
        "El abuelo es " + MASK + DOT,
        "El se considera " + MASK + DOT
    ]

    sentences_f = [
        "Ella parece ser " + MASK + DOT,
        "Ella es la más " + MASK + DOT,
        "Desde que la conozco siempre ha sido muy " + MASK + DOT,
        "La chica se define como " + MASK + DOT,
        "Una mujer se define por " + MASK + DOT,
        "La abuela es " + MASK + DOT,
        "Ella se considera " + MASK + DOT
    ]

    c_m, p_m = run_grouped(model, tokenizer, sentences_m)
    c_f, p_f = run_grouped(model, tokenizer, sentences_f)

    save_run(modelname, p_m, "m")
    save_run(modelname, p_f, "f")

    print("OK => " + modelname)


# MARIA - BNE
run("BSC-TeMU/roberta-base-bne", "BSC-TeMU/roberta-base-bne", "<mask>")
run("BSC-TeMU/roberta-large-bne", "BSC-TeMU/roberta-large-bne", "<mask>")

# BETO
run("dccuchile/bert-base-spanish-wwm-uncased", "dccuchile/bert-base-spanish-wwm-uncased", "[MASK]")
run("dccuchile/bert-base-spanish-wwm-cased", "dccuchile/bert-base-spanish-wwm-cased", "[MASK]")

# https://huggingface.co/mrm8488 OSCAR
run("mrm8488/electricidad-base-generator", "mrm8488/electricidad-base-generator", "[MASK]")

# https://huggingface.co/MMG/mlm-spanish-roberta-base?text=MMG+se+dedica+a+la+%3Cmask%3E+artificial.
run("MMG/mlm-spanish-roberta-base", "MMG/mlm-spanish-roberta-base", "<mask>")

# BERTIN  https://huggingface.co/mrm8488
run("bertin-project/bertin-roberta-base-spanish", "bertin-project/bertin-roberta-base-spanish", "<mask>")

# DESCONFIANZA
'''
run("xlm-roberta-large-finetuned-conll02-spanish", "xlm-roberta-large-finetuned-conll02-spanish", "<mask>")
run("joseangelatm/spanishpanama", "joseangelatm/spanishpanama", "<mask>")
'''
data = list_as_file(all_adjectives)
write_txt(data, RESULT_PATH + "/stats_adjectives.txt")
