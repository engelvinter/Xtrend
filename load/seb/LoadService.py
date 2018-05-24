
from .Load import Load

import glob
import os.path
import os
import re

class LoadService:
    def __init__(self, db_path, min_days):
        self._path = db_path
        self._min_days = min_days
    
    def _list_fund_names(self, regexp = ".*"):
        files = glob.glob("./db/*.csv")
        extract_base = lambda fullpath :  os.path.splitext(os.path.basename(fullpath))[0]
        all_fund_names = [extract_base(fullpath) for fullpath in files]
        fund_names = [name for name in all_fund_names if re.match(regexp, name)]
        return fund_names

    def execute(self, *fund_names):
        names_to_load = []
        if len(fund_names) is 0:
            names_to_load = self._list_fund_names()
        else:
            names_to_load = self._list_fund_names("|".join(fund_names))
        
        l = Load(self._path, names_to_load, self._min_days)
        funds = l.execute()

        return funds