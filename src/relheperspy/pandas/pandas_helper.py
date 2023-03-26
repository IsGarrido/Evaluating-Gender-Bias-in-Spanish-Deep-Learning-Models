import types
import os
import inspect
import pandas as pd
import datetime as dt

def log_pd(fn):

    if type(fn).__name__ == 'staticmethod':
        fn = fn.__func__
    
    # https://stackoverflow.com/questions/50673566/how-to-get-the-path-of-a-function-in-python
    file = 'file.py'
    try:
        file =os.path.abspath(inspect.getfile(fn)).split('/')[-1]
    except:
        pass

    def wrapper(df, *args, **kwargs):
        tic = dt.datetime.now()
        result = fn(df, *args, **kwargs)
        toc = dt.datetime.now()
        print(f"{file} | {fn.__name__} took {toc - tic }")
        return result
    return wrapper
    
class PandasHelper:

    @staticmethod
    def from_classes(items) -> pd.DataFrame:
        return pd.DataFrame([t.__dict__ for t in items])

    @log_pd
    @staticmethod
    def read_tsv(path: str) -> pd.DataFrame:
        df = pd.read_csv(path, sep='\t', header = 0)
        return PandasHelper.remove_comments(df)

    @staticmethod
    def remove_comments(df) -> pd.DataFrame:
        return df[~df[df.columns[0]].str.contains("#")]

    # https://stackoverflow.com/questions/39475978/apply-function-to-each-cell-in-dataframe
    @log_pd
    @staticmethod
    def apply_all_cells(df, fn) -> pd.DataFrame:
        return df.applymap(fn)

    # @log_pd
    @staticmethod
    def from_dict(items: dict):
        return pd.DataFrame.from_dict(items)

    @staticmethod
    def to_dict(df: pd.DataFrame):
        return df.to_dict('records')

    # @log_pd
    @staticmethod
    def remove_col(df: pd.DataFrame, col: str) -> pd.DataFrame:
        return df.drop(col, axis=1)
    
    @log_pd
    def save(df: pd.DataFrame, path: str):
        df.to_csv(path, sep="\t")
        print("Saved " + path )
    
    @log_pd
    def load(path: str) -> pd.DataFrame:
        return pd.read_csv(path, sep = "\t")

    @log_pd
    @staticmethod
    def log(pd: pd.DataFrame) -> pd.DataFrame:
        return pd
    
    # Explore
    @staticmethod
    def unique_by_col(df: pd.DataFrame, col: str):
        return df[col].unique()
    
    @staticmethod
    def unique_count_by_col(df: pd.DataFrame, col: str):
        return df[col].value_counts()

