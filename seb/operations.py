
from seb.collect.CollectService import CollectService

from seb.load.LoadService import LoadService, fund_names

from seb.load.MakeStats import MakeStats

from datetime import datetime

DB_PATH = r"C:\Temp\db"

_funds = None
_date = datetime.now


def collect():
    cs = CollectService(DB_PATH, "2016-01-01")
    cs.execute()


def load():
    global _funds
    names = fund_names(DB_PATH)
    service = LoadService(DB_PATH, 10, 10)
    _funds = service.execute(names)
    ms = MakeStats(_date)
    stats = ms.execute(_funds)
    return stats


def set_date(date):
    global _date
    _date = date


