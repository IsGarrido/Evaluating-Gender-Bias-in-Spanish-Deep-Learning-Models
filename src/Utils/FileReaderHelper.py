from typing import List, TextIO

from src.Utils.ProjectHelper import ProjectHelper


class FileHelperReader:

    @staticmethod
    def read_raw(path) -> str:

        if "~/" in path:
            path = ProjectHelper.from_root(path.split("~/")[1])

        file: TextIO = open(path, "r")
        content: str = file.read()
        return content

    @staticmethod
    def read_lines_as_list(path: str) -> list[str]:
        content = FileHelperReader.read_raw(path)
        return content.split("\n")

    @staticmethod
    def read_tsv(file: str) -> list[list[str]]:
        data: list[str] = FileHelperReader.read_lines_as_list(file)
        filtered: filter[str] = filter(lambda line: not line.startswith("#"), data)
        filtered = filter(lambda line: line.strip() != "", filtered)

        paired: list[list[str]] = [item.split("\t") for item in filtered]
        return paired

