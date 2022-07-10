import os
import pandas as pd
import jsonpickle

import relhelpers.io.project_helper as _project

class WriteHelper:

    def __init__(self) -> None:
        pass

    def write_log(text, folder, fname):
        # path = "results/test/" + fname
        path = "results/" + folder + "/stats_" + fname
        os.makedirs(os.path.dirname(path), exist_ok=True)

        f = open(path, "w")
        f.write(text)
        f.close()

        print('Fichero guardado en ' + path)

    def txt(text, path):
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

    
    def save_array_as_excel(data, folder, fname):
        df = pd.DataFrame.from_records(data)

        path = "results/" + folder + "/" + fname + ".xlsx"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        writer = pd.ExcelWriter(path)
        df.to_excel(writer)
        writer.save()
        print('Fichero guardado en ' + path)

    @staticmethod
    def write(path:str, data):

        if "~/" in path:
            path = _project.from_root(path.split("~/")[1])

        os.makedirs(os.path.dirname(path), exist_ok=True)

        f = open(path, "w")
        f.write(data)
        f.close()
