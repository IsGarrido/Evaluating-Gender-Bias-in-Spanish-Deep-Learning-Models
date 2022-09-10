import pandas as pd
from relhelperspy.primitives.dict_helper import DictHelper as _dict

class EvaluateCategoriesDataService():

    def add_is_adjective_column(self, df: pd.DataFrame):

        df['is_adjective'] = df["pos_tag"] == "AQ"
        df.drop(columns=['pos_tag'], inplace=True)

        return df
    
    def add_category_column(self, df: pd.DataFrame, categories: 'dict[str, str]'):
        category_lookup = _dict.as_lookup(categories)
        df["category"] = df.apply(
            lambda row: category_lookup.get(row['word'], 'unknown')
        , axis=1 ) 
        return df

    def add_adjective_proportion(self, df: pd.DataFrame) -> pd.DataFrame:
        df["adj_prop"] = (df["adj_cnt"] / df["count"]) * 100
        return df

    def group_by_sentence_fn(self, df_data: pd.DataFrame) -> pd.DataFrame:
        
        grouping_columns = ['dimension', 'model', 'category', 'sentence']
        base_grouping = df_data.groupby(grouping_columns, as_index=False).agg(
            score_sum=('score', 'sum'),

            score_min=('score', 'min'),
            score_max=('score', 'max'),
            score_mean=('score', 'mean'),

            count=('rsv', 'count'),

            adj_cnt=('is_adjective', 'sum')
        )

        rsv_grouping = df_data[df_data["is_adjective"]].groupby(grouping_columns, as_index=False).agg(
            rsv_sum=('rsv', 'sum'),

            rsv_min=('rsv', 'min'),
            rsv_max=('rsv', 'max'),
            rsv_mean=('rsv', 'mean'),
        )

        merged_df = base_grouping.merge(rsv_grouping, on = grouping_columns )
        return merged_df
        # return grouped_res[grouped_res.category != 'unknown']

    def group_by_category_fn(self, df_data: pd.DataFrame) -> pd.DataFrame:

        grouping_columns = ['dimension', 'model', 'category']

        base_df = df_data.groupby(grouping_columns, as_index = False).agg(
            score_sum=('score', 'sum'),

            score_min=('score', 'min'),
            score_max=('score', 'max'),
            score_mean=('score', 'mean'),

            count=('rsv', 'count'),

            adj_cnt=('is_adjective', 'sum')
        )

        rsv_df = df_data[df_data["is_adjective"]].groupby(
            ['dimension', 'model', 'category'], as_index = False
        ).agg(
            rsv_sum=('rsv', 'sum'),

            rsv_min=('rsv', 'min'),
            rsv_max=('rsv', 'max'),
            rsv_mean=('rsv', 'mean'),
        )

        merged_df = base_df.merge(rsv_df, on = grouping_columns)
        return merged_df


    def group_by_dimension_fn(self, df_data: pd.DataFrame) -> pd.DataFrame:

        grouping_columns = ['dimension', 'model']

        base_df = df_data.groupby(grouping_columns, as_index = False).agg(
            score_sum=('score', 'sum'),

            score_min=('score', 'min'),
            score_max=('score', 'max'),
            score_mean=('score', 'mean'),

            count=('rsv', 'count'),

            adj_cnt=('is_adjective', 'sum')
        )

        rsv_df = df_data[df_data["is_adjective"]].groupby(grouping_columns, as_index = False).agg(
            rsv_sum=('rsv', 'sum'),

            rsv_min=('rsv', 'min'),
            rsv_max=('rsv', 'max'),
            rsv_mean=('rsv', 'mean'),
        )

        merged_df = base_df.merge(rsv_df, on = grouping_columns)
        return merged_df


    def group_by_model_fn(self, df_data: pd.DataFrame) -> pd.DataFrame:

        grouping_columns = ['model']

        base_df = df_data.groupby(grouping_columns, as_index = False).agg(
            score_sum=('score', 'sum'),

            score_min=('score', 'min'),
            score_max=('score', 'max'),
            score_mean=('score', 'mean'),

            count=('rsv', 'count'),

            adj_cnt=('is_adjective', 'sum')
        )

        rsv_df = df_data[df_data["is_adjective"]].groupby(grouping_columns, as_index = False).agg(
            rsv_sum=('rsv', 'sum'),

            rsv_min=('rsv', 'min'),
            rsv_max=('rsv', 'max'),
            rsv_mean=('rsv', 'mean'),
        )
        
        merged_df = base_df.merge(rsv_df, on = grouping_columns)
        return merged_df


    def group_sentences(self, df_data):

        grouping_columns = ['sentence']

        base_df = df_data.groupby(grouping_columns, as_index = False
        ).agg(
            score_sum=('score', 'sum'),

            score_min=('score', 'min'),
            score_max=('score', 'max'),
            score_mean=('score', 'mean'),

            count=('rsv', 'count'),

            adj_cnt=('is_adjective', 'sum')
        )

        rsv_df = df_data[df_data["is_adjective"]].groupby(grouping_columns, as_index = False
        ).agg(
            rsv_sum=('rsv', 'sum'),

            rsv_min=('rsv', 'min'),
            rsv_max=('rsv', 'max'),
            rsv_mean=('rsv', 'mean'),
        )

        merged_df = base_df.merge(rsv_df, on = grouping_columns)
        return merged_df


    def group_sentences_with_dimensions(self, df_data):

        grouping_columns = ['sentence', 'dimension']
        base_df = df_data.groupby(grouping_columns, as_index = False).agg(
            score_sum=('score', 'sum'),

            score_min=('score', 'min'),
            score_max=('score', 'max'),
            score_mean=('score', 'mean'),

            count=('rsv', 'count'),

            adj_cnt=('is_adjective', 'sum')
        )

        rsv_df = df_data[df_data["is_adjective"]].groupby(grouping_columns, as_index = False).agg(
            rsv_sum=('rsv', 'sum'),

            rsv_min=('rsv', 'min'),
            rsv_max=('rsv', 'max'),
            rsv_mean=('rsv', 'mean'),
        )

        merged_df = base_df.merge(rsv_df, on = grouping_columns )
        return merged_df
