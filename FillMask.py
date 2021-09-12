from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline

from src.DateHelper import FechaHoraTextual
from src.FileHelper import write_txt, read_lines_as_dict, read_lines_as_col_excel_asdict, read_pared_tsv
from src.FillMaskUtils.GroupedFillMask import GroupedFillMask
from src.FillMaskUtils.RunResult import RunResult
from src.StatisticalAnalysis import run_tests_labeled
from src.StringHelper import as_file_name
from src.FillMaskUtils.CategorizacionConfig import CategorizacionConfig

# Solo para BNE
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer, FillMaskPipeline

from src.ListHelper import *


cat_config_ismael = CategorizacionConfig("result_fillmask/categorias_ismael", "../TextTools/CategoriasAdjetivos/excel_ismael.tsv")
cat_config_polaridad_visibilidad = CategorizacionConfig("result_fillmask/categorias_polaridad_visibilidad", "../TextTools/CategoriasAdjetivos/polaridad_visibilidad.tsv")

cconfig = cat_config_polaridad_visibilidad

# constantes
T = "\t"
#RESULT_PATH = "result_fillmask/categorias_ismael"
RESULT_QTY = 25
TOTAL_CAT = "[_TOTAL]"
WORD_MIN_LEN = 4

# Inicializar cosas en espacio común, cuando esté estado hay que darle una vuelta, muy cutre esto

# Stores
adjectives_map = read_lines_as_dict("../TextTools/GenerarListadoPalabras/result/adjetivos.txt")

if cconfig.categories_ready:
    adjetivos_categorizados = read_lines_as_col_excel_asdict(cconfig.categories_source_file)
    adjetivos_categorias = list_unique(list(adjetivos_categorizados.values())) # Bastante bruto esto
else:
    adjetivos_categorizados = {}
    adjetivos_categorias = []

# Comunes a todas las runs
all_filling_words = []
all_filling_adjectives = []
run_id = 0

run_results = []

'''
generator = pipeline("text-generation", model = "dccuchile/bert-base-spanish-wwm-uncased", tokenizer= "dccuchile/bert-base-spanish-wwm-uncased")

generator(
    "El es muy",
    max_length = 30,
    num_return_sentences = 30,
)
'''

def run_grouped(model, modelname, tokenizer, sentences):
    filler = GroupedFillMask(model, modelname, tokenizer, cconfig.RESULT_PATH, RESULT_QTY).run_for_sentences(sentences)
    return filler


def save_run(model_name, points, kind="m"):

    # ReFormatear resultados

    l = []
    l_adj = []
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
            l_adj.append(key + T + str(val))
            all_filling_adjectives.append(key)

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
    l_adj.sort()
    l_category.sort()

    # Añadir cabeceras
    l_category.insert(0, "[CAT]" + T + "Count" + T + "PRC_Count" + T + "Points" + T + "PRC_points")

    # Juntar lineas
    data = "\n".join(l)
    data_adj = "\n".join(l_adj) + "\n" + FechaHoraTextual()
    data_category = "\n".join(l_category)

    # Pasar a disco
    path = cconfig.RESULT_PATH + "/run_" + str(run_id) + "_" + kind + "_" + as_file_name(model_name)

    write_txt(data, path + ".csv")
    write_txt(data_adj, path + "_adj.csv")
    write_txt(data_category, path + "_cat.csv")

    return dict_results

def run_global_stats():
    #run_results
    # adjetivos_categorias

    models =    [x[0] for x in run_results]
    m_result_tables = [x[1] for x in run_results]
    f_result_tables = [x[2] for x in run_results]
    attrs = ['count', 'prc_count', 'points', 'prc_points']

    # Quiero buscar correlaciones para TODOS los attributos njumericos
    for attr in attrs:

        # La correlación se busca para cada categoría
        for cat in adjetivos_categorias:
            l_before = []
            l_after = []
            l_model = []

            # Para cada par de tablas de resultados, buscamos correlaciones para el attributo ATTR
            for idx, val in enumerate(m_result_tables):

                m_result_table = m_result_tables[idx]
                f_result_table = f_result_tables[idx]
                l_model.append(models[idx])

                m_result_cat = m_result_table[cat]
                f_result_cat = f_result_table[cat]

                val_m = getattr(m_result_cat, attr)
                val_f = getattr(f_result_cat, attr)

                l_before.append(val_m)
                l_after.append(val_f)

            result_text = run_tests_labeled(l_before, l_after)

            posfix = as_file_name(cat)  + "_" + str(attr)

            # Escribir listas para posterior revisión
            data_m = list_as_file(list_as_str_list(l_before))
            write_txt(data_m, cconfig.RESULT_PATH + "/stats_source_" + posfix + "_m.txt")
            data_f = list_as_file(list_as_str_list(l_after))
            write_txt(data_f, cconfig.RESULT_PATH + "/stats_source_" + posfix + "_f.txt")

            l_both = []
            for idx, val in enumerate(l_before):
                m_val = l_before[idx]
                f_val = l_after[idx]
                modelname = l_model[idx]
                arrow = ">" if m_val > f_val else "<"
                l_both.append( str(m_val) + T + arrow + T + str(f_val) + T + modelname)

            str_both_l = list_as_str_list(l_both)
            str_both_l.insert(0, "[MASC]" + T + " " + T + "[FEM]" + T + "[model_name]")
            str_both_l.insert(0, "")
            str_both_l.insert(0, "")
            str_both_l.insert(0, as_file_name(cat) + "," + str(attr))

            data_both = list_as_file(str_both_l, False)

            write_txt(data_both, cconfig.RESULT_PATH + "/stats_both_" + posfix + ".csv")

            # Escribir resultado
            path = cconfig.RESULT_PATH + "/stats_result_" + posfix + ".txt"
            write_txt(result_text, path )

def run(modelname, tokenizername, MASK, sentences):
    print("Loading model")

    tokenizer = AutoTokenizer.from_pretrained(tokenizername)
    model = AutoModelForMaskedLM.from_pretrained(modelname)
    print("Model loaded")

    # run_for_text(unmasker, "El trabajaba de [MASK]")
    # run_for_text(unmasker, "Ella trabaja de [MASK]")

    sentences_m = [sentence[0].replace("[MASK]", MASK) for sentence in sentences]
    sentences_f = [sentence[1].replace("[MASK]", MASK) for sentence in sentences]

    c_m, p_m = run_grouped(model, modelname, tokenizer, sentences_m)
    c_f, p_f = run_grouped(model, modelname, tokenizer, sentences_f)

    result_table_m = save_run(modelname, p_m, "m")
    result_table_f = save_run(modelname, p_f, "f")
    run_results.append((modelname, result_table_m, result_table_f))

    print("OK => " + modelname)

sentences = read_pared_tsv("./data/FillMask/sentences.tsv")
models = read_pared_tsv("./data/FillMask/models.tsv")

for model in models:
    run_id = model[0]
    run(model[1], model[2], model[3], sentences)

data = list_as_file(all_filling_words)
write_txt(data, cconfig.RESULT_PATH + "/summary_all_filling_words.csv")

data = list_as_file(all_filling_adjectives)
write_txt(data, cconfig.RESULT_PATH + "/summary_all_filling_adjectives.csv")

if cconfig.categories_ready:
    run_global_stats()
    adjetivos_sin_categorizar = filter( lambda adjetivo: not adjetivo in adjetivos_categorizados, all_filling_adjectives)
    data = list_as_file(adjetivos_sin_categorizar)
    write_txt(data, cconfig.RESULT_PATH + "/summary_adj_missing_category.csv")



