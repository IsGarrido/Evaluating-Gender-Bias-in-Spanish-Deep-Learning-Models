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
from relhelpers.primitives.annotations import log_time
from relhelpers.primitives.dict_helper import DictHelper as _dict
# Service
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
        dimensions = _dict.keys(fill_template_result.sentences)
        
        df_data = pd.DataFrame.from_records(all_data)
        df_data = _service.add_is_adjective_column(df_data)
        df_data = _service.add_category_column(df_data, categories)

        self.compute_sentences_statistics(_service, df_data.copy(), dimensions)
        self.compute_general_statistics(_service, df_data.copy())

    @log_time
    def compute_sentences_statistics(self, _service: EvaluateCategoriesDataService, df: pd.DataFrame,  dimensions: 'list[str]'):
        df_sentences = _service.group_sentences(df)
        df_sentences = _service.add_adjective_proportion(df_sentences)

        path_sentences = _project.result_path(self.experiment, "EvaluateCategories", "SentenceStatistics.json" )

        _write.df_as_json(df_sentences, path_sentences)

        by_dimension = {}
        for dimension in dimensions:
            sub_df = _service.group_sentences_with_dimensions(df)
            sub_df = sub_df[sub_df.dimension == dimension]
            by_dimension[dimension] = _pd.to_dict(sub_df)
            
        path_dim = _project.result_path(self.experiment, "EvaluateCategories", "SentenceAndDimensionStatistics.json" )
        _write.dict_as_json(by_dimension, path_dim)



    @log_time
    def compute_general_statistics(self, _service: EvaluateCategoriesDataService, df: pd.DataFrame):
        df_by_sentence = _service.group_by_sentence_fn(df)
        df_by_sentence = _service.add_adjective_proportion(df_by_sentence)

        df_by_category = _service.group_by_category_fn(df)
        df_by_category = _service.add_adjective_proportion(df_by_category)

        df_by_dimension = _service.group_by_dimension_fn(df)
        df_by_dimension = _service.add_adjective_proportion(df_by_dimension)

        df_by_model = _service.group_by_model_fn(df)
        df_by_model = _service.add_adjective_proportion(df_by_model)

        path_sentence = _project.result_path(self.experiment, "EvaluateCategories", "BySentence.json" )
        path_category = _project.result_path(self.experiment, "EvaluateCategories", "ByCategory.json" )
        path_dimension = _project.result_path(self.experiment, "EvaluateCategories", "ByDimension.json" )
        path_model = _project.result_path(self.experiment, "EvaluateCategories", "ByModel.json" )

        _write.df_as_json(df_by_sentence, path_sentence)
        _write.df_as_json(df_by_category, path_category)
        _write.df_as_json(df_by_dimension, path_dimension)
        _write.df_as_json(df_by_model, path_model)

    def compute_statistics_for_categories(self):
        pass

cfg = EvaluateCategoriesConfig(
    'Spanish Genre',
    _project.data_path("EvaluateCategories", 'Yulia.json')
)

EvaluateCategories(cfg)
