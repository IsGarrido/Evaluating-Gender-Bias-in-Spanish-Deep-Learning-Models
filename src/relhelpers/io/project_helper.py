from pathlib import Path

class ProjectHelper:

    @staticmethod
    def get_project_root() -> str:
        return Path(__file__).parent.parent.parent.as_posix()

    @staticmethod
    def from_root(path):
        root = ProjectHelper.get_project_root()
        return root + "/" + path
