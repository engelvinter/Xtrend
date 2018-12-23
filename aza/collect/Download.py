import urllib.parse
import urllib.request

import json


class Download:
    """ Downloads the datapoints of a fund from Avanza.
        Each datapoint consists of a timestamp and a NAV value
    """
    def __init__(self, fund_id):
        """
        Initiates the object
        :param fund_id: the id of the fund at Avanza
        """
        self._url = "https://www.avanza.se/ab/component/highstockchart/getchart/orderbook"
        self._fund_id = fund_id

    def create_aza_parameters(self, fund_id, period, resolution="DAY"):
        """
        Creates a parameter dictionary for the REST request
        :param fund_id: id of fund in avanza
        :param period: string, one of "month", "three_months", "this_year", "year", "three_years", "five_years", "ten_years"
        :param resolution: string, one of day, month
        :return: a dictionary containing the parameters needed for avanza
        """
        parameters = {"orderbookId": str(fund_id) ,
                      "chartType": "AREA",
                      "widthOfPlotContainer": 558,
                      "chartResolution": resolution,
                      "navigator": "true",
                      "percentage": "false",
                      "volume": "false",
                      "owners": "false",
                      "timePeriod": period,
                      "ta": []}

        return parameters

    def perform_json_post_request(self, url, params):
        """
        Performs a REST request using the parameters specified in argument 'params'
        Returns the JSON answer

        :param url: the url of the REST request
        :param params: parametst to be supplied with request
        :return: returns the JSON answer
        """
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')

        js = json.dumps(params).encode("utf-8")
        
        answer = urllib.request.urlopen(req, js)
        json_data = answer.read()

        data = json.loads(json_data)
        return data

    def execute(self):
        """
        Returns the datapoints containing the NAV values for the actual fund_id

        :return: the datapoints as an array containing tuples
                 the tuples consists of timestamp (seconds since 1970) and a NAV value
        """
        params = self.create_aza_parameters(self._fund_id, "three_months")
        data = self.perform_json_post_request(self._url, params)
        points = data['dataPoints']

        return points