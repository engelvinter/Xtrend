
import requests
#Statistik%20Premiepension%202018-04-30.xlsm


class Download:
    def __init__(self, url, date):
        self._url = url
        self._date = date

    def execute(self):
        date_str = '{0:%Y-%m-%d}'.format(self._date)
        url = '{0}/{1}/Statistik%20Premiepension%20{2}.xlsm'.format(self._url,
                                                                    self._date.year,
                                                                    date_str)
        req = requests.get(url)
        if req.status_code is not 200:
            raise IOError(req.status_code, "Failed to download {0}, since status code is {1}".format(url, req.status_code))

        return req.content
