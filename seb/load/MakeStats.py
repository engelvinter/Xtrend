import pandas as pd

from common.bdays import (BDAYS_ONE_MONTH,
                          BDAYS_THREE_MONTHS,
                          BDAYS_SIX_MONTHS,
                          BDAYS_TWELVE_MONTHS)


class MakeStats:
    def __init__(self, date):
        self._date = date

    def _create_empty_frame(self):
        c = ["Fund", "Twelve_months", "Six_months", 
             "Three_months", "One_month", "Compound"]
        df = pd.DataFrame(columns=c)
        df = df.set_index("Fund")
        return df

    def _return(self, quotes, nbr_bdays):
        last_quote = quotes.quote[-1]
        start_quote = quotes.quote[-nbr_bdays]
        ret = (last_quote - start_quote) / start_quote
        return ret

    def _create_row(self, fund, quotes):
        row = []
        row.append(self._return(quotes, BDAYS_TWELVE_MONTHS))
        row.append(self._return(quotes, BDAYS_SIX_MONTHS))
        row.append(self._return(quotes, BDAYS_THREE_MONTHS))
        row.append(self._return(quotes, BDAYS_ONE_MONTH))
        row.append((row[0] + row[1] + row[2] + row[3]) / 4)
        return row

    def _is_fund_still_open(self, last_open_date):
        diff = self._date - last_open_date
        return diff.days < 10
        
    def execute(self, funds):
        df = self._create_empty_frame()
        for fund, data in funds.items():
            try:
                sliced_data = data.loc[:self._date]
                last_open_date = sliced_data.index[-1].date()
                
                if self._is_fund_still_open(last_open_date):
                    row = self._create_row(fund, sliced_data)
                    df.loc[fund] = row

            except IndexError as e:
                print(fund, " has too short timeseries")
        df.name = self._date.strftime("%Y-%m-%d")
        return df
    