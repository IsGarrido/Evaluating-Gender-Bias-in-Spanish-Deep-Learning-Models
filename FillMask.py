from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline

from src.DateHelper import FechaHoraTextual
from src.FileHelper import write_txt, read_lines_as_dict, read_lines_as_col_excel_asdict, read_paired_tsv, write_json
from src.FillMaskUtils.GroupedFillMask import GroupedFillMask
from src.FillMaskUtils.RunResult import RunResult
from src.StatisticalAnalysis import run_tests_labeled
from src.StringHelper import as_file_name, from_int
from src.FillMaskUtils.CategorizacionConfig import CategorizacionConfig

# Solo para BNE
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer, FillMaskPipeline

from src.ListHelper import *


cat_config_ismael = CategorizacionConfig(
    "result_fillmask/categorias_ismael",
    "../TextTools/CategoriasAdjetivos/excel_ismael.tsv",
    "./data/FillMask/sentences.tsv",
    True
)

cat_config_polaridad_visibilidad = CategorizacionConfig(
    "result_fillmask/categorias_polaridad_visibilidad",
    "../TextTools/CategoriasAdjetivos/polaridad_visibilidad.tsv",
    "./data/FillMask/sentences.tsv",
    True
)

cat_config_polaridad_visibilidad_negadas = CategorizacionConfig(
    "result_fillmask/categorias_polaridad_visibilidad_negadas",
    "../TextTools/CategoriasAdjetivos/polaridad_visibilidad.tsv",
    "./data/FillMask/sentences_neg.tsv",
    True
)

cat_config_polaridad_foa_foa = CategorizacionConfig(
    "result_fillmask/categorias_polaridad_foa_foa",
    "../TextTools/CategoriasAdjetivos/polaridad_foa_foa.tsv",
    "./data/FillMask/sentences.tsv",
    True
)

cat_config_polaridad_foa_foa_with_visibles = CategorizacionConfig(
    "result_fillmask/categorias_polaridad_foa_foa_with_visibles",
    "../TextTools/CategoriasAdjetivos/polaridad_foa_foa_with_visibles.tsv",
    "./data/FillMask/sentences.tsv",
    True
)

cat_config_yulia = CategorizacionConfig(
    "result_fillmask/categorias_yulia",
    "../TextTools/CategoriasAdjetivos/yulia.tsv",
    "./data/FillMask/sentences.tsv",
    True
)

cat_config_profesiones =  CategorizacionConfig(
    "result_fillmask_profesiones/base",
    "../TextTools/CategoriasAdjetivos/profesiones_10_cnae_2021t2.tsv",
    "./data/FillMask/sentences_profesiones.tsv",
    False,
    10
)


cconfig = cat_config_yulia

# constantes
T = "\t"
#RESULT_PATH = "result_fillmask/categorias_ismael"
TOTAL_CAT = "[_TOTAL]"
UNKOWN_CAT = "[???]"
WORD_MIN_LEN = 4
WRITE_DEBUG = False
WRITE_STATS = False

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
    filler = GroupedFillMask(model, modelname, tokenizer, cconfig.RESULT_PATH, cconfig.quantity, True).run_for_sentences(sentences)
    return filler


def save_run(model_name, points, scores, kind="m"):

    # ReFormatear resultados

    l = []
    l_adj = []
    category_count = {}
    category_points = {}
    category_score = {}

    # Inicializar el mapa
    for category in adjetivos_categorias:
        category_count[category] = 0
        category_points[category] = 0
        category_score[category] = 0

    category_count[UNKOWN_CAT] = 0
    category_points[UNKOWN_CAT] = 0
    category_score[UNKOWN_CAT] = 0

    category_points[TOTAL_CAT] = 0
    category_count[TOTAL_CAT] = 0
    category_score[TOTAL_CAT] = 0

    for key, points_value in points.items():
        score_value = scores[key]

        l.append(from_int(points_value, 4) + T + key)
        all_filling_words.append(key)

        # Solo si es un adjetivo
        if key in adjectives_map or not cconfig.check_is_adjective:
            l_adj.append(from_int(points_value, 4) + T + key)
            all_filling_adjectives.append(key)

            # Buscar la categoria
            category = UNKOWN_CAT
            if key in adjetivos_categorizados:
                category = adjetivos_categorizados[key]

            # Agregar valores
            category_count[category] = category_count[category] + 1
            category_points[category] = category_points[category] + points_value
            category_score[category] = category_score[category] + score_value

            # Agregar al total
            category_count[TOTAL_CAT] = category_count[TOTAL_CAT] + 1
            category_points[TOTAL_CAT] = category_points[TOTAL_CAT] + points_value
            category_score[TOTAL_CAT] = category_score[TOTAL_CAT] + score_value

    l_category = []
    dict_results = {}
    for category_key in category_count.keys():

        # Count
        count = category_count[category_key]
        prc_count = (count*100) / category_count[TOTAL_CAT]

        # Points
        points = category_points[category_key]
        total_points = category_points[TOTAL_CAT]
        prc_points = (points * 100) / total_points

        # Scores
        score = category_score[category_key]
        total_score = category_score[TOTAL_CAT]
        prc_score = (score * 100) / total_score

        rresult = RunResult(category_key, count, prc_count, points, prc_points, score, prc_score)
        dict_results[category_key] = rresult

        l_category.append(category_key + T + str(count) + T + str( prc_count ) + T + str(points) + T + str( prc_points ) + T + str(score) + T + str(prc_score))

    # Ordenar ahora que son texto
    l.sort(reverse=True)
    l_adj.sort(reverse=True)
    l_category.sort(reverse=True)

    # Añadir cabeceras
    l_category.insert(0, "[CAT]" + T + "Count" + T + "PRC_Count" + T + "Points" + T + "PRC_points" + T + "Score" + T + "PRC_score")

    # Juntar lineas
    data = "\n".join(l)
    data_adj = "\n".join(l_adj) + "\n" + FechaHoraTextual()
    data_category = "\n".join(l_category)

    # Pasar a disco
    path = cconfig.RESULT_PATH + "/run_" + str(run_id) + "_" + kind + "_" + as_file_name(model_name)

    if WRITE_DEBUG:
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
            data_f = list_as_file(list_as_str_list(l_after))

            write_txt(data_m, cconfig.RESULT_PATH + "/stats_source_" + posfix + "_m.txt")
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

    sentences_m = [sentence[0].replace("[MASK]", MASK) for sentence in sentences]
    sentences_f = [sentence[1].replace("[MASK]", MASK) for sentence in sentences]

    c_m, points_m, score_m = run_grouped(model, modelname, tokenizer, sentences_m)
    c_f, points_f, score_f = run_grouped(model, modelname, tokenizer, sentences_f)

    result_table_m = save_run(modelname, points_m, score_m, "m")
    result_table_f = save_run(modelname, points_f, score_f, "f")
    run_results.append((modelname, result_table_m, result_table_f))

    print("OK => " + modelname)

sentences = read_paired_tsv(cconfig.sentences_path)

uncased_sentences = [ [p[0].lower().replace("[mask]", "[MASK]"), p[1].lower().replace("[mask]", "[MASK]")] for p in sentences]
models = read_paired_tsv("./data/FillMask/models.tsv")

for idx, model in enumerate(models):
    run_id = model[0]
    sentence_list = sentences if model[4] == "cased" else uncased_sentences
    run(model[1], model[2], model[3], sentence_list)
    print("Finalizado modelo nro " + str(idx))

data = list_as_file(all_filling_words)
write_txt(data, cconfig.RESULT_PATH + "/summary_all_filling_words.csv")

data = list_as_file(all_filling_adjectives)
write_txt(data, cconfig.RESULT_PATH + "/summary_all_filling_adjectives.csv")


if cconfig.categories_ready:

    if WRITE_STATS:
        run_global_stats()

    adjetivos_sin_categorizar = filter( lambda adjetivo: not adjetivo in adjetivos_categorizados, all_filling_adjectives)
    data = list_as_file(adjetivos_sin_categorizar)
    write_txt(data, cconfig.RESULT_PATH + "/summary_adj_missing_category.csv")

    write_json(run_results, cconfig.RESULT_PATH + "/run_result.json");


