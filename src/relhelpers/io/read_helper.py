import pandas as pd
import relhelpers.io.project_helper as _project
from typing import TextIO

class ReadHelper:
    
    def __init__(self) -> None:
        pass

    def pandad_read_tsv(file):
        data = pd.read_csv(file, sep='\t', decimal=",")
        return data

    def read_lines_as_list(path: str) -> 'list[str]':
        file = open(path, "r")
        content = file.read()
        lines: list[str] = content.split("\n")
        return lines


    def read_lines_as_dict(path):
        items = ReadHelper.read_lines_as_list(path)
        hashmap = dict.fromkeys(items, True)
        return hashmap

    def read_paired_tsv(file):
        data = ReadHelper.read_lines_as_list(file)
        data = filter(lambda line: not line.startswith("#"), data)
        data = filter(lambda line: line.strip() != "", data)

        paired = [item.split("\t") for item in data]
        return paired

    def read_lines_as_col_excel(path: str) -> 'dict[str, list[str]]':
        data: dict[str, list[str]] = {}

        lines: list[str] = ReadHelper.read_lines_as_list(path)
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
    def read_lines_as_col_excel_asdict(path: str) -> 'dict[str, str]':
        data: dict[str, list[str]] = ReadHelper.read_lines_as_col_excel(path)
        plain_data: dict[str, str] = {}

        for key, list_val in data.items():
            for item in list_val:
                plain_data[item] = key

        return plain_data


    @staticmethod
    def read_raw(path) -> str:

        if "~/" in path:
            path = _project.from_root(path.split("~/")[1])

        file: TextIO = open(path, "r")
        content: str = file.read()
        return content

    @staticmethod
    def read_as_list(path: str) -> 'list[str]':
        content = ReadHelper.read_raw(path)
        return content.split("\n")

    @staticmethod
    def read_as_dict(path: str) -> 'dict[str]':
        items = ReadHelper.read_as_list(path)
        hashmap = dict.fromkeys(items, True)
        return hashmap

    @staticmethod
    def read_tsv(file: str) -> 'list[list[str]]':
        data: list[str] = ReadHelper.read_as_list(file)
        filtered: filter[str] = filter(lambda line: not line.startswith("#"), data)
        filtered = filter(lambda line: line.strip() != "", filtered)

        paired: list[list[str]] = [item.split("\t") for item in filtered]
        return paired

