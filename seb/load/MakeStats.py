import pandas as pd
import numpy as np

from common.bdays import (BDAYS_ONE_MONTH,
                          BDAYS_THREE_MONTHS,
                          BDAYS_SIX_MONTHS,
                          BDAYS_TWELVE_MONTHS,
                          MA200_DAYS)


class MakeStats:
    def __init__(self, date, min_days_diff):
        self._date = date
        self._min_days_diff = min_days_diff

    def _create_empty_frame(self):
        c = ["Fund", "Twelve_months", "Six_months", 
             "Three_months", "One_month", "Compound", "Rel_MA200"]
        df = pd.DataFrame(columns=c)
        df = df.set_index("Fund")
        return df

    def _nav_return(self, navs, nbr_bdays):
        last_nav = navs.nav[-1]
        start_nav = navs.nav[-nbr_bdays]
        ret = (last_nav - start_nav) / start_nav
        return ret

    def _rel_diff_ma200(self, navs):
        if len(navs) < MA200_DAYS:
            return None

        mean = navs.nav.tail(MA200_DAYS).mean()
        rel_diff = (navs.nav[-1] - mean) / mean

        return np.round(rel_diff, 2) 

    def _create_row(self, fund, navs):
        row = []
        row.append(self._nav_return(navs, BDAYS_TWELVE_MONTHS))
        row.append(self._nav_return(navs, BDAYS_SIX_MONTHS))
        row.append(self._nav_return(navs, BDAYS_THREE_MONTHS))
        row.append(self._nav_return(navs, BDAYS_ONE_MONTH))
        row.append((row[0] + row[1] + row[2] + row[3]) / 4)
        row.append(self._rel_diff_ma200(navs))
        return row

    def _is_fund_still_open(self, last_open_date):
        diff = self._date - last_open_date
        return diff.days < self._min_days_diff
        
    def execute(self, funds):
        df = self._create_empty_frame()
        for fund, series in funds.items():
            try:
                sliced_series = series.loc[:self._date]
                last_open_date = sliced_series.index[-1].date()
                
                if not self._is_fund_still_open(last_open_date):
                    print("Fund '{0}' is closed".format(fund))
                    continue

                row = self._create_row(fund, sliced_series)
                df.loc[fund] = row

            except IndexError as e:
                print(fund, " has too short timeseries")
        df.name = self._date.strftime("%Y-%m-%d")
        return df
    