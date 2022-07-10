import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

from src import ScorerConfig
from src.vm.SimpleTestResult import SimpleTestResult


class ModelScorer:

    def __init__(self, config: ScorerConfig, model_id='dccuchile/bert-base-spanish-wwm-uncased'):
        self.model = AutoModelForMaskedLM.from_pretrained(model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.config = config
        self.model.eval()
        self.model.to('cuda')

        self.test_uid = 0

    def get_score_row(self, row):

        self.test_uid = self.test_uid + 1

        #
        score_m = -1
        score_f = -1

        # Indexes
        index_masked_sentence_m = self.config.index_masked_sentence_m
        index_masked_sentence_f = self.config.index_masked_sentence_f
        index_target_value_m = self.config.index_target_value_m
        index_target_value_f = self.config.index_target_value_f

        # Values
        masked_sentence_m = row[index_masked_sentence_m]
        masked_sentence_f = row[index_masked_sentence_f]
        target_value_m = row[index_target_value_m]
        target_value_f = row[index_target_value_f]

        type = self.config.type

        if type == 'simple':
            score_m = self.get_score_softmax(masked_sentence_m, target_value_m)
            score_f = self.get_score_softmax(masked_sentence_f, target_value_f)
            return SimpleTestResult(self.test_uid, score_m, score_f, masked_sentence_m, masked_sentence_f, target_value_m, target_value_f)

        return [score_m, score_f]

    def get_score_softmax(self, sentence, target_word):
        sentence_logits = self.get_logits_at_mask(sentence)
        target_logits = self.get_score_for_word(sentence_logits, target_word)
        return np.log(target_logits)

        return target_logits


    ''' BORRAR '''

    def find_mask(self, sentence):
        words = sentence.split()
        idx = words.index('MASK')
        return idx

    ''' BORRAR '''

    def get_mask_index_as_torch(seq):
        words = seq.split(sep=' ')
        for idx, word in enumerate(words):
            if word == '[MASK]':
                return torch.from_numpy(np.array([idx]))

    def get_ids(self, sentence):
        return self.tokenizer.encode(sentence, return_tensors="pt", add_special_tokens=False).to('cuda')

    def get_logits_at_mask(self, sentence):

        # Encode
        input_ids = self.get_ids(sentence)
        mask_id = self.get_ids('[MASK]')[0]
        #mask_index = input_ids.index(mask_id)
        mask_index = (input_ids == mask_id).nonzero(as_tuple=True)[0]

        with torch.no_grad():
            # token_logits = self.model(input_ids)[0]
            outputs = self.model(input_ids)
            last_hidden_state = outputs[0]

        mask_logits = last_hidden_state[0, mask_index, :]
        mask_logits_softmax = torch.softmax(mask_logits, dim=1)
        return mask_logits_softmax

    def get_score_for_word(self, mask_token_logits, word):

        sought_after_token_ids = self.tokenizer.encode(word, add_special_tokens=False)
        if len(sought_after_token_ids) > 1:
            raise ValueError("Multi-token " + word)

        sought_after_token_id = sought_after_token_ids[0]

        token_score = mask_token_logits[:, sought_after_token_id]
        return token_score.item()
