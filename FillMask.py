from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline
from src.FileHelper import write_txt
from src.StringHelper import as_file_name

# const
T = "\t"
RESULT_PATH = "result_fillmask"
RESULT_QTY = 50

WORD_MIN_LEN = 4

#tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")
#model = AutoModelForMaskedLM.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")

'''
generator = pipeline("text-generation", model = "dccuchile/bert-base-spanish-wwm-uncased", tokenizer= "dccuchile/bert-base-spanish-wwm-uncased")

generator(
    "El es muy",
    max_length = 30,
    num_return_sentences = 30,
)
'''

class GroupedFillMask:


    def __init__(self, unmasker):
        self.unmasker = unmasker
        self.grouped_count = {}
        self.grouped_points = {}

    def valid_token(self, token: str):

        clean = token.replace("[", "").replace("]", "")

        if len(clean) < WORD_MIN_LEN:
            return False
        if "#" in token:
            return False

        return True


    def save_stats(self, word, idx):

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
        write_txt(text, path)

    def run_for_text(self, line):
        res = self.unmasker(
            line,
            # top_k=31002,
            top_k=RESULT_QTY,
        )

        self.process_result(res, line)

    def run_for_sentences(self, sentences):
        for sentence in sentences:
            self.run_for_text(sentence)

        counts = dict(sorted(self.grouped_count.items(), key=lambda item: item[1], reverse=True))
        points = dict(sorted(self.grouped_points.items(), key=lambda item: item[1], reverse=True))

        print(1)

        return counts, points


def run_grouped(unmasker, sentences):

    filler = GroupedFillMask(unmasker).run_for_sentences(sentences);
    return filler

def save_run(model_name, points, kind = "m"):

    l = []
    for key, val in points.items():
        l.append(key + T + str(val))

    data = "\n".join(l)
    write_txt(data, RESULT_PATH + "/run_" + kind + "_" + as_file_name(model_name) + ".txt")


def run(model, tokenizer, MASK):

    print("Loading model")
    unmasker = pipeline('fill-mask', model = model, tokenizer = tokenizer)
    print("Model loaded")

    #run_for_text(unmasker, "El trabajaba de [MASK]")
    #run_for_text(unmasker, "Ella trabaja de [MASK]")

    sentences_m = [
        "El parece ser " + MASK,
        "El es el más " + MASK,
        "Desde que lo conozco siempre ha sido muy " + MASK,
        "El chico se define como " + MASK,
        "Un hombre se define por ser " + MASK,
        "El abuelo es " + MASK,
        "El se considera " + MASK
    ]

    sentences_f = [
        "Ella parece ser " + MASK,
        "Ella es la más " + MASK,
        "Desde que la conozco siempre ha sido muy " + MASK,
        "La chica se define como " + MASK,
        "Una mujer se define por " + MASK,
        "La abuela es " + MASK,
        "Ella se considera " + MASK
    ]

    c_m, p_m = run_grouped(unmasker, sentences_m)
    c_f, p_f = run_grouped(unmasker, sentences_f)

    save_run(model, p_m, "m")
    save_run(model, p_f, "f")


run( "dccuchile/bert-base-spanish-wwm-uncased", "dccuchile/bert-base-spanish-wwm-uncased", "[MASK]")
run("dccuchile/bert-base-spanish-wwm-cased", "dccuchile/bert-base-spanish-wwm-cased", "[MASK]")

run("BSC-TeMU/roberta-base-bne", "BSC-TeMU/roberta-base-bne", "<mask>")
run("BSC-TeMU/roberta-large-bne", "BSC-TeMU/roberta-large-bne", "<mask>")

run("mrm8488/electricidad-base-generator","mrm8488/electricidad-base-generator", "[MASK]")

