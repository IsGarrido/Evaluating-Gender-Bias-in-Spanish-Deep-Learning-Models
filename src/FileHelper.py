import pandas as pd
import openpyxl

def save_array_as_excel(data, fname):
    df = pd.DataFrame.from_records(data)
    path = "results/" + fname + ".xlsx"
    writer = pd.ExcelWriter(path)
    df.to_excel(writer)
    writer.save()
    print('Fichero guardado en ' + path)

def pandad_read_tsv(file):
    data = pd.read_csv(file, sep='\t', decimal=",")
    return data

def write_log(text, fname):
    path = "results/test/" + fname

    f = open(path, "w")
    f.write(text)
    f.close()

    print('Fichero guardado en ' + path)
