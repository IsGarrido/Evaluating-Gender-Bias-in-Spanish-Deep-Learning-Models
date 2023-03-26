import json
import os
import pandas as pd
import jsonpickle
import pathlib

import relhelperspy.io.project_helper as _project

class WriteHelper:

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_log(text, folder, fname):
        path = "results/" + folder + "/stats_" + fname
        os.makedirs(os.path.dirname(path), exist_ok=True)

        f = open(path, "w")
        f.write(text)
        f.close()

        print('Fichero guardado en ' + path)

    @staticmethod
    def txt(text, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        f = open(path, "w")
        f.write(text)
        f.close()

        print('Fichero guardado en ' + path)


    @staticmethod
    def json(obj, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = jsonpickle.encode(obj)
        f = open(path, "w")
        f.write(data)
        f.close()
    
    @staticmethod
    def stringify(obj, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = json.dumps(obj, separators=(',', ':'))
        f = open(path, "w")
        f.write(data)
        f.close()

    @staticmethod
    def save_array_as_excel(data, folder, fname):
        df = pd.DataFrame.from_records(data)

        path = "results/" + folder + "/" + fname + ".xlsx"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        writer = pd.ExcelWriter(path)
        df.to_excel(writer)
        writer.save()
        print('Fichero guardado en ' + path)
    
    @staticmethod
    def df_as_json(df: pd.DataFrame, path):
        df_dict = df.to_dict('records')
        WriteHelper.json(df_dict, path)

    @staticmethod
    def dict_as_json(d, path):
        WriteHelper.json(d, path)

    @staticmethod
    def list_as_json(l, path):
        WriteHelper.json(l,path)


    @staticmethod
    def write(path:str, data):

        if "~/" in path:
            path = _project.from_root(path.split("~/")[1])

        os.makedirs(os.path.dirname(path), exist_ok=True)

        f = open(path, "w")
        f.write(data)
        f.close()
