import unittest
import pandas as pd

from src.service.EvaluateCategoriesFilterService import EvaluateCategoriesFilterService


class TestEvaluateCategories(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.service = EvaluateCategoriesFilterService()

    # Creates mock df row
    def __r(self, rsv, prob, token, pos_token, sentence='', sequence = '', model='', dimension='') -> 'dict[str, str]':
        return {
            'rsv': rsv,
            'score': prob,
            'token_str': token,
            'sentence': sentence,
            'sequence': sequence,
            'model': model,
            'dimension': dimension,
            'pos_tag': pos_token
        }

    def __result(self, rsv, prob, token, pos_token, sentence, dimension = "Dim 1") -> 'dict[str, str]':
        return self.__r(rsv, prob, token, pos_token, sentence, sentence, "Model 1", dimension)

    def __data(self):
        return [
            self.__result(3, 0.9, "cool", "AQ", "s1", "male"),
            self.__result(2, 0.8, "pretty", "", "s1", "male"),
            self.__result(1, 0.7, "good", "", "s1", "male"),

            self.__result(3, 0.9, "bad", "AQ", "s1", "female"),
            self.__result(2, 0.8, "ugly", "", "s1", "female"),
            self.__result(1, 0.7, "fat", "", "s1", "female"),

            self.__result(3, 1, "nice", "AQ", "s2", "male"),
            self.__result(2, 0.5, "dumb", "AQ", "s2", "male"),
            self.__result(1, 0, "idiot", "", "s2", "male"),

            self.__result(3, 1, "unexpected", "AQ", "s2", "female"),
            self.__result(2, 0.5, "word", "AQ", "s2", "female"),
            self.__result(1, 0, "xword", "", "s2", "female"),


            self.__result(3, 1, "first s3", "", "s3", "male"),
            self.__result(2, 0.5, "second s3", "", "s3", "male"),
            self.__result(1, 0, "third s3", "", "s3", "male"),

            self.__result(3, 1, "first s3 fe", "", "s3", "female"),
            self.__result(2, 0.5, "second s3 fe", "", "s3", "female"),
            self.__result(1, 0, "third s3 fe", "", "s3", "female"),
        ]

    def __categories_data(self):
        return {
            "Cat 1": ['cool', 'pretty', 'good', 'nice'],
            "Cat 2": ['bad', 'ugly', 'fat', 'dumb', 'idiot', 'unexpected', 'word', 'xword', 'first s3', 'second s3'],
            "Cat 3": ['some', 'more', 'tokens'],
        }
    
    def __datadf(self) -> pd.DataFrame:
        data = self.__data()
        data_df = pd.DataFrame.from_records(data)
        return data_df

    def test__add_is_adjective_column__pos_tag_column_is_deleted(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        pos_tag_column_exist = 'pos_tag' in df.columns

        # assert
        self.assertFalse(pos_tag_column_exist)

    def test__add_is_adjective_column__is_adjective_count_valid(self):
        
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df_adjectives = df[df['is_adjective'] == True]

        # assert
        self.assertEqual(len(df_adjectives), 6)

    def test__add_is_adjective_column__is_adjective_filled_rows(self):
        
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df_adjectives = df[df['is_adjective'] == True]

        # assert
        self.assertEqual(df_adjectives['token_str'][0], 'cool')
        self.assertEqual(df_adjectives['token_str'][6], 'nice')

    def test__add_category_column__column_is_added(self):
        # arrange
        df = self.__datadf()
        categories = self.__categories_data()
        
        # act
        df = self.service.add_category_column(df, categories)

        # assert
        self.assertTrue('category' in df.columns)

    def test__add_category_column__column_is_valid(self):
        # arrange
        df = self.__datadf()
        categories = self.__categories_data()
        
        # act
        df = self.service.add_category_column(df, categories)

        print(df)
        # assert
        self.assertTrue(df.iloc[0]['category'] == 'Cat 1' )
        self.assertTrue(df.iloc[3]['category'] == 'Cat 2' )
        self.assertTrue(df.iloc[14]['category'] == 'unknown' )

    def test__group_by_sentence_fn__group_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_sentence_fn(df)

        # assert
        self.assertEqual(len(df), 8)

    def test__group_by_sentence_fn__valid_columns(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_sentence_fn(df)

        # assert
        self.assertTrue('sentence' in df.columns)
        self.assertTrue('sequence' in df.columns)
        self.assertTrue('model' in df.columns)
        self.assertTrue('dimension' in df.columns)
        self.assertTrue('category' in df.columns)

        self.assertFalse('token' in df.columns)
        self.assertFalse('token_str' in df.columns)
        self.assertFalse('pos_tag' in df.columns)
        self.assertFalse('score' in df.columns)
        self.assertFalse('rsv' in df.columns)

        self.assertTrue('count' in df.columns)
        self.assertTrue('adjective_count' in df.columns)

        self.assertTrue('rsv_sum' in df.columns)
        self.assertTrue('rsv_min' in df.columns)
        self.assertTrue('rsv_max' in df.columns)
        self.assertTrue('rsv_mean' in df.columns)

        self.assertTrue('score_sum' in df.columns)
        self.assertTrue('score_min' in df.columns)
        self.assertTrue('score_max' in df.columns)
        self.assertTrue('score_mean' in df.columns)

    def test__group_by_sentence_fn__valid_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_sentence_fn(df)

        # assert
        self.assertEqual(df.iloc[0]['count'], 3)
        self.assertEqual(df.iloc[1]['count'], 3)

    def test__group_by_sentence_fn__valid_adjective_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_sentence_fn(df)

        # assert
        self.assertEqual(df.iloc[0]['adjective_count'], 1)
        self.assertEqual(df.iloc[1]['adjective_count'], 2)

    def test__group_by_sentence_fn__rsv_aggregated_values(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_sentence_fn(df)

        # assert
        self.assertEqual(df.iloc[0]['rsv_sum'], 6)
        self.assertEqual(df.iloc[0]['rsv_min'], 1)
        self.assertEqual(df.iloc[0]['rsv_max'], 3)
        self.assertEqual(df.iloc[0]['rsv_mean'], 2)

    def test__group_by_category_fn__group_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_category_fn(df)

        # assert
        self.assertEqual(len(df), 5)

    def test__group_by_category_fn__valid_columns(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_category_fn(df)

        # assert
        self.assertTrue('model' in df.columns)
        self.assertTrue('dimension' in df.columns)
        self.assertTrue('category' in df.columns)

        self.assertFalse('token' in df.columns)
        self.assertFalse('token_str' in df.columns)
        self.assertFalse('pos_tag' in df.columns)
        self.assertFalse('score' in df.columns)
        self.assertFalse('rsv' in df.columns)
        self.assertFalse('sentence' in df.columns)
        self.assertFalse('sequence' in df.columns)

        self.assertTrue('count' in df.columns)
        self.assertTrue('adjective_count' in df.columns)

        self.assertTrue('rsv_sum' in df.columns)
        self.assertTrue('rsv_min' in df.columns)
        self.assertTrue('rsv_max' in df.columns)
        self.assertTrue('rsv_mean' in df.columns)

        self.assertTrue('score_sum' in df.columns)
        self.assertTrue('score_min' in df.columns)
        self.assertTrue('score_max' in df.columns)
        self.assertTrue('score_mean' in df.columns)

    def test__group_by_category_fn__valid_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_category_fn(df)

        # assert
        self.assertEqual(df[(df.category == 'Cat 1') & (df.dimension == 'male')]['count'].iloc[0], 4)
        self.assertEqual(df[(df.category == 'Cat 2') & (df.dimension == 'male')]['count'].iloc[0], 4)
        self.assertEqual(df[(df.category == 'Cat 2') & (df.dimension == 'female')]['count'].iloc[0], 6)
        self.assertEqual(df[(df.category == 'unknown') & (df.dimension == 'female')]['count'].iloc[0], 3)
        self.assertEqual(df[(df.category == 'unknown') & (df.dimension == 'male')]['count'].iloc[0], 1)

    def test__group_by_category_fn__valid_adjective_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_category_fn(df)

        # assert
        print(df)
        self.assertEqual(df[(df.category == 'Cat 1') & (df.dimension == 'male')]['adjective_count'].iloc[0], 2) 
        self.assertEqual(df[(df.category == 'Cat 2') & (df.dimension == 'male')]['adjective_count'].iloc[0], 1) 
        self.assertEqual(df[(df.category == 'Cat 2') & (df.dimension == 'female')]['adjective_count'].iloc[0], 3) 
        self.assertEqual(df[(df.category == 'unknown') & (df.dimension == 'female')]['adjective_count'].iloc[0], 0)
        self.assertEqual(df[(df.category == 'unknown') & (df.dimension == 'male')]['adjective_count'].iloc[0], 0) 

    def test__group_by_category_fn__rsv_aggregated_values(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_category_fn(df)
        res = df[(df.category == 'Cat 1') & (df.dimension == 'male')].iloc[0]

        # assert
        self.assertAlmostEqual(res['rsv_sum'], 9)
        self.assertAlmostEqual(res['rsv_min'], 1)
        self.assertAlmostEqual(res['rsv_max'], 3)
        self.assertAlmostEqual(res['rsv_mean'], 2.25)

    def test__group_by_category_fn__score_aggregated_values(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_category_fn(df)
        res = df[(df.category == 'Cat 1') & (df.dimension == 'male')].iloc[0]

        # assert
        self.assertAlmostEqual(res['score_sum'], 3.4)
        self.assertAlmostEqual(res['score_min'], 0.7)
        self.assertAlmostEqual(res['score_max'], 1)
        self.assertAlmostEqual(res['score_mean'], 0.85)

    def test__group_by_dimension_fn__group_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_dimension_fn(df)

        # assert
        self.assertEqual(len(df), 2)

    def test__group_by_dimension_fn__valid_columns(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_dimension_fn(df)

        # assert
        self.assertTrue('model' in df.columns)
        self.assertTrue('dimension' in df.columns)

        self.assertFalse('token' in df.columns)
        self.assertFalse('token_str' in df.columns)
        self.assertFalse('pos_tag' in df.columns)
        self.assertFalse('score' in df.columns)
        self.assertFalse('rsv' in df.columns)
        self.assertFalse('sentence' in df.columns)
        self.assertFalse('sequence' in df.columns)
        self.assertFalse('category' in df.columns)

        self.assertTrue('count' in df.columns)
        self.assertTrue('adjective_count' in df.columns)

        self.assertTrue('rsv_sum' in df.columns)
        self.assertTrue('rsv_min' in df.columns)
        self.assertTrue('rsv_max' in df.columns)
        self.assertTrue('rsv_mean' in df.columns)

        self.assertTrue('score_sum' in df.columns)
        self.assertTrue('score_min' in df.columns)
        self.assertTrue('score_max' in df.columns)
        self.assertTrue('score_mean' in df.columns)

    def test__group_by_dimension_fn__valid_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_dimension_fn(df)

        # assert
        self.assertEqual(df[df.dimension == 'male']['count'].iloc[0], 9)
        self.assertEqual(df[df.dimension == 'female']['count'].iloc[0], 9)

    def test__group_by_dimension_fn__valid_adjective_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_dimension_fn(df)

        # assert
        print(df)
        self.assertEqual(df[df.dimension == 'male']['adjective_count'].iloc[0], 3) 
        self.assertEqual(df[df.dimension == 'female']['adjective_count'].iloc[0], 3) 

    def test__group_by_dimension_fn__rsv_aggregated_values(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_dimension_fn(df)
        res = df[df.dimension == 'male'].iloc[0]

        # assert
        self.assertAlmostEqual(res['rsv_sum'], 18)
        self.assertAlmostEqual(res['rsv_min'], 1)
        self.assertAlmostEqual(res['rsv_max'], 3)
        self.assertAlmostEqual(res['rsv_mean'], 2)

    def test__group_by_dimension_fn__score_aggregated_values(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_dimension_fn(df)
        res = df[df.dimension == 'male'].iloc[0]

        # assert
        self.assertAlmostEqual(res['score_sum'], 5.4)
        self.assertAlmostEqual(res['score_min'], 0.0)
        self.assertAlmostEqual(res['score_max'], 1)
        self.assertAlmostEqual(res['score_mean'], 0.6)

    def test__group_by_model_fn__group_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_model_fn(df)

        # assert
        self.assertEqual(len(df), 1)

    def test__group_by_model_fn__valid_columns(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_model_fn(df)

        # assert
        self.assertTrue('model' in df.columns)

        self.assertFalse('token' in df.columns)
        self.assertFalse('token_str' in df.columns)
        self.assertFalse('pos_tag' in df.columns)
        self.assertFalse('score' in df.columns)
        self.assertFalse('rsv' in df.columns)
        self.assertFalse('sentence' in df.columns)
        self.assertFalse('sequence' in df.columns)
        self.assertFalse('category' in df.columns)
        self.assertFalse('dimension' in df.columns)

        self.assertTrue('count' in df.columns)
        self.assertTrue('adjective_count' in df.columns)

        self.assertTrue('rsv_sum' in df.columns)
        self.assertTrue('rsv_min' in df.columns)
        self.assertTrue('rsv_max' in df.columns)
        self.assertTrue('rsv_mean' in df.columns)

        self.assertTrue('score_sum' in df.columns)
        self.assertTrue('score_min' in df.columns)
        self.assertTrue('score_max' in df.columns)
        self.assertTrue('score_mean' in df.columns)

    def test__group_by_model_fn__valid_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_dimension_fn(df)

        # assert
        self.assertEqual(df[df.dimension == 'male']['count'].iloc[0], 9)
        self.assertEqual(df[df.dimension == 'female']['count'].iloc[0], 9)

    def test__group_by_model_fn__valid_adjective_count(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_model_fn(df)

        # assert
        print(df)
        self.assertEqual(df['adjective_count'].iloc[0], 6) 

    def test__group_by_model_fn__rsv_aggregated_values(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_model_fn(df)
        res = df.iloc[0]

        # assert
        self.assertAlmostEqual(res['rsv_sum'], 36)
        self.assertAlmostEqual(res['rsv_min'], 1)
        self.assertAlmostEqual(res['rsv_max'], 3)
        self.assertAlmostEqual(res['rsv_mean'], 2)

    def test__group_by_model_fn__score_aggregated_values(self):
        # arrange
        df = self.__datadf()

        # act
        df = self.service.add_is_adjective_column(df)
        df = self.service.add_category_column(df, self.__categories_data())
        df = self.service.group_by_model_fn(df)
        res = df.iloc[0]

        # assert
        self.assertAlmostEqual(res['score_sum'], 10.8)
        self.assertAlmostEqual(res['score_min'], 0.0)
        self.assertAlmostEqual(res['score_max'], 1)
        self.assertAlmostEqual(res['score_mean'], 0.6)