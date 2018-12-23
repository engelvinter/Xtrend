
import pandas as pd
import datetime


class Collect:
    """
    Collects the NAV values as a Panda timeseries for each specified fund id
    """
    def __init__(self, fund_ids, factory):
        """
        Creates a Collector object
        :param fund_ids: array of tuples consisting of (fund name, fund id)
        :param factory: factory object able to create a downloader helper object
        """
        self._fund_ids = fund_ids
        self._factory = factory

    def _to_timeseries(self, points):
        """
        Converts to a Panda timeseries
        :param points: an array of tuples where typle is a timestamp and a NAV value
        :return: a Panda timeseries
        """
        to_date = lambda ts: datetime.datetime.fromtimestamp(ts).date()
        dict_points = {to_date(ts / 1000): nav for ts, nav in points}
        series = pd.Series(dict_points, name="nav")
        series.index.name = "date"

        return series

    def _download(self, fund_id):
        """Downloads the datapoints of a fund and returns a timeseries"""
        dw = self._factory.create_downloader(fund_id)
        points = dw.execute()

        ts = self._to_timeseries(points)
        return ts.dropna()

    def execute(self):
        """Returns a dictionary where each item is fund name : timseries of NAV values"""
        return {name: self._download(id) for name, id in self._fund_ids}

