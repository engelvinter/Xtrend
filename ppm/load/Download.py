
import requests


class Download:
    def __init__(self, url, date):
        self._url = url
        self._date = date

    def execute(self):
        date_str = '{0:%Y-%m-%d}'.format(self._date)
        url_frm = '{0}/{1}/Statistik%20Premiepension%20{2}.xlsm'
        url = url_frm.format(self._url, self._date.year, date_str)

        req = requests.get(url)
        if req.status_code is not 200:
            txt = "Failed to download {0}, since status code is {1}"
            msg = txt.format(url, req.status_code)
            raise IOError(req.status_code, msg)

        return req.content
