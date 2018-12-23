import os

from .LastStored import LastStored

from datetime import datetime

class Store:
    """
    Stores NAV timeseries of funds down to csv files.
    """
    def __init__(self, db_path, funds):
        """
        Creates a Store object

        :param db_path: The path to file directory where fund csv files are going to be stored
        :param funds: a dictionary of fund_name : timeseries of NAV values
        """
        self._path = db_path
        self._funds = funds
        self._last = LastStored(self._path)
        self._now = datetime.now().date()

    def execute(self):
        """
        Iterates through all the funds and appends the timeseries to an already existing
        timeseries in a csv file.
        """
        for fund in self._funds:
            try:
                filename = "{0}.csv".format(fund)
                filepath = os.path.join(self._path, filename)
                header = False if os.path.isfile(filepath) else True

                with open(filepath, 'a') as f:
                    self._funds[fund].to_csv(f, header=header)
            except IOError as e:
                print(e)

        self._last.set_last_stored(self._now)