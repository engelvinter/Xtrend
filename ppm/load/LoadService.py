
from . Factory import Factory
from io import BytesIO
from datetime import datetime
import pandas as pd
import calendar


class LoadService:
    def __init__(self):
        self._factory = Factory()

    def _last_day_in_month(self, month):
        now = datetime.now()
        day = calendar.monthrange(now.year, month)[1]
        dt = datetime(now.year, month, day)
        return dt

    def _load_month(self, month):
        dt = self._last_day_in_month(month)
        download = self._factory.create_downloader(dt)
        excel_file = BytesIO(download.execute())

        xl = pd.ExcelFile(excel_file)

        df = xl.parse("Fondstatistik",
                      header=None,
                      skiprows=21,
                      names=['Id', 'Fund',  '', 'One_month', 'Three_months',
                             'Six_months', 'Twelve_months', 'Three_years',
                             'Five_years', 'Avg_five_years', 'Netto', 'Brutto',
                             'SD36', 'Sharpe', 'Valuta', '', '', '', '',
                             'Category', ''])

        df.name = '{0:%Y-%m-%d}'.format(dt)

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
