import requests
import lxml.html as lh
import pandas as pd
import re

from .NoDataException import NoDataException


class DownloadAzaFundIds:
    """ This class downloads all ids of fund at Avanza """

    ARGUMENTS = ("disableSelection=false&"
                 "name=&page={0}&"
                 "sortField=CHANGE_IN_SEK_SINCE_THREE_MONTHS&"
                 "sortOrder=DESCENDING&"
                 "activeTab=overview")

    def __init__(self, url, page):
        self._url = url
        self._page = page

    def _get_text(self, item):
        """ Returns the text of html node"""
        return item.text.strip()

    def _get_id(self, item):
        """ Returns the fund id from an html link of Avanza """
        link = item.attrib["href"]
        # Searches for a string containing an arbitrary number of text characters (\D+)
        # then an arbitrary number of figures (\d+)
        # Extract the figures since this is the fund id
        p = re.compile("\D+(\d+)")
        m = p.match(link)
        if m is None:
            # Found nothing
            return ""
        fund_id = m.group(1)
        return fund_id

    def _download_page(self, url):
        request_url = url + "?" + self.ARGUMENTS.format(self._page)
        page = requests.get(request_url)
        return page

    def _download_fund_id_dict(self, url):
        """ Returns a dictionary containing fund_name:[fund_id] by downloading from avanzas site """
        page = self._download_page(url)
        doc = lh.fromstring(page.content)
        # Search for all a-elements (links) having an href attribute containing the text 'om-fonden'
        xpath_expr = "//a[contains(@href, 'om-fonden')]"
        links = doc.xpath(xpath_expr)
        if len(links) == 0:
            raise NoDataException()
        # Create dictionary fund_name:fund_id
        dict = {self._get_text(item): [self._get_id(item)] for item in links}
        return dict

    def _create_dataframe(self, dict):
        df = pd.DataFrame.from_dict(dict, orient="index")
        df.index.name = "Fund"
        df.columns = ["AzaId"]
        return df

    def execute(self):
        """
        Returns a DataFrame containing the columns fund name and fund avanza id 
        by downloading from avanzas site
        """        
        dict = self._download_fund_id_dict(self._url)
        df = self._create_dataframe(dict)
        return df


