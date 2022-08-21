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
    sought_after_token_id = tokenizer.encode(word, add_special_tokens=False)[0]  # 928

    token_score = mask_token_logits[:, sought_after_token_id]
    return token_score;

def get_logits(sequence):
    input_ids = tokenizer.encode(sequence, return_tensors="pt").to('cuda')
    mask_token_index = torch.where(input_ids == tokenizer.mask_token_id)[1]

    token_logits = model(input_ids)[0]
    mask_token_logits = token_logits[0, mask_token_index, :]
    mask_token_logits = torch.softmax(mask_token_logits, dim=1)
    return mask_token_logits

def run(row, positivo):

    sen1 = row[1]
    sen2 = row[2]
    w1 = row[3]
    w2 = row[4]

    uid = row[0]
    ttype = row[5]

    res = runPair(sen1, w1, sen2, w2)
    ret = Result(positivo, sen1, sen2, w1,w2, ttype, res[0], res[1])

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

tokenizer = AutoTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
model = AutoModelForMaskedLM.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
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
        print(total)
        export(results, conjunto)
        return conjunto

positivos = RunFor("positivos")
negativos = RunFor("negativos")
otros = RunFor("otros")

todos = positivos + negativos + otros
export(todos, "todos")
