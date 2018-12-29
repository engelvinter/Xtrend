
import pandas as pd

class AddColumn:
    def __init__(self, name, dictionary):
        self._name = name
        self._dict = dictionary

    def execute(self, df):
        df[self._name] = pd.Series(self._dict)
        return df