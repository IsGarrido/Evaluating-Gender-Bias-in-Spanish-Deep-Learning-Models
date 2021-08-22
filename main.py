import numpy as np
import csv

from src import ModelScorer
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

simpleconfig = ScorerConfig(
    2, 3,
    4,  # el
    5  # ella
)

simplemasculino = ScorerConfig(
    2, 2,
    4,  # el
    5  # ella
)

# Pasar esta basura a reflexión o meter en un mapa los metodos o algo..
def Run():
    res = input('Test:')

    if "," in res:
        RunComma(res)
    else:
        res_int = int(res)
        RunIdx(res_int)

def RunIdx(idx: int):
    fname = 'Run' + str(idx)
    globals()[fname]()

def RunComma(itemArr: str):
    items = itemArr.split(",")
    items_int = map(int, items)

    for idx in items_int:
        RunIdx(idx)

# Run all
def Run0():

    for i in range(1, 4):
        RunIdx(i)

    for i in range(7, 24):
        RunIdx(i)


def Run1():
    RunTest('test1.profesiones_small', simpleconfig)

def Run2():
    RunTest('test2.profesiones_big', simpleconfig)

def Run3():
    RunTest('test3.profesiones_small_alt', simpleconfig)

def Run4():
    RunTest('test4.profesiones_big_alt', simpleconfig)

def Run7():
    RunTest('test7.profesiones_masculinas_el_ella', simplemasculino)

def Run8():
    RunTest('test8.genero_profesiones_masculinas_el_ella', simplemasculino)

def Run9():
    RunTest('test9.adjetivos_enmascarados_positivos', simpleconfig)

def Run10():
    RunTest('test10.adjetivos_enmascarados_otros', simpleconfig)

def Run11():
    RunTest('test11.adjetivos_enmascarados_negativos', simpleconfig)

def Run12():
    RunTest('test12.genero_adjetivos_enmascarados_positivos', simpleconfig)

def Run13():
    RunTest('test13.genero_adjetivos_enmascarados_otros', simpleconfig)

def Run14():
    RunTest('test14.genero_adjetivos_enmascarados_negativos', simpleconfig)

def Run15():
    RunTest('test15.genero_adjetivos_enmascarados_positivos_grande', simpleconfig)

def Run16():
    RunTest('test16.genero_adjetivos_enmascarados_otros_grande', simpleconfig)

def Run17():
    RunTest('test17.genero_adjetivos_enmascarados_negativos_grande', simpleconfig)

def Run18():
    RunTest('test18.adjetivos_con_profesiones_enmascaradas_positivos', simpleconfig)

def Run19():
    RunTest('test19.adjetivos_con_profesiones_enmascaradas_otros', simpleconfig)

def Run20():
    RunTest('test20.adjetivos_con_profesiones_enmascaradas_negativos', simpleconfig)

def Run21():
    RunTest('test21.genero_adjetivos_negados_enmascarados_positivos_grande', simpleconfig)

def Run22():
    RunTest('test22.genero_adjetivos_negados_enmascarados_otros_grande', simpleconfig)

def Run23():
    RunTest('test23.genero_adjetivos_negados_enmascarados_negativos_grande', simpleconfig)




def RunTest(fname: str, config: ScorerConfig, verbose: bool = False):
    results = []
    i = 0
    scorer = ModelScorer.ModelScorer(config)

    file = "/mnt/disco2tb/Datos/OneDrive/P/TextTools/FormarFrases/tests/" + fname + ".test.tsv"
    with open(file, newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')

        for row in reader:
            try:
                res = scorer.get_score_row(row)
                results.append(res.as_dict())
            except:
                if verbose:
                    print("Error en:")
                    print(row)
                    print("\n")

            i += 1
            if i % 1000 == 0:
                print(str(i))

        print( 'Finalizado test ' + fname + " -> " + str(i))

        l1 = []
        l2 = []
        for result in results:
            l1.append(result.get("score_m"))
            l2.append(result.get("score_f"))

        text_log = run_tests_labeled(l1, l2)

        write_log(text_log, fname+'.txt')
        save_array_as_excel(results, fname)


Run()
