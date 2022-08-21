import unittest
import pandas as pd

from src.service.EvaluateCategoriesFilterService import EvaluateCategoriesFilterService

class TestEvaluateCategories(unittest.TestCase):

    def __r(self, rsv, prob, token, sentence = '', category = '', model = '', dimension = '') -> 'dict[str, str]':  # Creates mock df row
        return {
            'rsv': rsv,
            'prob': prob, 
            'token': token,
            'sentence': sentence,
            'category': category,
            'model': model,
            'dimension': dimension
        }

    def __result(self, rsv, prob, token, sentence) -> 'dict[str, str]':
        return self.__r(rsv, prob, token, sentence, "Cat 1", "Model 1", "Dim 1")

    def test_sentence_grouping(self): # 'dimension', 'model', 'category', 'sentence']
        # arrange 
        data = [
            self.__result( 3, 0.9, "first", "s1"),
            self.__result( 2, 0.8, "second", "s1"),
            self.__result( 1, 0.7, "third", "s1"),

            self.__result( 3, 1, "first", "s2"),
            self.__result( 2, 0.5, "second", "s2"),
            self.__result( 1, 0, "third", "s2")
        ]
        df = pd.DataFrame.from_records(data)
        
        service = EvaluateCategoriesFilterService()

        print(data)
        res = service.group_by_sentence_fn(df)
        print(res)

        # act
        print(data)

        self.assertEqual(1, 1)


    # def test_group_by_sentence(self):

    #     # arrange

    #     # act

    #     # assert
