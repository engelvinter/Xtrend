
from pandas import read_html, to_numeric

# https://www.avanza.se/fonder/lista.html


class Download:
    ARGUMENTS = ("disableSelection=false&"
                 "name=&page={0}&"
                 "sortField=CHANGE_IN_SEK_SINCE_THREE_MONTHS&"
                 "sortOrder=DESCENDING&"
                 "activeTab=history")

    def __init__(self, url, page):
        self._url = url
        self._page = page

    def _convert_col_to_numeric(self, df, column_name):
        # The column may contain '-' and consists of strings
        # remove all "-" in column
        # Finally convert to numeric
        df = df[df[column_name] != '-'].copy()
        # Convert the column to numeric
        df[column_name] = to_numeric(df[column_name])
        return df

    def _transform(self, df):
        # Rename columns - aligned with columns in ppm
        df.columns = ["", "Fund", "",
                      "", "One_month", "Three_months",
                      "Six_months", "Twelve_months", "Three_years",
                      "Five_years", ""]
        # drop all columns containing no description
        df = df.drop("", 1)
        df = self._convert_col_to_numeric(df, "Twelve_months")
        df = self._convert_col_to_numeric(df, "Three_years")
        df = self._convert_col_to_numeric(df, "Five_years")
        return df

    def execute(self):
        request_url = self._url + "?" + self.ARGUMENTS.format(self._page)
        resp_df = read_html(request_url)[1]
        resp_df = self._transform(resp_df)
        return resp_df
