
from .Download import Download
from .Collect import Collect
from .CollectService import CollectService
from common.Store import Store
from common.LastStored import LastStored

import datetime
import os


class Factory:
    def __init__(self, db_path):
        self._db_path = db_path
        self._last = LastStored(self._db_path)

    def create_downloader(self, fund_id):
        return Download(fund_id)

    def create_collector(self, fund_ids):
        return Collect(fund_ids, self)

    def create_storer(self, funds):
        return Store(self._db_path, funds)

    def create_collect_service(self, fund_ids):
        default_date = datetime.datetime(1999, 1, 1).date()        
        last_updated = self._last.get_last_stored(default_date)
        return CollectService(fund_ids, last_updated, self)
