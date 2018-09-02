
from seb.collect.CollectService import CollectService

from seb.load.LoadService import LoadService, fund_names

from seb.load.MakeStats import MakeStats

from datetime import datetime

from re import match

DB_PATH = r"C:\Temp\db"

_funds = None
_orig_df = None
_df = None

_date = datetime.now()


def collect():
    cs = CollectService(DB_PATH, "2016-01-01")
    cs.execute()


def load():
    global _funds, _orig_df, _df, _date
    names = fund_names(DB_PATH)
    service = LoadService(DB_PATH, 10, 10)
    _funds = service.execute(names)
    ms = MakeStats(_date)
    _orig_df = _df = ms.execute(_funds)


def set_date(date):
    global _date
    _date = date


def reset():
    """ Resets into no filters """
    global _df
    _df = _orig_df


def filter_name(regexp):
    """
    Specify which funds to use when doing trend analysis.
    A regexp is given as argument that is matched with
    the name of each fund.

    Parameters
    ----------
    `regexp` : A regexp that matches the name of funds
               e.g. "SEB.*|Swedbank.*" to match all funds
               of SEB and Swedbank
    """
    def fund_match(x):
        return match(regexp, x) is not None
        
    matches = _orig_df.apply(axis=1, func=lambda x: fund_match(x.name))
    _filter_df(matches)


def _filter_df(filter_series):
    """"Performs a filtering using the given True/False series."""
    global _df
    _df = _orig_df[filter_series]
    _df.name = _orig_df.name