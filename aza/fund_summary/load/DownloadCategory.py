from pandas import read_html

from .NoDataException import NoDataException


class DownloadCategory:
    ARGUMENTS = ("disableSelection=false&"
                 "name=&page={0}&"
                 "sortField=CHANGE_IN_SEK_SINCE_THREE_MONTHS&"
                 "sortOrder=DESCENDING&"
                 "activeTab=misc")

    def __init__(self, url, page):
        self._url = url
        self._page = page

    def _transform(self, df):
        # Rename columns - aligned with columns in ppm
        df.columns = ["", "Fund", "Category",
                      "Broker", "Size", "Start_date", "Owners", ""]
        # Name of fund is index
        df.set_index("Fund", inplace=True)
        # drop all columns having empty column name i.e. not used
        df = df.drop("", axis=1)
        return df

    def execute(self):
        # Fetch page
        request_url = self._url + "?" + self.ARGUMENTS.format(self._page)
        resp_df = read_html(request_url)
        # Contains data? Shall contain 2 frames
        if len(resp_df) != 2:
            raise NoDataException()
        # Transfrom frame into correct format
        resp_df = self._transform(resp_df[1])
        return resp_df