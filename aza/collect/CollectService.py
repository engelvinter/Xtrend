

class CollectService:
    """
    Collects fund timeseries by downloading from avanza and
    stores them into csv files
    """
    def __init__(self, fund_ids, last_updated, factory):
        """
        Creates a CollectService object

        :param fund_ids: array of tuples (fund name, fund id). This is fund to download and store
        :param last_updated: a date where all the funds were last updated
        :param factory: the factory object for this module
        """
        self._fund_ids = fund_ids
        self._factory = factory
        self._last_updated = last_updated

    def _slice_interval(self, funds, last_updated):
        slice : lambda ts : ts[last_updated:]
        sliced_dict = {name: funds[name][last_updated:] for name in funds}
        return sliced_dict

    def execute(self):
        """
        First downloads the timeseries of each fund,
        then stores/appends the timeseries to csv-files.
        """
        collect = self._factory.create_collector(self._fund_ids)
        funds = collect.execute()

        sliced_funds = self._slice_interval(funds, self._last_updated)

        s = self._factory.create_storer(sliced_funds)
        s.execute()