
from . Factory import Factory
from io import BytesIO
from datetime import datetime
import pandas as pd


class LoadService:
    def __init__(self):
        self._factory = Factory()

    def _load_month(self, month):
        download = self._factory.create_downloader(month)
        excel_file = BytesIO(download.execute())

        xl = pd.ExcelFile(excel_file)

        df = xl.parse("Fondstatistik",
                      header=None,
                      skiprows=21,
                      names=['Id', 'Name',  '', 'One_month', 'Three_months',
                             'Six_months', 'Twelve_months', 'Three_years',
                             'Five_years', 'Avg_five_years', 'Netto', 'Brutto',
                             'SD36', 'Sharpe', 'Valuta', '', '', '', '',
                             'Category', ''])

        return df

    def _load_available_month(self, month):
        df = None
        while df is None:
            try:
                df = self._load_month(month)
            except OSError:
                month -= 1
                if month < 1:
                    raise

        return df

    def execute(self, month=None):
        if not month:
            month = datetime.now().month
            df = self._load_available_month(month)
        else:
            df = self._load_month(month)

        return df
