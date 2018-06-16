
from . Factory import Factory
from io import BytesIO
import pandas as pd


class LoadService:
    def __init__(self):
        self._factory = Factory()

    def _load(self, month_lookback):
        download = self._factory.create_downloader(month_lookback)
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

    def execute(self):
        df = None
        month_lookback = 0

        while df is None:
            try:
                df = self._load(month_lookback)
            except OSError:
                month_lookback += 1
                if month_lookback > 2:
                    raise

        return df
