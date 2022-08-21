import pandas as pd
import numpy as np

# VM
from dataclass.filltemplate.fill_template_result import FillTemplateResult
from dataclass.evaluate_categories.evaluate_categories_config import EvaluateCategoriesConfig

# Helpers
from relhelpers.io.project_helper import ProjectHelper as _project
from relhelpers.io.json_helper import JsonHelper as _json
from relhelpers.io.read_helper import ReadHelper as _read
from relhelpers.primitives.string_helper import StringHelper as _string
from relhelpers.pandas.pandas_helper import PandasHelper as _pd
from relhelpers.io.write_helper import WriteHelper as _write
from service.EvaluateCategoriesDataService import EvaluateCategoriesDataService


class EvaluateCategories:

    def __init__(self, cfg: EvaluateCategoriesConfig) -> None:

        self.cfg :EvaluateCategoriesConfig = cfg
        self.experiment = _string.as_file_name(cfg.label)
        _service = EvaluateCategoriesDataService()

        # Load data
        fill_template_path = _project.result_path(self.experiment, "FillTemplate", "FillTemplate.json" )
        fill_template_json = _read.as_text(fill_template_path)
        categories = _read.json_as_dict(cfg.categories_path)
        
        fill_template_result: FillTemplateResult = _json.decode(fill_template_json)
        all_data = fill_template_result.data
        
        df_data = pd.DataFrame.from_records(all_data)
        df_data = _service.add_is_adjective_column(df_data)
        df_data = _service.add_category_column(df_data, categories)

        df_by_sentence = _pd.log(_service.group_by_sentence_fn(df_data))
        df_by_sentence = _pd.log(_service.add_adjective_proportion(df_by_sentence))

        df_by_category = _pd.log(_service.group_by_category_fn(df_data))
        df_by_category = _pd.log(_service.add_adjective_proportion(df_by_category))

        df_by_dimension = _pd.log(_service.group_by_dimension_fn(df_data))
        df_by_dimension = _pd.log(_service. add_adjective_proportion(df_by_dimension))

        df_by_model = _pd.log(_service.group_by_model_fn(df_data))
        df_by_model = _pd.log(_service.add_adjective_proportion(df_by_model))

        path_sentence = _project.result_path(self.experiment, "EvaluateCategories", "BySentence.json" )
        path_category = _project.result_path(self.experiment, "EvaluateCategories", "ByCategory.json" )
        path_dimension = _project.result_path(self.experiment, "EvaluateCategories", "ByDimension.json" )
        path_model = _project.result_path(self.experiment, "EvaluateCategories", "ByModel.json" )

        _write.df_as_json(df_by_sentence, path_sentence)
        _write.df_as_json(df_by_category, path_category)
        _write.df_as_json(df_by_dimension, path_dimension)
        _write.df_as_json(df_by_model, path_model)

        #self.compute_statistics_for_words(df_data)
        

    # def split_by_dimension(self, df, column):
    #     df.groupby(['dimension', column], as_index = False).head()
    #     df.groupby(['dimension', 'model'], as_index = False)['rsv'].agg(['min', 'max', 'mean']).add_prefix('rsv_').reset_index()
    #     df.groupby(['dimension', 'model', 'sentence'], as_index = False)['rsv'].agg(['min', 'max', 'mean', 'sum']).add_prefix('rsv_').reset_index()
    #     df.groupby(['dimension', 'model', 'sentence', "category"], as_index = False)['rsv'].agg(['min', 'max', 'mean', 'sum']).add_prefix('rsv_').reset_index()
    #     df.groupby(['dimension', 'model', 'sentence', "category"], as_index = False).agg({ 'rsv': ['min', 'max', 'mean', 'sum'], 'score': ['min', 'max', 'mean', 'sum'] })
    #     df.groupby(['dimension', 'model', 'sentence', "category"], as_index = False).agg({ 'rsv': ['min', 'max', 'mean', 'sum'], 'score': ['min', 'max', 'mean', 'sum'] }).sort_values( by = [('score', 'mean')], ascending = False)
    #     df.groupby(['dimension', 'model', 'sentence', "category"], as_index = False).agg({ 'rsv': ['min', 'max', 'mean', 'sum'], 'score': ['min', 'max', 'mean', 'sum'] }).sort_values( by = [('score', 'mean')], ascending = False).groupby('model', 'sentence', "category").agg({})
    #     df.groupby(['dimension', 'model', 'sentence', "category"], as_index = False).agg({ 'rsv': ['min', 'max', 'mean', 'sum'], 'score': ['min', 'max', 'mean', 'sum'] }).sort_values( by = [('score', 'mean')], ascending = False).groupby(["model","sentence", "category"]).agg({ })

    #     df["category"] = df["token_str"] + "_"

    def compute_statistics_for_words(self, df):
        df_male = df[df.dimension == "male"]
        df_female = df[df.dimension == "female"]

        df_word_male = df_male.groupby(by = ["token_str"], dropna = True ).sum()
        df_word_female = df_female.groupby(by = ["token_str"], dropna = True ).sum()
        
        df.groupby("token_str").agg(mean_index = ('index', np.mean), sum_index = ('index', np.sum), mean_rsv = ('rsv', np.mean), sum_rsv = ('rsv', np.sum) )

        df.groupby(['dimension', 'model'], as_index = False)

        x = 1
        # pd_male = pd[]
        # pd_data.groupby( by = ["token_str"] , dropna=True).sum()

    def compute_statistics_for_categories(self):
        pass

cfg = EvaluateCategoriesConfig(
    'Spanish Genre',
    _project.data_path("EvaluateCategories", 'Yulia.json')
)

EvaluateCategories(cfg)
