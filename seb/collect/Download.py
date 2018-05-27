
import requests

class Download:
    def __init__(self, url, date):
        self._url = url
        self._date = date

    def execute(self):
        date_str = '{0:%Y-%m-%d}'.format(self._date)
        url = '{0}/fonder_{1}.TXT'.format(self._url, date_str)
        req = requests.get(url)
        if req.status_code is not 200:
            raise IOError(req.status_code, "Failed to download {0}, since status code is {1}".format(url, req.status_code))

        return req.content.decode("iso-8859-1")
