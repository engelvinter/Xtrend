from pandas import read_html

from .helper import convert_col_to_percent

from .NoDataException import NoDataException


class DownloadHistory:
    ARGUMENTS = ("disableSelection=false&"
                 "name=&page={0}&"
                 "sortField=CHANGE_IN_SEK_SINCE_THREE_MONTHS&"
                 "sortOrder=DESCENDING&"
                 "activeTab=history")

    def __init__(self, url, page):
        self._url = url
        self._page = page

    def _transform(self, df):
        # Rename columns - aligned with columns in ppm
        df.columns = ["", "Fund", "",
                      "", "One_month", "Three_months",
                      "Six_months", "Twelve_months", "Three_years",
                      "Five_years", ""]
        df.set_index("Fund", inplace=True)
        # drop all columns containing no description
        df = df.drop("", 1).copy()
        # convert columns to floating percentage 0.00 - 1.00
        df = convert_col_to_percent(df, "Twelve_months")
        df = convert_col_to_percent(df, "Six_months")
        df = convert_col_to_percent(df, "Three_months")
        df = convert_col_to_percent(df, "One_month")
        return df

    def execute(self):
        # Fetch page using url
        request_url = self._url + "?" + self.ARGUMENTS.format(self._page)
        resp_df = read_html(request_url)
        # Contains data? Shall contain 2 frames
        if len(resp_df) != 2:
            raise NoDataException()
        # Transfrom frame into correct format
        resp_df = self._transform(resp_df[1])
        return resp_df
