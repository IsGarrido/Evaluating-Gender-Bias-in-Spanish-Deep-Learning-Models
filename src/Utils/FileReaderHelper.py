from typing import List, TextIO

from src.Utils.ProjectHelper import ProjectHelper


class FileReaderHelper:

    @staticmethod
    def read_raw(path) -> str:

        if "~/" in path:
            path = ProjectHelper.from_root(path.split("~/")[1])

        file: TextIO = open(path, "r")
        content: str = file.read()
        return content

    @staticmethod
    def read_as_list(path: str) -> list[str]:
        content = FileReaderHelper.read_raw(path)
        return content.split("\n")

    @staticmethod
    def read_as_dict(path: str) -> dict[str]:
        items = FileReaderHelper.read_as_list(path)
        hashmap = dict.fromkeys(items, True)
        return hashmap

    @staticmethod
    def read_tsv(file: str) -> list[list[str]]:
        data: list[str] = FileReaderHelper.read_as_list(file)
        filtered: filter[str] = filter(lambda line: not line.startswith("#"), data)
        filtered = filter(lambda line: line.strip() != "", filtered)

        paired: list[list[str]] = [item.split("\t") for item in filtered]
        return paired

