
from .Download import Download
from .Extract import Extract
from .Store import Store
from .Collect import Collect


class Factory:
    def __init__(self, db_path):
        self._db_path = db_path

    def create_downloader(self, date):
        return Download("https://seb.se/pow/fmk/2100", date)

    def create_extractor(self, content, fund_callback):
        return Extract(content, fund_callback)

    def create_storer(self, funds):
        return Store(self._db_path, funds)

    def create_collector(self, funds):
        return Collect(funds, self)
