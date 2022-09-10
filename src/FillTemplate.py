

import pandas as pd
from transformers import FillMaskPipeline

from dataclass.filltemplate.fill_template_result import FillTemplateResult
from dataclass.filltemplate.fill_template_config import FillTemplateConfig
from dataclass.model_config import ModelConfig

from relhelperspy.huggingface.service.PostTagger import PosTaggerService
from relhelperspy.io.project_helper import ProjectHelper as _project
from relhelperspy.huggingface.model_helper import HuggingFaceModelHelper as _hf_model
from relhelperspy.huggingface.fillmask_helper import FillMaskHelper as _hf_fillmask
from relhelperspy.pandas.pandas_helper import PandasHelper as _pd
from relhelperspy.primitives.annotations import log_time, log_time_with_counter
from relhelperspy.primitives.string_helper import StringHelper as _string
from relhelperspy.io.write_helper import WriteHelper as _write
from relhelperspy.io.cli_helper import CliHelper as _cli

import warnings
warnings.filterwarnings("ignore")

# TODO: Imporporar lo de valid token

class FillTemplate:

    def __init__(self, cfg: FillTemplateConfig) -> None:

        self.cfg = cfg        
        self.data = pd.DataFrame()
        self.model_data = pd.DataFrame()
        self.experiment = _string.as_file_name(cfg.label)

        # TODO revisar si esto hace falta aún 
        folder = _project.result_path(self.experiment, FillTemplate.__name__)
        _write.create_dir(folder)

        self.run()

    def run(self):
        # TODO: Generalizar y cachear
        cased_templates_df = _pd.read_tsv(self.cfg.templates_path)
        uncased_templates_df = _pd.apply_all_cells(cased_templates_df, _hf_fillmask.to_lower_but_mask)

        cased_templates_roberta_df = _pd.apply_all_cells(cased_templates_df, _hf_fillmask.to_robert_mask)
        uncased_templates_roberta_df = _pd.apply_all_cells(uncased_templates_df, _hf_fillmask.to_robert_mask)

        models_df = _pd.read_tsv(self.cfg.models_path)
        models: 'list[ModelConfig]' = models_df.apply( lambda row: ModelConfig(row[0],row[1],row[2],row[3], row[3] == 'cased'), axis = 1)

        for idx, model in enumerate(models):

            # TODO: Generalizar y cachear
            templates = {}
            if model.cased:
                if model.mask == "[MASK]":
                    templates = cased_templates_df
                else:
                    templates = cased_templates_roberta_df
            else:
                if model.mask == "[MASK]":
                    templates = uncased_templates_df
                else:
                    templates = uncased_templates_roberta_df

            self.run_for_model(model.name, model.tokenizer, model.mask, idx, templates)
        
        templates_export = {}
        templetes_dict = cased_templates_df.to_dict()
        for key in templetes_dict:
            val = templetes_dict[key]
            vals = list(val.values())
            templates_export[key] = vals
        
        model_names = [model.name for model in models]
        self.export_all_results(templates_export, model_names)

    @log_time_with_counter
    def run_for_model(self, model_name: str, tokenizer_name: str, mask: str, model_idx: int, templates_df: pd.DataFrame):

        model, tokenizer = _hf_model.load_model(model_name, tokenizer_name)
        pipeline = FillMaskPipeline(model, tokenizer, top_k=self.cfg.n_predictions, device=model.device.index)
        tagger = PosTaggerService(device_index=model.device.index)

        dimensions = templates_df.columns
        for dimension in dimensions:
            dimension_df = templates_df[dimension]
            self.run_for_dimension(tagger, pipeline, model_idx, dimension_df, dimension, mask)
        
        self.data = self.data.append(self.model_data)
        self.export_model_result(model_name)
        self.model_data = pd.DataFrame()

    @log_time
    def run_for_dimension(self, tagger: PosTaggerService, pipeline: FillMaskPipeline, model_idx: int, df: pd.DataFrame, dimension: str, mask: str):
        cdf = df.copy()
        cdf = cdf.reset_index()

        [self.run_for_sentence(tagger, pipeline, model_idx, sentence[1], index, dimension, mask) for index, sentence in cdf.iterrows()]

    def run_for_sentence(self, tagger: PosTaggerService, pipeline: FillMaskPipeline,  model_idx: int, sentence: str, sentence_index: int, dimension: str, mask: str):
        # Predict
        res = pipeline(sentence)

        # To pandas
        res_df = _pd.from_dict(res)

        # Add context
        # res_df['stn'] = sentence   # He is [MASK]
        res_df['sentence'] = sentence_index
        res_df['model'] = model_idx    # beto by its index
        res_df['dimension'] = dimension # m/f
        res_df['pos_tag'] = res_df.apply(lambda row: self.tag_sentence(tagger, mask, sentence, row['token_str'].strip()) , axis = 1)
        
        res_df.reset_index(inplace=True)
        res_df['rsv'] = [len(res_df)]*len(res_df) - res_df.index 

        # Alter
        res_df["word"] = res_df["token_str"].str.strip()
        res_df["word"] = res_df["word"].str.lower()

        # Delete extra
        res_df = _pd.remove_col(res_df, 'sequence')
        res_df = _pd.remove_col(res_df, 'token_str')

        self.model_data = self.model_data.append(res_df) 

    def tag_sentence(self, tagger: PosTaggerService, mask: str, sentence: str, word: str):
        msequence = sentence.replace(mask, word)
        return tagger.tag(msequence, word)

    def export_model_result(self, model_name):
        path = _project.result_path(self.experiment, FillTemplate.__name__, _string.as_file_name(model_name) + ".tsv" )
        _pd.save(self.model_data, path)

    def export_all_results(self, templates, models):
        self.data.reset_index(drop=True)

        path = _project.result_path(self.experiment, FillTemplate.__name__, FillTemplate.__name__ )
        file_tsv = path + ".tsv"
        file_json = path + ".json"
        _pd.save(self.data, file_tsv)
        
        records = self.data.to_dict('records')
        unique_words = pd.unique(self.data["word"].values).tolist()

        result_container = FillTemplateResult()
        result_container.add_all(records, unique_words, templates, models)
        _write.json(result_container, file_json)

        unique_adjectives = pd.unique(self.data[ (self.data["pos_tag"] == "AQ") & ( ~self.data["word"].str.contains("#", regex = False) ) ]["word"]).tolist()
        path_adjectives = _project.result_path(self.experiment, "FillTemplate", "Adjectives.json" )
        _write.list_as_json(unique_adjectives, path_adjectives)


# args = _cli.args(
#     label = 'Spanish Genre',
#     templates = 'sentences.tsv',
#     n_predictions = 29
# )

args = _cli.args(
    label = 'Spanish Genre 10',
    templates = 'sentences.tsv',
    models = 'models.tsv',
    n_predictions = 10
)

cfg = FillTemplateConfig(
    args.label,
    _project.data_path("FillTemplate", args.templates),
    _project.data_path("FillTemplate", args.models),
    args.n_predictions
)

FillTemplate(cfg)