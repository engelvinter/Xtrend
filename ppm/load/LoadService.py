
from datetime import datetime
from . Factory import Factory
from io import BytesIO
import pandas as pd

class LoadService:
    def __init__(self):
        pass

    def execute(self):
        factory = Factory()
        download = factory.create_downloader()
        excel_file = BytesIO(download.execute())

        xl = pd.ExcelFile(excel_file)

        df = xl.parse("Fondstatistik",
                      header=None,
                      skiprows=21,
                      names=['Id', 'Name',  '', 'One_month', 'Three_months', 'Six_months', 'Twelve_months',
                     'Three_years', 'Five_years', 'Avg_five_years', 'Netto', 'Brutto', 'SD36',
                     'Sharpe', 'Valuta', '', '', '', '',
                     'Category', ''])

        return df