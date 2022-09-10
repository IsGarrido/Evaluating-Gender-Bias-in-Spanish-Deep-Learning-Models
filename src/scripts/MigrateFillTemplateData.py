import pandas as pd
from dataclass.model_config import ModelConfig
from relhelperspy.io.project_helper import ProjectHelper as _project
from relhelperspy.pandas.pandas_helper import PandasHelper as _pd
from relhelperspy.primitives.string_helper import StringHelper as _string
from relhelperspy.io.write_helper import WriteHelper as _write

import warnings
warnings.filterwarnings("ignore")

"""
Script to migrate FillTemplate Task result to other formats. Ex join every file into one file.
"""
class MigrateFillTemplateData:

    def __init__(self) -> None:

        folder = _project.result_path(self.__class__.__name__, None)
        _write.create_dir(folder)

        self.run()

    def run(self):

        models_df = _pd.read_tsv(_project.data_path("FillMask", "models.tsv"))
        models: 'list[ModelConfig]' = models_df.apply( lambda row: ModelConfig(row[0],row[1],row[2],row[3], row[3] == 'cased'), axis = 1)
        data = pd.DataFrame()

        for model in models:

            path = _project.result_path(self.__class__.__name__, _string.as_file_name(model.name) + ".tsv" )
            mode_df = _pd.load(path)
            data = data.append(mode_df)

        self.migrate_to_tsv(data)

    def migrate_to_tsv(self, df: pd.DataFrame):
        path = _project.result_path("FillMask", "FillMask.tsv" )
        _pd.save(df, path)

MigrateFillTemplateData()
