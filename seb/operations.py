
from seb.collect.CollectService import CollectService

from seb.load.LoadService import LoadService, fund_names

from seb.load.MakeStats import MakeStats

from datetime import datetime

from re import match

from common.assign_date import assign_date

DB_PATH = r"C:\Temp\db"

_funds = None
_orig_df = None
_df = None

_date = datetime.now()


def collect():
    """
    Collects data from SEB of funds and stores into file db.
    The path of the file db is within this module (DB_PATH)
    """
    cs = CollectService(DB_PATH, "2016-01-01")
    cs.execute()


def load():
    """
    This function loads the quotes from file db of funds and then calcualtes
    statistics of each fund into a dataframe.
    """
    global _funds, _orig_df, _df, _date
    names = fund_names(DB_PATH)
    service = LoadService(DB_PATH, 10, 10)
    _funds = service.execute(names)
    ms = MakeStats(_date)
    _orig_df = _df = ms.execute(_funds)


def avail_funds_during_year(year, regexp=".*"):
    """
    Returns funds that ara available during given year
    Available is defined as it has been possible to buy
    the fund throughout the whole year.

    Parameters
    ----------
    `year` : the given year
    `regexp` : optional, filter using the given regexp

    Returns
    -------
    a list of fund names
    """
    avail_funds = []
    start_year = datetime(year, 1, 1)
    end_year = datetime(year, 12, 31)
    for fund, data in _funds.items():
        if match(regexp, fund) is None:
            continue
        start_fund = data.index[0]
        end_fund = data.index[-1]
        if start_fund < start_year and end_fund > end_year:
            avail_funds.append(fund)
    return avail_funds


def set_date(date):
    """
    Sets a new date. This new date will be used as
    the last date in trend calculations.

    Parameters
    ----------
    `date` : the actual date
    """
    global _date, _df
    _date = assign_date(date)
    ms = MakeStats(_date)
    _df = ms.execute(_funds)


def reset():
    """ Resets into no filters """
    global _df, _date
    _df = _orig_df
    _date = datetime.now()


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


def agg(nbr_funds):
    """
    Picks the top trending funds using the compound
    value. The compound value is calculated by an average
    of four other averages (12, 6, 3 ,1 month(s)).

    Parameters
    ----------
    `nbr_funds` : number of funds to pick, must be less than number of
                  categories.

    Returns
    -------
    A panda series containing the trending funds
    """
    sorted_funds = _df.sort_values("Compound", ascending=False)["Compound"]
    picked_funds = sorted_funds.head(nbr_funds)
    picked_funds.name = "Aggressive Global Growth {}".format(_df.name)
    return picked_funds


def _filter_df(filter_series):
    """"Performs a filtering using the given True/False series."""
    global _df
    _df = _orig_df[filter_series]
    _df.name = _orig_df.name