
from pandas import read_html


class Download:
    ARGUMENTS = ("disableSelection=false&"
                 "name=&page={0}&"
                 "sortField=CHANGE_IN_SEK_SINCE_THREE_MONTHS&"
                 "sortOrder=DESCENDING&"
                 "activeTab=history")

    def __init__(self, url, page):
        self._url = url
        self._page = page
    
    def execute(self):
        request_url = self._url + "?" + self.ARGUMENTS.format(self._page)
        resp_df = read_html(request_url)[1]
        return resp_df    
