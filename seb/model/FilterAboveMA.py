
from common.functions import above_ma as above_ma_ts


class FilterAboveMA:
    def __init__(self, funds, date, nbr_days):
        self._funds = funds
        self._date = date
        self._nbr_days = nbr_days
    
    def execute(self, df):
        def calc(name):
            ts = self._funds[name].nav[:self._date]
            return above_ma_ts(self._nbr_days, ts)

        matches = df.index.map(calc).tolist()
        filtered_df = df[matches]
        filtered_df.name = df.name
        
        return filtered_df