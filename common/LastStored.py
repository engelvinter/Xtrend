
from datetime import datetime

import os


class LastStored:
    def __init__(self, db_path):
        self._path = db_path
        self._file = os.path.join(self._path, "._last_updated.txt") 
    
    def set_last_stored(self, actual_date):
        date_str = "{0:%Y-%m-%d}".format(actual_date)
        with open(self._file, "w") as f:
            f.write(date_str)

    def get_last_stored(self, default_date):
        if not os.path.isfile(self._file):
            return default_date

        with open(self._file, "r") as f:
            date_str = f.readline().rstrip()
            actual_date = datetime.strptime(date_str, "%Y-%m-%d")

        return actual_date.date()
    
    