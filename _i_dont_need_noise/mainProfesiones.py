from transformers import AutoTokenizer, AutoModelForMaskedLM
import openpyxl
import torch
import csv
import pandas as pd


class Result:

    SentenceM = ''
    SentenceF = ''
    TargetM = ''
    TargetF = ''

    TargetType = ''
    AdjetiveType = 'otros'

    DetM = ''
    NameM = ''
    AdjM = ''
    DetF = ''
    NameF = ''
    AdjF = ''

    ScoreM = 0.0
    ScoreF = 0.0

    Uid = 0

    def __init__(self, adjType, sm, sf, m, f, targetType, mval, fval):
        self.AdjetiveType = adjType
        self.SentenceM = sm
        self.SentenceF = sf
        self.TargetM = m
        self.TargetF = f
        self.TargetType = targetType
        self.ScoreM = mval
        self.ScoreF = fval

    def WithMeta(self, uid, detm, detf, namem,namef, adjm, adjf):
        self.Uid = uid;
        self.DetM = detm
        self.DetF = detf
        self.NameM = namem
        self.NameF = namef
        self.AdjM = adjm
        self.AdjF = adjf
        return self

    def WinM(self):
        return self.ScoreM > self.ScoreF

    def __str__(self):
        return self.TargetM + " " + str(self.ScoreM) + " ||| " + self.TargetF + " " + str(self.ScoreF)

    def to_dict(self):
        return {
            'Uid': self.Uid,
            'AdjetiveType': self.AdjetiveType,
            'SentenceM': self.SentenceM,
            'SentenceF': self.SentenceF,
            'TargetM' : self.TargetM,
            'ScoreM': self.ScoreM,
            'TargetF': self.TargetF,
            'ScoreF': self.ScoreF,
            'TargetType': self.TargetType,
            'DetM': self.DetM,
            'DetF': self.DetF,
            'NameM': self.NameM,
            'NameF': self.NameF,
            'AdjM': self.AdjM,
            'AdjF': self.AdjF,
        }


def scoreWord(mask_token_logits, word):
    sought_after_token_id = tokenizer.encode(word, add_special_tokens=False) # 928
    if len(sought_after_token_id) > 1:
        print("+1 " + sought_after_token_id.__str__())

    for id in sought_after_token_id:
        assert id != 3

    sought_after_token_id = sought_after_token_id[0]
    token_score = mask_token_logits[:, sought_after_token_id]
    return token_score

def get_logits(sequence):
    input_ids = tokenizer.encode(sequence, return_tensors="pt", add_special_tokens = False).to('cuda')
    mask_token_index = torch.where(input_ids == tokenizer.mask_token_id)[1]

    token_logits = model(input_ids)[0]
    mask_token_logits = token_logits[0, mask_token_index, :]
    mask_token_logits = torch.softmax(mask_token_logits, dim=1)
    return mask_token_logits

def runProfesion(row):

    # sen1 = row[0] unmasked
    # sen2 = row[1] unmasked
    sen1 = row[2]
    sen2 = row[3]
    w1 = row[4]
    w2 = row[5]

    uid = row[6]
    tId = row[7]

    res = runPair(sen1, w1, sen2, w2)

    # Pone los resultados a la izquierda. En 0 el, en 1 ella.
    join = res + row + [ w1 + '/' + w2 ]
    return join

def run(row, positivo):
    sen1 = row[1]
    sen2 = row[2]
    w1 = row[3]
    w2 = row[4]

    uid = row[0]
    ttype = row[5]

    res = runPair(sen1, w1, sen2, w2)
    ret = Result(positivo, sen1, sen2, w1, w2, ttype, res[0], res[1])

    return ret.WithMeta(uid, row[6], row[7], row[8], row[9], row[10], row[11])


def runPair(seq1, w1, seq2, w2):
    logits1 = get_logits(seq1)
    logits2 = get_logits(seq2)

    s1 = scoreWord(logits1, w1)
    s2 = scoreWord(logits2, w2)

    return [s1.item(),s2.item()] #Result(seq1, seq2, w1,w2, s1.item(), s2.item())

def export(data, AdjetiveType):
    df = pd.DataFrame.from_records([s.to_dict() for s in data])
    file = AdjetiveType + ".xlsx"
    writer = pd.ExcelWriter(file)
    df.to_excel(writer)
    writer.save()
    print('DataFrame is written successfully to Excel File.')

def exportProfs(data):
    df = pd.DataFrame.from_records(data)
    file = "profesiones.xlsx"
    writer = pd.ExcelWriter(file)
    df.to_excel(writer)
    writer.save()
    print('DataFrame is written successfully to Excel File.')

tokenizer = AutoTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
model = AutoModelForMaskedLM.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
model.eval()
model.to('cuda')

def RunFor(conjunto):
    file = "/mnt/disco2tb/Datos/OneDrive/2021/Universidad/Stereo/tests." + conjunto + ".txt"

    total = 0
    i = 0
    results = []

    with open(file, newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:
            ok = True
            res = run(row, conjunto);

            if ok:
                if res.WinM():
                    total -= 1
                else:
                    total += 1
            results.append(res)

            i += 1
            if i % 1000 == 0:
                print(str(i) + " -> " + str(total) )

        print(i)
        print(total)
        export(results, conjunto)
        return conjunto

def asDict(row):

    dict = {
        'ScoreM': row[0],
        'ScoreF': row[1],
        'SentenceM': row[2],
        'SentenceF': row[3],
        'MaskedSentenceM': row[4],
        'MaskedSentenceF': row[5],
        'TargetM': row[6],
        'TargetF': row[7],
        'Uid': row[8],
        'TestId': row[9],
    }

    dict['Target'] = row[18]

    if len(row) > 11:
        dict2 = {
            'NameM': row[10],
            'NameF': row[11],
            'GenreM': row[12],
            'GenreF': row[13],
            'DetM': row[14],
            'DetF': row[15],
            'ProfM': row[16],
            'ProfF': row[17],
            'Target': row[18]
        }

        dict = {**dict, **dict2}

    return dict



def RunProfesiones():

    total = 0
    results = []
    i = 0
    file = "/mnt/disco2tb/Datos/OneDrive/P/TextTools/FormarFrases/tests/profesiones.test.tsv"
    with open(file, newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter = '\t')

        for row in reader:
            res = runProfesion(row)

            if res[0] > res[1]:
                total -= 1
            else:
                total += 1
            results.append(asDict(res))

            i += 1
            if i % 1000 == 0:
                print(str(i) + " -> " + str(total))

        print(i)
        print(total)
        exportProfs(results)

RunProfesiones()

#positivos = RunFor("positivos")
#negativos = RunFor("negativos")
#otros = RunFor("otros")

#todos = positivos + negativos + otros
#export(todos, "todos")
