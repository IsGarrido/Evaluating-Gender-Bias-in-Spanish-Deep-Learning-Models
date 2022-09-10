from src.FillMask.Service.AdjectiveService import AdjectiveService
from src.FillMask.Service.TaskStatService import TaskStatService
from src.FillMask.Vm.AdjectiveStatResult import AdjectiveStatResult
from src.FillMask.Vm.AdjectiveSummaryStat import AdjectiveSummaryStat

from collections import defaultdict

import relhelperspy.io.read_helper as _read
import relhelperspy.primitives.dict_helper as _dict
import relhelperspy.io.write_helper as _write
import relhelperspy.functional.functional_helper as _fn
import relhelperspy.io.json_helper as _json
import relhelperspy.pandas.pandas_helper as _pd

class StatCore:

    def __init__(self):
        json = _read.read_raw("~/result_data/FillMask/predictions.json")

        self.data_points = _json.decode(json)
        self.statService = TaskStatService()

        adjectiveService = AdjectiveService()
        for datapoint in self.data_points:
            for prediction in datapoint.predictions:
                prediction.set_adjective(adjectiveService.has(prediction.token_str))


    def adjective_tasks_stats(self, qty):

        groups = _fn.group_by_two(self.data_points, "model", "sentence_index")

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

        stats_by_model = _fn.group_by_two(stats, "model", "type")

        arr = []
        for model_key in stats_by_model:
            model_stats_by_type = stats_by_model[model_key]

            for type_key in model_stats_by_type:
                stat_list = model_stats_by_type[type_key]
                n_words = _fn.sum(stat_list, "n_words")
                n_adjectives = _fn.sum(stat_list, "n_adjectives")

                grouped_stat = AdjectiveSummaryStat(model_key, type_key, n_words, n_adjectives, qty)
                arr.append(grouped_stat)
        return arr

        #json = JsonHelper.encode(arr)
        #_write.write("~/result_data/FillMask/adjectives_stats_by_model_" + str(qty) + ".json", json)
    def descriptive_stats_by_model(self, arr):

        df = _pd.from_classes(arr)
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

        json = _json.encode(results_grouped)
        _write.write("~/result_data/FillMask/descriptive_stats_by_model.json", json)

        results_plain = []
        for result_key in results_grouped:
            result_list = results_grouped[result_key]
            results_plain.extend(result_list)

        json = _json.encode(results_plain)
        _write.write("~/result_data/FillMask/descriptive_stats.json", json)


    def adjective_stats(self, max):

        #arr = []

        #for qty in range(1,max+1):
        #    stats = self.adjective_tasks_stats(qty)
        #    stats_by_model = self.adjective_tasks_stats_grouped_by_model(stats, qty)
        #    arr.extend(stats_by_model)

        stats = self.adjective_tasks_stats(max)
        stats_by_model = self.adjective_tasks_stats_grouped_by_model(stats, max)
        #arr.extend(stats_by_model)

        json = _json.encode(stats_by_model)
        _write.write("~/result_data/FillMask/stats_by_model.json", json)

        x = 0
        #self.descriptive_stats_by_model(arr)


StatCore().adjective_stats(29)
