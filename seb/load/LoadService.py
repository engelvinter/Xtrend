
from .Load import Load

import glob
import os.path
import os
import re


def fund_names(db_path, regexp = ".*", ext=".csv"):
    files = glob.glob("{}/*{}".format(db_path, ext))
    extract_base = lambda fullpath :  os.path.splitext(os.path.basename(fullpath))[0]
    all_names = [extract_base(fullpath) for fullpath in files]
    names = [name for name in all_names if re.match(regexp, name)]
    return names


class LoadService:
    def __init__(self, db_path, min_days, max_missing_days):
        self._path = db_path
        self._min_days = min_days
        self._max_missing_days = max_missing_days
    
    def execute(self, fund_names):        
        l = Load(self._path, fund_names, self._min_days, self._max_missing_days)
        funds = l.execute()

        return funds