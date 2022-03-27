import jsonpickle
from typing import List, Dict, Any

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


def read_lines_as_list(path: str) -> list[str]:
    file = open(path, "r")
    content = file.read()
    lines: list[str] = content.split("\n")
    return lines


def read_lines_as_dict(path):
    items = read_lines_as_list(path)
    hashmap = dict.fromkeys(items, True)
    return hashmap

def read_paired_tsv(file):
    data = read_lines_as_list(file)
    data = filter(lambda line: not line.startswith("#"), data)
    data = filter(lambda line: line.strip() != "", data)

    paired = [item.split("\t") for item in data]
    return paired

def read_lines_as_col_excel(path: str) -> dict[str, list[str]]:
    data: dict[str, list[str]] = {}

    lines: list[str] = read_lines_as_list(path)
    tag_line: str = 2 if lines[0].startswith("#") else 1
    tags: list[str] = lines[tag_line].split("\t")

    # Preparar las listas vacias
    for tag in tags:
        data[tag] = []

    # Leemos las lines con datos y las vamos pasando a la lista que corresponda
    data_lines = lines[tag_line + 1:]
    for line in data_lines:
        parts = line.split("\t")
        for idx, part in enumerate(parts):
            if part != "":
                tag = tags[idx]
                data[tag].append(part)

    return data


# Deja el objeto de listas de string como un hashmap/lookup
def read_lines_as_col_excel_asdict(path: str) -> dict[str, str]:
    data: dict[str, list[str]] = read_lines_as_col_excel(path)
    plain_data: dict[str, str] = {}

    for key, list_val in data.items():
        for item in list_val:
            plain_data[item] = key

    return plain_data


def write_txt(text, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    f = open(path, "w")
    f.write(text)
    f.close()

    print('Fichero guardado en ' + path)


def write_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data = jsonpickle.encode(obj)
    f = open(path, "w")
    f.write(data)
    f.close()


def get_file_list(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def get_folder_list(path):
    folders = [f for f in listdir(path) if isdir(join(path, f))]
    return folders
