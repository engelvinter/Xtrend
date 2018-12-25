
from .Download import Download
from .Extract import Extract
from common.Store import Store
from .Collect import Collect
from .CollectService import CollectService
from common.LastStored import LastStored

import datetime
import os


class Factory:
    def __init__(self, db_path):
        self._db_path = db_path
        self._last = LastStored(self._db_path)

    def create_downloader(self, date):
        return Download("https://seb.se/pow/fmk/2100", date)

    def create_extractor(self, content, fund_callback):
        return Extract(content, fund_callback)

    def create_storer(self, funds):
        return Store(self._db_path, funds)

    def create_collector(self, funds):
        return Collect(funds, self)
    
    def create_collector_service(self):
        self._prepare_db()
        
        default_date = datetime.datetime(1994, 1, 1).date()        
        last_updated = self._last.get_last_stored(default_date)
        return CollectService(last_updated, self)

    def _prepare_db(self):
        if not os.path.exists(self._db_path):
            os.mkdir(self._db_path)