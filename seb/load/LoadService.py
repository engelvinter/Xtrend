
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
        self._date_file = os.path.join(db_path, "._last_updated.txt")
    
    def execute(self, fund_names):        
        load = Load(self._path, fund_names, self._min_days, self._max_missing_days)
        funds = load.execute()

        date = self._get_last_updated(self._date_file)

        print("Loaded {0} funds. They were last updated '{1}'".
              format(len(funds.keys()), date))

        return self.Result(date, funds)

    def _get_last_updated(self, fullpath):
        actual_date = None
        with open(fullpath, "r") as f:
            date_str = f.readline().rstrip()
            actual_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return actual_date