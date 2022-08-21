

import pandas as pd
from transformers import FillMaskPipeline

from dataclass.filltemplate.fill_template_result import FillTemplateResult
from dataclass.filltemplate.fill_template_config import FillTemplateConfig
from dataclass.model_config import ModelConfig

from relhelpers.huggingface.service.PostTagger import PosTaggerService
from relhelpers.io.project_helper import ProjectHelper as _project
from relhelpers.huggingface.model_helper import HuggingFaceModelHelper as _hf_model
from relhelpers.huggingface.fillmask_helper import FillMaskHelper as _hf_fillmask
from relhelpers.pandas.pandas_helper import PandasHelper as _pd
from relhelpers.primitives.annotations import log_time
from relhelpers.primitives.string_helper import StringHelper as _string
from relhelpers.io.write_helper import WriteHelper as _write
from relhelpers.io.read_helper import ReadHelper as _read

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

        models_df = _pd.read_tsv(_project.data_path(FillTemplate.__name__, "models.tsv"))
        models: 'list[ModelConfig]' = models_df.apply( lambda row: ModelConfig(row[0],row[1],row[2],row[3], row[3] == 'cased'), axis = 1)

        for model in models:

            # TODO: Generalizar y cachear
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

            self.run_for_model(model.name, model.tokenizer, model.mask, templates)
        
        self.export_all_results()

    @log_time
    def run_for_model(self, model_name: str, tokenizer_name: str, mask: str, templates_df: pd.DataFrame):

        model, tokenizer = _hf_model.load_model(model_name, tokenizer_name)
        pipeline = FillMaskPipeline(model, tokenizer, top_k=self.cfg.n_predictions, device=model.device.index)
        tagger = PosTaggerService(device_index=model.device.index)

        dimensions = templates_df.columns
        for dimension in dimensions:
            dimension_df = templates_df[dimension]
            self.run_for_dimension(tagger, pipeline, model_name, dimension_df, dimension, mask)
        
        self.data = self.data.append(self.model_data)
        self.export_model_result(model_name)
        self.model_data = pd.DataFrame()

    @log_time
    def run_for_dimension(self, tagger: PosTaggerService, pipeline: FillMaskPipeline, model_name: str, df: pd.DataFrame, dimension: str, mask: str):
        [self.run_for_sentence(tagger, pipeline, model_name, sentence, dimension, mask) for sentence in df]

    def run_for_sentence(self, tagger: PosTaggerService, pipeline: FillMaskPipeline,  model_name: str, sentence: str, dimension: str, mask: str):
        # Predict
        res = pipeline(sentence)

        # To pandas
        res_df = _pd.from_dict(res)

        # Add context
        res_df['sentence'] = sentence   # He is [MASK]
        res_df['model'] = model_name    # beto
        res_df['dimension'] = dimension # m/f
        res_df['pos_tag'] = res_df.apply(lambda row: self.tag_sentence(tagger, mask, row) , axis = 1)
        
        res_df.reset_index(inplace=True)
        res_df['rsv'] = [len(res_df)]*len(res_df) - res_df.index 

        # Alter
        res_df["token_str"] = res_df["token_str"].str.strip()
        res_df["token_str"] = res_df["token_str"].str.lower()

        # Delete extra
        #res_df = _pd.remove_col(res_df, 'sequence')

        self.model_data = self.model_data.append(res_df) 

    def tag_sentence(self, tagger: PosTaggerService, mask: str, row):
        word = row['token_str'].strip()
        sequence = row['sentence'].replace(mask, word)
        return tagger.tag(sequence, word)
        

    def export_model_result(self, model_name):
        path = _project.result_path(self.experiment, FillTemplate.__name__, _string.as_file_name(model_name) + ".tsv" )
        _pd.save(self.model_data, path)

    def export_all_results(self):
        self.data.reset_index(drop=True)
        # self.data["token_str"] = self.data["token_str"].str.strip()
        # self.data["token_str"] = self.data["token_str"].str.lower()

        path = _project.result_path(self.experiment, FillTemplate.__name__, FillTemplate.__name__ )
        file_tsv = path + ".tsv"
        file_json = path + ".json"

        _pd.save(self.data, file_tsv)
        adjectives = _read.json_list_as_lookup(_project.data_path("Adjectives", "cess_spanish_adjectives.json"))
        adjectives = [adjective.lower() for adjective in adjectives]
        
        records = self.data.to_dict('records')
        unique_words = pd.unique(self.data["token_str"].values).tolist()

        unique_adjectives = []
        other_words = []
        for word in unique_words:
            if word in adjectives:
                unique_adjectives.append(word)
            else:
                other_words.append(word)

        result_container = FillTemplateResult()
        result_container.add_all(records, unique_adjectives, other_words)
        _write.json(result_container, file_json)
        

cfg = FillTemplateConfig(
    'Spanish Genre',
    _project.data_path(FillTemplate.__name__,'sentences.tsv')
)

FillTemplate(cfg)


'''

class GroupedFillMask:

    def run_for_sentences(self, sentences):
        for sentence in sentences:
            self.run_for_text(sentence)

        counts = dict(sorted(self.grouped_count.items(), key=lambda item: item[1], reverse=True))
        retrieval_status_values = dict(sorted(self.grouped_retrieval_status_values.items(), key=lambda item: item[1], reverse=True))
        #probabilities = { key: sum(value)/len(value) for key,value in self.grouped_model_probabilities.items()}
        probabilities = { key: sum(value) for key,value in self.grouped_model_probabilities.items()}

        return counts, retrieval_status_values, probabilities


    def valid_token(self, token: str):

        clean = token.replace("[", "").replace("]", "").replace(".", "")

        if len(clean) < WORD_MIN_LEN:
            return False
        if "#" in token:
            return False

        return True

'''