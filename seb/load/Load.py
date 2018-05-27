import pandas as pd
import numpy as np
import timeit
import os

class Load:
    def __init__(self, db_path, fund_names, min_days, max_missing_days):
        self._fund_names = fund_names
        self._path = db_path
        self._min_days = min_days
        self._max_missing_days = max_missing_days

    def _read_file(self, path, fund_name):
        filename = "{0}.csv".format(fund_name)
        filepath = os.path.join(path, filename)

        # Workaround for bug #15086
        filehandle = open(filepath, "r")
        df = pd.read_csv(filehandle, usecols=[1, 2, 3])

        return df

    def _set_index_date(self, df):
        # convert text string to pandas datetimestamp
        df['date'] = pd.to_datetime(df['date'])
        # use as index
        df = df.set_index("date")

        return df

    def _reindex_using_business_days(self, df):
        # reindex using business days
        start = df.first_valid_index()
        end = df.last_valid_index()
        range = pd.date_range(start, end, freq='B')
        df = df.reindex(range)
        # now check nbr of missing days in a row
        self._check_na_days(df)

        return df

    class TooManyMissingDays(Exception):
        pass

    def _check_na_days(self, df):
        row_status = df.isnull().quote
        only_nulls = row_status[row_status == True].index
        if len(only_nulls) == 0:
            return

        start_date = pd.Timestamp(only_nulls[0], freq="B")
        nbr_missing_days = 0

        for date in only_nulls:
            if start_date == date:
                start_date += 1
                nbr_missing_days += 1
            else:
                start_date = pd.Timestamp(date, freq="B")
                nbr_missing_days = 1

            if nbr_missing_days >= self._max_missing_days:
                raise Load.TooManyMissingDays()

    def _fill_na_days(self, df):
        df = df.fillna(method="ffill")
        return df

    def _remove_duplicates(self, df):
        df = df[~df.index.duplicated()]
        return df

    def _remove_zero_values(self, df):
        df = df[df.quote != 0]
        return df

    def _add_fund(self, funds, df, fund_name):
        df.name = fund_name   
        funds[fund_name] = df

    def _adjust_fund_remake(self, df):
        contains_id_nbr = df.id.apply(lambda x: np.isreal(x)).all()
        if not contains_id_nbr:
            return

        # Detect if Id is changed i.e. fund is recreated to a new fund  
        diff = df.id.diff()

        change = df.quote.pct_change()
        fund_remakes = diff[diff != 0]
        for index,_ in fund_remakes.iteritems():
            updated_rows = df[index:].quote / (1 + change[index])
            df.update(updated_rows)

    def _adjust_fund_abnormal(self, df):
        change = df.quote.pct_change()
        # Detect if change in fund is more than 10% interday
        abnormal_change = change[abs(change) > 0.1]
        for date_index, percent_change in abnormal_change.iteritems():
            updated_rows = df[date_index:].quote / (1 + percent_change)
            df.update(updated_rows)

    def _do_operations_on_dataset(self, df):
        df = self._set_index_date(df)
        df = self._remove_duplicates(df)
        df = self._reindex_using_business_days(df)
        df = self._fill_na_days(df)
        df = self._remove_zero_values(df)
        self._adjust_fund_remake(df)
        self._adjust_fund_abnormal(df)

        return df

    class NotEnoughNbrDays(Exception):
        pass

    def _check_min_days(self, df):
        height, _ = df.shape
        if height < self._min_days:
            raise Load.NotEnoughNbrDays()

    def _load_single_fund(self, fund_name):
        df = self._read_file(self._path, fund_name)        
        df = self._do_operations_on_dataset(df)
        self._check_min_days(df)

        return df

    def execute(self):
        funds = {}

        for fund_name in self._fund_names:
            try:
                #print("Loading {}".format(fund_name))
                df = self._load_single_fund(fund_name)
                self._add_fund(funds, df, fund_name)
            except Load.NotEnoughNbrDays:
                print("{}: not enough number of days".format(fund_name))
            except Load.TooManyMissingDays:
                print("{}: too many missing days in a row".format(fund_name))
            
        return funds