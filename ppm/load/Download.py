
import requests


class Download:
    SUCCESS_CODE = 200

    def __init__(self, url, date):
        self._url = url
        self._date = date

    def _get_date_str(self, date):
        return '{0:%Y-%m-%d}'.format(date)

    def _create_link(self, pre_url, date, file_version=""):
        url_frm = '{0}/{1}/Statistik%20Premiepension%20{2}{3}.xlsm'
        complete_url = url_frm.format(pre_url, 
                                      date.year, 
                                      self._get_date_str(date),
                                      file_version)
        return complete_url
    
    def _create_io_error(self, url, response):
        txt = "Failed to download {0}, since status code is {1}"
        msg = txt.format(url, response.status_code)
        return IOError(response.status_code, msg)

    def execute(self):
        date_str = self._get_date_str(self._date)
        print("Trying to dowload ", date_str)

        versions = ["", "v2", "v3", "v4"]

        for version in versions:            
            url = self._create_link(self._url, self._date, "." + version)
            resp = requests.get(url)
            if resp.status_code is self.SUCCESS_CODE:
                break

        if resp.status_code is not self.SUCCESS_CODE:
            raise self._create_io_error(url, resp)

        print("Succeded downloading ", date_str)

        return resp.content
