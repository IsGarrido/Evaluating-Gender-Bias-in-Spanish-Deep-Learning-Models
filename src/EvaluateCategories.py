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
from relhelpers.primitives.dict_helper import DictHelper as _dict
from relhelpers.pandas.pandas_helper import PandasHelper as _pd
from relhelpers.io.write_helper import WriteHelper as _write


class EvaluateCategories:

    def __init__(self, cfg: EvaluateCategoriesConfig) -> None:

        self.cfg :EvaluateCategoriesConfig = cfg
        self.experiment = _string.as_file_name(cfg.label)

        # Load categories
        categories = _read.json_as_dict(cfg.categories_path)
        self.word_categories = _dict.as_lookup(categories)

        # Load data
        fill_template_path = _project.result_path(self.experiment, "FillTemplate", "FillTemplate.json" )
        fill_template_json = _read.as_text(fill_template_path)
        
        fill_template_result: FillTemplateResult = _json.decode(fill_template_json)
        all_data = fill_template_result.data
        df_data = pd.DataFrame.from_records(all_data)
        
        # Add categories to data
        def get_category(row):
            return self.word_categories.get(row['token_str'], 'unknown')

        def is_adjective(row):
            return row['token_str'] in self.word_categories

        def add_adjective_proportion(df: pd.DataFrame) -> pd.DataFrame:
            df["adjetive_proportion"] = (df["adjective_count"] / df["count"]) * 100
            return df

        df_data["category"] = df_data.apply( lambda row: get_category(row), axis=1 ) 
        df_data["is_adjective"] = df_data.apply( lambda row: 1 if is_adjective(row) else 0, axis=1 ) 

        def group_by_sentence_fn(df_data: pd.DataFrame) -> pd.DataFrame:
            return df_data.groupby(
                ['dimension', 'model', 'category', 'sentence' ], as_index = False
            ).agg(
                rsv_sum = ('rsv', 'sum'),

                rsv_min = ('rsv', 'min'),
                rsv_max = ('rsv', 'max'),
                rsv_mean = ('rsv', 'mean'),

                score_sum = ('score', 'sum'),

                score_min = ('score', 'min'),
                score_max = ('score', 'max'),
                score_mean = ('score', 'mean'),

                count = ('rsv', 'count'), # count of records, rsv or score is the same

                adjective_count = ('is_adjective', 'sum')
            )

        def group_by_category_fn(df_by_sentence: pd.DataFrame) -> pd.DataFrame:
            return df_by_sentence.groupby(
                ['dimension', 'model', 'category'], as_index = False
            ).agg(
                rsv_sum = ('rsv_sum', 'sum'),
                score_sum = ('score_sum', 'sum'),
                count = ('count', 'sum'),

                rsv_min = ('rsv_min', 'min'),
                rsv_max = ('rsv_max', 'max'),
                rsv_mean = ('rsv_mean', 'mean'),

                score_min = ('score_min', 'min'),
                score_max = ('score_max', 'max'),
                score_mean = ('score_mean', 'mean'),

                adjective_count = ('adjective_count', 'sum')
            )

        def group_by_model_fn(df_by_category: pd.DataFrame) -> pd.DataFrame:
            return df_by_category.groupby(
                ['dimension', 'model'], as_index = False
            ).agg(
                rsv_sum = ('rsv_sum', 'sum'),
                score_sum = ('score_sum', 'sum'),
                count = ('count', 'sum'),

                rsv_min = ('rsv_min', 'min'),
                rsv_max = ('rsv_max', 'max'),
                rsv_mean = ('rsv_mean', 'mean'),

                score_min = ('score_min', 'min'),
                score_max = ('score_max', 'max'),
                score_mean = ('score_mean', 'mean'),

                adjective_count = ('adjective_count', 'sum')
            )
        
        
        df_by_sentence = _pd.log(group_by_sentence_fn(df_data))
        df_by_sentence = add_adjective_proportion(df_by_sentence)

        df_by_category = _pd.log(group_by_category_fn(df_by_sentence))
        df_by_category = add_adjective_proportion(df_by_category)

        df_by_model = _pd.log(group_by_model_fn(df_by_category))
        df_by_model = add_adjective_proportion(df_by_model)

        path_sentence = _project.result_path(self.experiment, "EvaluateCategories", "BySentence.json" )
        path_category = _project.result_path(self.experiment, "EvaluateCategories", "ByCategory.json" )
        path_model = _project.result_path(self.experiment, "EvaluateCategories", "ByModel.json" )

        _write.df_as_json(df_by_sentence, path_sentence)
        _write.df_as_json(df_by_category, path_category)
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
