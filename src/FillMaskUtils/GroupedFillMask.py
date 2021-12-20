from transformers import FillMaskPipeline

from src.FileHelper import write_txt
from src.StringHelper import as_file_name

WORD_MIN_LEN = 4
T = "\t"

class GroupedFillMask:

    def __init__(self, model, modelname, tokenizer, result_path, result_qty, write_files = False):

        self.model = model
        self.modelname = modelname
        self.model.eval()

        self.tokenizer = tokenizer

        self.pipeline = FillMaskPipeline(self.model, self.tokenizer, top_k=result_qty, device=self.model.device.index)

        self.grouped_count = {}
        self.grouped_retrieval_status_values = {}
        self.grouped_model_probabilities = {}

        self.result_path = result_path
        self.result_qty = result_qty
        self.write_files = write_files

    def valid_token(self, token: str):

        clean = token.replace("[", "").replace("]", "").replace(".", "")

        if len(clean) < WORD_MIN_LEN:
            return False
        if "#" in token:
            return False

        return True

    def save_stats(self, word: str, probability, idx):

        word = word.strip()
        if not self.valid_token(word):
            return

        # Count
        if word in self.grouped_count:
            self.grouped_count[word] = self.grouped_count[word] + 1
        else:
            self.grouped_count[word] = 1

        retrieval_status_values = self.result_qty - idx

        if word in self.grouped_retrieval_status_values:
            self.grouped_retrieval_status_values[word] = self.grouped_retrieval_status_values[word] + retrieval_status_values
        else:
            self.grouped_retrieval_status_values[word] = retrieval_status_values

        if word in self.grouped_model_probabilities:
            self.grouped_model_probabilities[word].append(probability)
        else:
            self.grouped_model_probabilities[word] = []
            self.grouped_model_probabilities[word].append(probability)


    def process_result(self, items, orig_line):
        l = []
        for idx, item in enumerate(items):
            word: str = item["token_str"].lower()
            probability = item["score"]
            self.save_stats(word, probability, idx)

            line = str(idx) + T + word + T + str(item["token"])
            l.append(line)

        if self.write_files:
            text = "\n".join(l)
            path = self.result_path + "/" + as_file_name(self.modelname) + "/" + as_file_name(orig_line) + ".csv"
            write_txt(text, path)

    def run_for_text(self, line):

        if line == "él ha conseguido el trabajo ya que es muy [MASK]." or line == "ella ha conseguido el trabajo ya que es muy [MASK].":
            print(1)

        res = self.pipeline(line)
        self.process_result(res, line)

    def run_for_sentences(self, sentences):
        for sentence in sentences:
            self.run_for_text(sentence)

        counts = dict(sorted(self.grouped_count.items(), key=lambda item: item[1], reverse=True))
        retrieval_status_values = dict(sorted(self.grouped_retrieval_status_values.items(), key=lambda item: item[1], reverse=True))
        #probabilities = { key: sum(value)/len(value) for key,value in self.grouped_model_probabilities.items()}
        probabilities = { key: sum(value) for key,value in self.grouped_model_probabilities.items()}

        return counts, retrieval_status_values, probabilities