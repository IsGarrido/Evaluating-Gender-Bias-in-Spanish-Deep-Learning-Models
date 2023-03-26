import os
from pathlib import Path
from tkinter import N

class ProjectHelper:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_project_root() -> str:
        path = Path(__file__).as_posix()
        src_index = path.index('/src/')
        return path[0:src_index]

    @staticmethod
    def from_root(path):
        root = ProjectHelper.get_project_root()
        return os.path.join(root, path)

    @staticmethod
    def special_path(main_type: str, sub_type: str, experiment: str, folder: str = None, file: str = None):
        
        path = ProjectHelper.from_root(main_type)

        if sub_type is not None:
            path = os.path.join(path, sub_type)

        if experiment is not None:
            path = os.path.join(path, experiment)

        if folder is not None:
            path = os.path.join(path, folder)

        if file is not None:
            return os.path.join(path, file)

        return path

    @staticmethod
    def data_path(folder = None, file = None) -> str:
        return ProjectHelper.special_path('assets', 'data', None, folder, file)

    @staticmethod
    def test_data_path(folder = None, file = None) -> str:
        return ProjectHelper.special_path('assets', 'tests', None, folder, file)

    @staticmethod
    def result_path(experiment = None, folder = None, file = None) -> str:
        return ProjectHelper.special_path('assets', 'result', experiment, folder, file)