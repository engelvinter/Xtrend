import pandas as pd

import os

class Store:
    def __init__(self, db_path, funds):
        self._funds = funds
        self._path = db_path
    
    def execute(self):
        for fund in self._funds:
            try:
                filename = "{0}.csv".format(fund)
                filepath = os.path.join(self._path, filename)
                header = False if os.path.isfile(filepath) else True
                with open(filepath, 'a') as f:
                    self._funds[fund].to_csv(f, header = header)
            except IOError as e:
                print(e)

            