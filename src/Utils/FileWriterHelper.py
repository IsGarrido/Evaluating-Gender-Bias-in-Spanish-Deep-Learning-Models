import os

from src.Utils.ProjectHelper import ProjectHelper


class FileWriterHelper:

    @staticmethod
    def write(path:str, data):

        if "~/" in path:
            path = ProjectHelper.from_root(path.split("~/")[1])

        os.makedirs(os.path.dirname(path), exist_ok=True)

        f = open(path, "w")
        f.write(data)
        f.close()
