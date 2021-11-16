from src.FillMask.Service.AdjectiveService import AdjectiveService
from src.FillMask.Service.TaskStatService import TaskStatService
from src.FillMask.Vm.AdjectiveStatResult import AdjectiveStatResult
from src.FillMask.Vm.AdjectiveSummaryStat import AdjectiveSummaryStat
from src.Utils.DictHelper import DictHelper
from src.Utils.FileReaderHelper import FileReaderHelper
from src.Utils.FileWriterHelper import FileWriterHelper
from src.Utils.FunctionalHelper import FunctionalHelper
from src.Utils.JsonHelper import JsonHelper

from collections import defaultdict

from src.Utils.PandasHelper import PandasHelper


class StatCore:

    def __init__(self):
        json = FileReaderHelper.read_raw("~/result_data/FillMask/predictions.json")

        self.data_points = JsonHelper.decode(json)
        self.statService = TaskStatService()

        adjectiveService = AdjectiveService()
        for datapoint in self.data_points:
            for prediction in datapoint.predictions:
                prediction.set_adjective(adjectiveService.has(prediction.token_str))


    def adjective_tasks_stats(self, qty):

        groups = FunctionalHelper.group_by_two(self.data_points, "model", "sentence_index");

        arr = []
        for model in groups:
            sentences = groups[model]

            for sentence_tasks_index in sentences:
                sentence_tasks = sentences[sentence_tasks_index]

                for task in sentence_tasks:
                    res = self.statService.get_stats_for_task(task, qty)
                    arr.append(res)

        return arr

    def adjective_tasks_stats_grouped_by_model(self, stats, qty):

        stats_by_model = FunctionalHelper.group_by_two(stats, "model", "type")

        arr = []
        for model_key in stats_by_model:
            model_stats_by_type = stats_by_model[model_key]

            for type_key in model_stats_by_type:
                stat_list = model_stats_by_type[type_key]
                n_words = FunctionalHelper.sum(stat_list, "n_words")
                n_adjectives = FunctionalHelper.sum(stat_list, "n_adjectives")

                grouped_stat = AdjectiveSummaryStat(model_key, type_key, n_words, n_adjectives, qty)
                arr.append(grouped_stat)
        return arr

        #json = JsonHelper.encode(arr)
        #FileWriterHelper.write("~/result_data/FillMask/adjectives_stats_by_model_" + str(qty) + ".json", json)
    def descriptive_stats_by_model(self, arr):

        df = PandasHelper.from_classes(arr)
        x = 0

        models = df["model"].unique()
        types = df["type"].unique()

        results_grouped = defaultdict(list)

        for model in models:
            stats_dict = df[df["model"] == model]["proportion"].describe().to_dict()
            #stats_dict = DictHelper.exclude_key(stats_dict, "n_results")
            stats_dict["model"] = model
            stats_dict["type"] = "all"
            results_grouped[model].append(stats_dict)

            for type in types:
                type_dict = df[ (df["model"] == model) & (df["type"] == type) ]["proportion"].describe().to_dict()
                #stats_type_dict = DictHelper.exclude_key(type_dict, "n_results")
                type_dict["model"] = model
                type_dict["type"] = type
                results_grouped[model].append(type_dict)

        global_dict = df["proportion"].describe().to_dict()
        global_dict["model"] = "global"
        global_dict["type"] = "global"
        results_grouped["global"].append(global_dict)

        json = JsonHelper.encode(results_grouped)
        FileWriterHelper.write("~/result_data/FillMask/descriptive_stats_by_model.json", json)

        results_plain = []
        for result_key in results_grouped:
            result_list = results_grouped[result_key]
            results_plain.extend(result_list)

        json = JsonHelper.encode(results_plain)
        FileWriterHelper.write("~/result_data/FillMask/descriptive_stats.json", json)


    def adjective_stats(self, max):

        arr = []
        for qty in range(1,max+1):
            stats = self.adjective_tasks_stats(qty)
            stats_by_model = self.adjective_tasks_stats_grouped_by_model(stats, qty)
            arr.extend(stats_by_model)

        self.descriptive_stats_by_model(arr)


StatCore().adjective_stats(30)
