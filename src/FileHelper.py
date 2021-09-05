import pandas as pd
import openpyxl
from os import listdir
from os.path import isdir
from os.path import isfile, join
import os
import errno

def save_array_as_excel(data, folder, fname):
    df = pd.DataFrame.from_records(data)

    path = "results/" + folder + "/" + fname + ".xlsx"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    writer = pd.ExcelWriter(path)
    df.to_excel(writer)
    writer.save()
    print('Fichero guardado en ' + path)


def pandad_read_tsv(file):
    data = pd.read_csv(file, sep='\t', decimal=",")
    return data


def write_log(text, folder, fname):
    # path = "results/test/" + fname
    path = "results/" + folder + "/stats_" + fname
    os.makedirs(os.path.dirname(path), exist_ok=True)

    f = open(path, "w")
    f.write(text)
    f.close()

    print('Fichero guardado en ' + path)


def write_txt(text, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    f = open(path, "w")
    f.write(text)
    f.close()

    print('Fichero guardado en ' + path)


def get_file_list(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def get_folder_list(path):
    folders = [f for f in listdir(path) if isdir(join(path, f))]
    return folders
