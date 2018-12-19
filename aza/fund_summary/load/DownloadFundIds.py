
import requests
import lxml.html as lh
import re


class DownloadAzaFundIds:
    """ This class downloads all ids of fund at Avanza """
    def __init__(self):
        self._url = 'https://www.avanza.se/fonder/lista.html'

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

    def _download_fund_id_dict(self, url):
        """ Returns a dictionary containing fund_name:fund_id by downloading from avanzas site """
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        # Search for all a-elements (links) having an href attribute containing the text 'om-fonden'
        xpath_expr = "//a[contains(@href, 'om-fonden')]"
        links = doc.xpath(xpath_expr)
        # Create dictionary fund_name:fund_id
        dict = {self._get_text(item):self._get_id(item) for item in links}
        return dict

    def execute(self):
        """ Returns a dictionary containing fund_name:fund_id by downloading from avanzas site """
        dict = self._download_fund_id_dict(self._url)
        return dict

