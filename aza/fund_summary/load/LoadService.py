from .DownloadHistory import DownloadHistory
from .DownloadCategory import DownloadCategory
from .NoDataException import NoDataException

from pandas import DataFrame

_download_link = "https://www.avanza.se/fonder/lista.html"


class LoadService:
    def __init__(self):
        pass

    def _download_history(self, page):
        # Fetch the page as a dataframe
        dw = DownloadHistory(_download_link, page)
        df = dw.execute()
        # remove any duplicates in index
        df = df[~df.index.duplicated()]
        return df

    def _download_category(self, page):
        # Fetch the page as a dataframe
        dw = DownloadCategory(_download_link, page)
        df = dw.execute()
        # remove any duplicates in index
        df = df[~df.index.duplicated()]
        return df

    def _download_pages(self, download_func):
        page = 1
        whole_df = DataFrame()
        # Start at page 1, iterate page by page until no data
        try:
            while(True):
                print("Page ", page)
                df = download_func(page)
                whole_df = whole_df.append(df)   # verify_integrity=True
                page += 1
        except NoDataException:
            pass
        return whole_df

    def execute(self):
        df_hist = self._download_pages(self._download_history)
        df_cat = self._download_pages(self._download_category)
        df_hist["Category"] = df_cat["Category"]
        return df_hist