from . Download import Download
from pandas import DataFrame

_download_link = "https://www.avanza.se/fonder/lista.html"


class LoadService:
    def __init__(self):
        pass

    def execute(self):
        page = 1
        whole_df = DataFrame()
        try:
            while(True):
                print("Page ", page)
                dw = Download(_download_link, page)
                df = dw.execute()
                whole_df = whole_df.append(df)   # verify_integrity=True
                page += 1
        except Download.NoData:
            pass

        return whole_df