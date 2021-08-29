import numpy as np
import csv

from src import ModelScorer, FileHelper
from src.FileHelper import save_array_as_excel
from src.ScorerConfig import ScorerConfig
from src.StatisticalAnalysis import *
from src.FileHelper import *

''' TEST SEIS  '''
'''
def runTestSeis(row):
    # sen1 = row[0] unmasked
    # sen2 = row[1] unmasked
    targetMasked1 = row[2]
    targetMasked2 = row[3]
    w1 = row[4]
    w2 = row[5]

    uid = row[6]
    tId = row[7]

    # 8 meta name m
    # 9 meta name f
    # 10 meta genre m
    # 11 meta genre f
    # 12 meta det m
    # 13 meta det f
    # 14 meta prof m
    # 15 meta prof f
    targetGenreMasked1 = row[16]
    targetGenreMasked2 = row[17]
    genreMasked1 = row[18]
    genreMasked2 = row[19]
    wa1 = row[20]
    wa2 = row[21]


    pred_genre_m = runSeisTarget(targetMasked1, targetGenreMasked1, genreMasked1, w1, wa1)
    pred_genre_f = runSeisTarget(targetMasked2, targetGenreMasked2, genreMasked2, w2, wa2)
    res = [pred_genre_m, pred_genre_f]

    # Pone los resultados a la izquierda. En 0 el, en 1 ella.
    join = res + row + [w1 + '/' + w2]
    return join
'''
'''
def runSeisTarget(mt, mtg, ma, word, wordAttr):

    if "[MASK] es compositor" == mt:
        print("Debug")

    index_target = get_mask_index_as_torch(mt)
    index_attribute = get_mask_index_as_torch(ma)

    # Saca los logits para MASK en ambos ejemplos.
    logits_mt = get_logits_idx(mt, index_target)
    logits_ma = get_logits_idx(ma, index_attribute)
    logits_mtg = get_logits_idx(mtg, index_target)

    # Busca los valores del valor real de TARGET
    pred_mt = score_word(logits_mt, word)
    pred_ma = score_word(logits_ma, wordAttr)

    pred_mtg = score_word(logits_mtg, word)
    pred_mta = score_word(logits_mtg, wordAttr)

    # Odd logs
    #pred_fixed = pred_mt - pred_ma
    #pred = np.log( pred_fixed / pred_mtg)

    pred = (pred_mt/pred_mtg) -  (pred_ma/ pred_mta)

    return pred


'''

'''
def runProfesion(row):
    # sen1 = row[0] unmasked
    # sen2 = row[1] unmasked
    targetMasked1 = row[2]
    targetMasked2 = row[3]
    w1 = row[4]
    w2 = row[5]

    uid = row[6]
    tId = row[7]

    # 8 meta name m
    # 9 meta name f
    # 10 meta genre m
    # 11 meta genre f
    # 12 meta det m
    # 13 meta det f
    # 14 meta prof m
    # 15 meta prof f
    targetGenreMasked1 = row[16]
    targetGenreMasked2 = row[17]

    res = runPair(targetMasked1, targetGenreMasked1, w1, targetMasked2, targetGenreMasked2, w2)

    # Pone los resultados a la izquierda. En 0 el, en 1 ella.
    join = res + row + [w1 + '/' + w2]
    return join
'''

'''
def runTarget(mt, mtg, word):
    # Indice de la MASK original, referente a target. Si se saca el indice más tarde, habrá más de una MASK
    index = get_mask_index_as_torch(mt)

    # Saca los logits para MASK en ambos ejemplos.
    logits_mt = get_logits_idx(mt, index)
    logits_mtg = get_logits_idx(mtg, index)

    # Busca los valores del valor real de TARGET
    pred_mt = score_word(logits_mt, word)
    pred_mtg = score_word(logits_mtg, word)

    # Odd logs
    pred = np.log(pred_mt / pred_mtg)

    return pred


def runPair(mt1, mtg1, w1, mt2, mtg2, w2):

    pred_m = runTarget(mt1, mtg1, w1)
    pred_f = runTarget(mt2, mtg2, w2)
    return [pred_m, pred_f]


def asDict(row):
    dict = {
        'ScoreM': row[0],
        'ScoreF': row[1],
        'SentenceM': row[2],
        'SentenceF': row[3],
        'MaskedTargetM': row[4],
        'MaskedTargetF': row[5],
        'TargetM': row[6],
        'TargetF': row[7],
        'Uid': row[8],
        'TestId': row[9],
        'NameM': '',
        'NameF': '',
        'DetM': '',
        'DetF': '',
        'GenreM': '',
        'GenreF': '',
        'ProfM': '',
        'ProfF': '',
    }

    if len(row) > 11:
        dict2 = {
            'NameM': row[10],
            'NameF': row[11],
            'DetM': row[12],
            'DetF': row[13],
            'GenreM': row[14],
            'GenreF': row[15],
            'ProfM': row[16],
            'ProfF': row[17],
            'MaskedTargetAttributeM': row[18],
            'MaskedTargetAttributeF': row[19],
            'MaskedAttributeM': row[20],
            'MaskedAttributeF': row[21],
            'AttributeM': row[22],
            'AttributeF': row[23],
        }

        dict['Target'] = row[len(row)-1] # last pos
        dict['Proporcion'] = row[0]/row[1]
        dict['Proporcion'] = row[0]/row[1]
        dict = {**dict, **dict2}

    return dict
'''


# INIT
# INIT
# INIT
# INIT
# INIT

autoconfig = ScorerConfig(
    2, 3,
    6,  # el
    7  # ella
)

folder_base = "/mnt/disco2tb/Datos/OneDrive/P/TextTools/FormarFrases/test_auto"

def Run():

    path = folder_base
    files = FileHelper.get_file_list(path)

    [ RunTest(name , autoconfig, False) for name in files ]


def RunTest(name, config: ScorerConfig, verbose: bool = False):

    file_clean_name = name.split('.')[0]
    path = folder_base
    file_path = path + '/' + name

    results = []
    i = 0
    errores = 0
    scorer = ModelScorer.ModelScorer(config)

    with open(file_path, newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')

        for row in reader:
            #try:
            res = scorer.get_score_row(row)
            results.append(res.as_dict())
            #except:
            #    if verbose:
            #        print("Error en:")
            #        print(row)
            #        print("\n")
            #    errores = errores + 1

            i += 1
            if i % 1000 == 0:
                print(str(i))

        print( 'Finalizado test ' + name + " -> " + str(i) + " con " + str(errores) + " errores ")

        l1 = []
        l2 = []
        for result in results:
            l1.append(result.get("score_m"))
            l2.append(result.get("score_f"))

        text_log = run_tests_labeled(l1, l2)
        text_log = text_log + "Errores:" + str(errores) + "/" + str(i)

        # Save
        folder = "Auto"
        write_log(text_log, folder, file_clean_name +'.txt')
        save_array_as_excel(results, folder, file_clean_name)


Run()

exit(0)