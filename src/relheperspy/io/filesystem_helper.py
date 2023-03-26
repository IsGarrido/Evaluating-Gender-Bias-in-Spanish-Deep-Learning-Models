import read_helper as _read
from os.path import join

class FileSystemHelper:

    def __init__(self) -> None:
        pass

    def get_file_list(path):
        files = [f for f in _read.listdir(path) if _read.isfile(join(path, f))]
        return files


    def get_folder_list(path):
        folders = [f for f in _read.listdir(path) if _read.isdir(join(path, f))]
        return folders
