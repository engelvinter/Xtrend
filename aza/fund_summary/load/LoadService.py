from .DownloadHistory import DownloadHistory
from .DownloadCategory import DownloadCategory
from .DownloadOverview import DownloadOverview
from .DownloadFundIds import DownloadAzaFundIds

from .helper import remove_duplicates

from .NoDataException import NoDataException

from pandas import DataFrame, concat

from datetime import datetime

_download_link = "https://www.avanza.se/fonder/lista.html"


class LoadService:
    def __init__(self):
        pass

    def _download_history(self, page):
        # Fetch the page as a dataframe
        dw = DownloadHistory(_download_link, page)
        df = dw.execute()
        return df

    def _download_category(self, page):
        # Fetch the page as a dataframe
        dw = DownloadCategory(_download_link, page)
        df = dw.execute()
        return df

    def _download_overview(self, page):
        # Fetch the page as a dataframe
        dw = DownloadOverview(_download_link, page)
        df = dw.execute()
        return df

    def _download_fund_ids(self, page):        
        dw_fund_ids = DownloadAzaFundIds(_download_link, page)
        fund_ids_dict = dw_fund_ids.execute()
        return fund_ids_dict

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
        # remove any duplicates in index
        whole_df = remove_duplicates(whole_df)
        return whole_df

    def execute(self):
        df_hist = self._download_pages(self._download_history)
        df_cat = self._download_pages(self._download_category)
        df_overv = self._download_pages(self._download_overview)
        df_ids = self._download_pages(self._download_fund_ids)

        # Concat all the different tables into one
        df = concat([df_hist, df_cat, df_overv, df_ids], axis="columns")

        # Set time stamp
        df.name = datetime.now().strftime("%Y-%m-%d")
        # Remove all not a number
        df = df.dropna()

        return df