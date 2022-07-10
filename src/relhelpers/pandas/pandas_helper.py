import pandas as pd

class PandasHelper:

    @staticmethod
    def from_classes(items):
        return pd.DataFrame([t.__dict__ for t in items])
