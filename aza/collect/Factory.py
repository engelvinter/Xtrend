
from .Download import Download
from .Collect import Collect
from .CollectService import CollectService
from common.Store import Store

import datetime
import os


class Factory:
    def __init__(self, db_path):
        self._db_path = db_path

    def create_downloader(self, fund_id):
        return Download(fund_id)

    def create_collector(self, fund_ids):
        return Collect(fund_ids, self)

    def create_storer(self, funds):
        return Store(self._db_path, funds)

    def create_collect_service(self, fund_ids):
        last_updated = self._get_last_updated(self._db_path)
        return CollectService(fund_ids, last_updated, self)

    def _get_last_updated(self, db_path):
        actual_date = datetime.datetime(1999, 1, 1)
        try:
            file_name = os.path.join(db_path, "._last_updated.txt")
            with open(file_name, "r") as f:
                date_str = f.readline().rstrip()
                actual_date = datetime.strptime(date_str, "%Y-%m-%d")

            return actual_date.date()
        except FileNotFoundError:
            pass

        return actual_date.date()