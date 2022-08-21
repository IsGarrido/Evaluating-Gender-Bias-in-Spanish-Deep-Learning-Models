import pandas as pd

class EvaluateCategoriesFilterService():

    def group_by_sentence_fn(self, df_data: pd.DataFrame) -> pd.DataFrame:

        # filtered_df = df_data.loc[df_data.category != 'unknown'].groupby(
        #     ['dimension', 'model', 'category', 'sentence'], as_index=False
        # ).agg(
        #     rsv_sum=('rsv', 'sum'),

        #     rsv_min=('rsv', 'min'),
        #     rsv_max=('rsv', 'max'),
        #     rsv_mean=('rsv', 'mean'),

        #     score_sum=('score', 'sum'),

        #     score_min=('score', 'min'),
        #     score_max=('score', 'max'),
        #     score_mean=('score', 'mean'),

        #     # count of records, rsv or score is the same
        #     count=('rsv', 'count'),

        #     adjective_count=('is_adjective', 'sum')
        # )

        grouped_res = df_data.groupby(
            ['dimension', 'model', 'category', 'sentence'], as_index=False
        ).agg(
            rsv_sum=('rsv', 'sum'),

            rsv_min=('rsv', 'min'),
            rsv_max=('rsv', 'max'),
            rsv_mean=('rsv', 'mean'),

            score_sum=('score', 'sum'),

            score_min=('score', 'min'),
            score_max=('score', 'max'),
            score_mean=('score', 'mean'),

            # count of records, rsv or score is the same
            count=('rsv', 'count'),

            adjective_count=('is_adjective', 'sum')
        )

        return grouped_res[grouped_res.category != 'unknown']

    def group_by_category_fn(self, df_by_sentence: pd.DataFrame) -> pd.DataFrame:
        return df_by_sentence.groupby(
            ['dimension', 'model', 'category'], as_index = False
        ).agg(
            rsv_sum = ('rsv_sum', 'sum'),
            score_sum = ('score_sum', 'sum'),
            count = ('count', 'sum'),

            rsv_min = ('rsv_min', 'min'),
            rsv_max = ('rsv_max', 'max'),
            rsv_mean = ('rsv_mean', 'mean'),

            score_min = ('score_min', 'min'),
            score_max = ('score_max', 'max'),
            score_mean = ('score_mean', 'mean'),

            adjective_count = ('adjective_count', 'sum')
        )

    def group_by_dimension_fn(self, df_by_category: pd.DataFrame) -> pd.DataFrame:
        return df_by_category.groupby(
            ['dimension', 'model'], as_index = False
        ).agg(
            rsv_sum = ('rsv_sum', 'sum'),
            score_sum = ('score_sum', 'sum'),
            count = ('count', 'sum'),

            rsv_min = ('rsv_min', 'min'),
            rsv_max = ('rsv_max', 'max'),
            rsv_mean = ('rsv_mean', 'mean'),

            score_min = ('score_min', 'min'),
            score_max = ('score_max', 'max'),
            score_mean = ('score_mean', 'mean'),

            adjective_count = ('adjective_count', 'sum')
        )

    def group_by_model_fn(self, df_by_dimension: pd.DataFrame) -> pd.DataFrame:
        return df_by_dimension.groupby(
            ['model'], as_index = False
        ).agg(
            rsv_sum = ('rsv_sum', 'sum'),
            score_sum = ('score_sum', 'sum'),
            count = ('count', 'sum'),

            rsv_min = ('rsv_min', 'min'),
            rsv_max = ('rsv_max', 'max'),
            rsv_mean = ('rsv_mean', 'mean'),

            score_min = ('score_min', 'min'),
            score_max = ('score_max', 'max'),
            score_mean = ('score_mean', 'mean'),

            adjective_count = ('adjective_count', 'sum')
        )

