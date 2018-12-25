
from .Load import Load

import glob
import os.path
import os
import re

from datetime import datetime


def fund_names(db_path, regexp=".*", ext=".csv"):
    files = glob.glob("{}/*{}".format(db_path, ext))
    extract_base = lambda fullpath :  os.path.splitext(os.path.basename(fullpath))[0]
    all_names = [extract_base(fullpath) for fullpath in files]
    names = [name for name in all_names if re.match(regexp, name)]
    return names


class LoadService:
    class Result:
        def __init__(self, date, funds):
            self.last_updated = date
            self.funds = funds

    def __init__(self, db_path, min_days, max_missing_days):
        self._path = db_path
        self._min_days = min_days
        self._max_missing_days = max_missing_days
    
    def execute(self, fund_names):        
        load = Load(self._path, fund_names, self._min_days, self._max_missing_days)
        funds = load.execute()

        last_date = max([funds[key].index[-1].date() for key in funds])

        print("Loaded {0} funds. Last date: '{1}'".
              format(len(funds.keys()), last_date))

        return self.Result(last_date, funds)