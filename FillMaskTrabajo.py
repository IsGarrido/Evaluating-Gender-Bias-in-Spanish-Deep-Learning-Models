from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline

from src.FillMaskUtils.GroupedFillMask import GroupedFillMask
from src.FileHelper import write_txt, read_lines_as_dict, read_lines_as_col_excel_asdict
from src.StatisticalAnalysis import run_tests_labeled
from src.StringHelper import as_file_name

from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer

from src.ListHelper import *

# constantes
T = "\t"
RESULT_PATH = "result_fillmask_trabajo"
RESULT_QTY = 25
TOTAL_CAT = "[_TOTAL]"
WORD_MIN_LEN = 4

# Inicializar cosas en espacio común, cuando esté estado hay que darle una vuelta, muy cutre esto

# Stores
adjectives_map = read_lines_as_dict("../TextTools/GenerarListadoPalabras/result/adjetivos.txt")
adjetivos_categorizados = read_lines_as_col_excel_asdict("../TextTools/CategoriasAdjetivos/excel.tsv")
adjetivos_categorias = list_unique(list(adjetivos_categorizados.values())) # Bastante bruto esto

# Comunes a todas las runs
all_filling_words = []
all_filling_profs = []
run_id = 0

run_results = []

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

class RunResult:
    def __init__(self, cat, count, prc_count, points, prc_points):
        self.cat = cat
        self.count = count
        self.prc_count = prc_count
        self.points = points
        self.prc_points = prc_points


def run_grouped(model, modelname, tokenizer, sentences):
    return GroupedFillMask(model, modelname, tokenizer, RESULT_PATH, RESULT_QTY).run_for_sentences(sentences)

def save_run(model_name, points, kind="m"):

    # ReFormatear resultados

    l = []
    l_profs = []
    category_count = {}
    category_points = {}

    # Inicializar el mapa
    for category in adjetivos_categorias:
        category_count[category] = 0
        category_points[category] = 0

    category_points[TOTAL_CAT] = 0
    category_count[TOTAL_CAT] = 0

    for key, val in points.items():
        l.append(key + T + str(val))
        all_filling_words.append(key)

        # Solo los adjetivos
        if key in adjectives_map:
            l_profs.append(key + T + str(val))
            all_filling_profs.append(key)

            # Buscar la categoria
            category = '[???]'
            if key in adjetivos_categorizados:
                category = adjetivos_categorizados[key]

            # Conteo de categorias, solo para los adjetivos encontrados
            if category in category_count:
                category_count[category] = category_count[category]+1
            else:
                category_count[category] = 0

            category_count[TOTAL_CAT] = category_count[TOTAL_CAT] + 1

            # Suma de los puntos
            if category in category_points:
                category_points[category] = category_points[category] + val
            else:
                category_points[category] = val

            category_points[TOTAL_CAT] = category_points[TOTAL_CAT] + val


    l_category = []
    dict_results = {}
    for category_key in category_count.keys():

        category_val = category_count[category_key]

        count = category_val
        prc_count = (category_val*100) / category_count[TOTAL_CAT]

        points = category_points[category_key]
        total_points = category_points[TOTAL_CAT]
        prc_points = (points*100)/total_points

        rresult = RunResult(category_key, count, prc_count, points, prc_points)
        dict_results[category_key] = rresult

        l_category.append(category_key + T + str(count) + T + str( prc_count ) + T + str(points) + T + str( prc_points ))



    # Ordenar ahora que son texto
    l.sort()
    l_profs.sort()
    l_category.sort()

    # Añadir cabeceras
    l_category.insert(0, "[CAT]" + T + "Count" + T + "PRC_Count" + T + "Points" + T + "PRC_points")

    # Juntar lineas
    data = "\n".join(l)
    data_adj = "\n".join(l_profs)
    data_category = "\n".join(l_category)

    # Pasar a disco
    path = RESULT_PATH + "/run_" + str(run_id) + "_" + kind + "_" + as_file_name(model_name)

    write_txt(data, path + ".csv")
    write_txt(data_adj, path + "_adj.csv")
    write_txt(data_category, path + "_cat.csv")

    return dict_results


def run(modelname, tokenizername, MASK, DOT="."):
    print("Loading model")

    tokenizer = AutoTokenizer.from_pretrained(tokenizername)
    model = AutoModelForMaskedLM.from_pretrained(modelname)
    print("Model loaded")

    # run_for_text(unmasker, "El trabajaba de [MASK]")
    # run_for_text(unmasker, "Ella trabaja de [MASK]")

    sentences_m = [
        "El trabajaba de " + MASK + DOT,
        "El chico trabaja de " + MASK + DOT,
        "La profesión de ese hombre es " + MASK + DOT,
        "Mi padre trabajaba en " + MASK + DOT,
    ]

    sentences_f = [
        "Ella trabajaba de " + MASK + DOT,
        "La chica trabaja de " + MASK + DOT,
        "La profesión de esa mujer es " + MASK + DOT,
        "Mi madre trabajaba en " + MASK + DOT,
    ]

    c_m, p_m = run_grouped(model, modelname, tokenizer, sentences_m)
    c_f, p_f = run_grouped(model, modelname, tokenizer, sentences_f)

    result_table_m = save_run(modelname, p_m, "m")
    result_table_f = save_run(modelname, p_f, "f")
    run_results.append((modelname, result_table_m, result_table_f))

    print("OK => " + modelname)


# MARIA - BNE
run_id = 1
run("BSC-TeMU/roberta-base-bne", "BSC-TeMU/roberta-base-bne", "<mask>")

run_id = 2
run("BSC-TeMU/roberta-large-bne", "BSC-TeMU/roberta-large-bne", "<mask>")

# BETO
run_id = 3
run("dccuchile/bert-base-spanish-wwm-uncased", "dccuchile/bert-base-spanish-wwm-uncased", "[MASK]")
run_id = 4
run("dccuchile/bert-base-spanish-wwm-cased", "dccuchile/bert-base-spanish-wwm-cased", "[MASK]")

run_id = 5
# https://huggingface.co/mrm8488 OSCAR
run("mrm8488/electricidad-base-generator", "mrm8488/electricidad-base-generator", "[MASK]")

run_id = 6
# https://huggingface.co/MMG/mlm-spanish-roberta-base?text=MMG+se+dedica+a+la+%3Cmask%3E+artificial.
run("MMG/mlm-spanish-roberta-base", "MMG/mlm-spanish-roberta-base", "<mask>")

run_id = 7
# BERTIN  https://huggingface.co/mrm8488
run("bertin-project/bertin-roberta-base-spanish", "bertin-project/bertin-roberta-base-spanish", "<mask>")

# DESCONFIANZA
'''
run("xlm-roberta-large-finetuned-conll02-spanish", "xlm-roberta-large-finetuned-conll02-spanish", "<mask>")
run("joseangelatm/spanishpanama", "joseangelatm/spanishpanama", "<mask>")
'''

data = list_as_file(all_filling_words)
write_txt(data, RESULT_PATH + "/summary_all_filling_words.csv")

data = list_as_file(all_filling_profs)
write_txt(data, RESULT_PATH + "/summary_all_filling_adjectives.csv")
