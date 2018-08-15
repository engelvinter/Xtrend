from pandas import read_html, to_numeric


class Download:
    ARGUMENTS = ("disableSelection=false&"
                 "name=&page={0}&"
                 "sortField=CHANGE_IN_SEK_SINCE_THREE_MONTHS&"
                 "sortOrder=DESCENDING&"
                 "activeTab=history")

    class NoData(Exception):
        pass

    def __init__(self, url, page):
        self._url = url
        self._page = page

    def _convert_col_to_percent(self, df, column_name):
        if df[column_name].dtype == "O":  # Object column
            # The column may contain '-' and consists of strings
            # remove all "-" (no value) in column and make a copy
            # containing only funds which has made more than a year.
            df = df[df[column_name] != '-'].copy()
            # Convert the column to numeric
            df[column_name] = to_numeric(df[column_name])

        df[column_name] = df[column_name].div(100)

        return df

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
        df = self._convert_col_to_percent(df, "Twelve_months")
        df = self._convert_col_to_percent(df, "Six_months")
        df = self._convert_col_to_percent(df, "Three_months")
        df = self._convert_col_to_percent(df, "One_month")
        return df

    def execute(self):
        request_url = self._url + "?" + self.ARGUMENTS.format(self._page)
        resp_df = read_html(request_url)
        if len(resp_df) == 1:
            raise Download.NoData()
        resp_df = self._transform(resp_df[1])
        return resp_df
