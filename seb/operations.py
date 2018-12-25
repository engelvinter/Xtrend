
from seb.collect.CollectService import CollectService

from seb.load.LoadService import LoadService, fund_names

from seb.load.MakeStats import MakeStats

from datetime import datetime

from re import match

from common.assign_date import assign_date

from common.Graph import Graph

from common.functions import above_ma as above_ma_ts
from common.functions import read_fund_groups

from .collect.Factory import Factory

import pandas as pd

DB_PATH = r"C:\Temp\db"

GROUP_PATH = r"C:\Temp\Groups.ini"

_funds = None
_orig_df = None
_df = None

_date = datetime.now().date()


def collect():
    """
    Collects data from SEB of funds and stores into file db.
    The path of the file db is within this module (DB_PATH)
    """
    f = Factory(DB_PATH)
    cs = f.create_collector_service()
    cs.execute()


def load(nbr_funds=10000):
    """
    This function loads the navs (net asset values) from file db of funds and then calcualtes
    statistics of each fund into a dataframe.
    """
    global _funds, _orig_df, _df, _date
    names = fund_names(DB_PATH)[:nbr_funds]

    service = LoadService(DB_PATH, 10, 10)
    result = service.execute(names)
    _funds = result.funds

    ms = MakeStats(result.last_updated, 10)
    _df = ms.execute(result.funds)

    _orig_df = _df


def apply_groups(full_path=GROUP_PATH):
    """
    Applies a group ini file to the statistics. 
    """
    global _get_funds
    fund_to_group = read_fund_groups(full_path)
    _set_groups(fund_to_group)
    _get_funds = lambda: trend("Group", 1)  # noqa: E731


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
    global _date, _orig_df, _df
    _date = assign_date(date)
    ms = MakeStats(_date, 10)
    _orig_df = _df = ms.execute(_funds)


def reset():
    """ Resets into no filters """
    global _df, _date, _get_funds
    _df = _orig_df
    _date = datetime.now().date()
    _get_funds = _all_funds


def filter_name(regexp):
    """
    Specify which funds to use when doing trend analysis
    based on the fund name.
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


def filter_above_ma(nbr_days):
    """
    Specifies to only use the funds that are above
    their moving average of nbr_days

    Parameters
    ----------
    `nbr_days` : number days to use in moving average

    """
    def calc(name):
        ts = _funds[name].nav[:_date]
        return above_ma_ts(nbr_days, ts)

    result = _df.index.map(calc).tolist()
    _filter_df(result)


def best(nbr_funds=5):
    """
    This function chooces the top funds in three months perspective.

    Parameters
    ----------
    `nbr_funds` : number of funds chosen
    """
    df_funds = _get_funds()
    sorted_funds = df_funds.sort_values("Three_months", ascending=False)["Three_months"]
    return sorted_funds[0:nbr_funds]


def trend(column_name, nbr_funds=3):
    """
    This functions chooses the funds with the highest compound value
    for each group. The compund value is calculated by an average
    of four other averages (12, 6, 3 ,1 month(s)).

    Returns
    -------
    A panda dataframe containing the best fund of each group
    """
    trend = lambda x: x.nlargest(nbr_funds, "Compound")  # noqa: E731

    group = _df.groupby(column_name)
    
    funds = group.apply(trend)[["Compound"]]

    funds.name = "Best groups {}".format(_df.name)

    return funds

def agg(nbr_funds):
    """
    Aggresive Global - Meb Faber
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
    df_funds = _get_funds()
    sorted_funds = df_funds.sort_values("Compound", ascending=False)["Compound"]
    picked_funds = sorted_funds.head(nbr_funds)
    picked_funds.name = "Aggressive Global Growth {}".format(_df.name)
    return picked_funds


def graph(fund_name):
    """
    Shows a graph showing the return of the given fund in percent.
    
    Parameters
    ----------
    `fund_name` : the name of the fund
    """
    s = _funds[fund_name]['nav']
    graph = Graph(fund_name, s)
    graph.show()    


def value(fund_name):
    """

    Parameters
    ----------
    `fund_name` : the name of the fund

    Returns
    -------
    The nav (net asset vaue) of the fund at the given date
    Use set_date to set the date
    """
    ts = _funds[fund_name]
    if _date not in ts.index:
        msg = "The date '{0}' does not exist in the timeseries".format(_date)
        raise Exception(msg)
    return ts.loc[_date].nav


"""
Private functions of module
"""


def _filter_df(filter_series):
    """"Performs a filtering using the given True/False series."""
    global _df
    _df = _orig_df[filter_series]
    _df.name = _orig_df.name


def _set_groups(fund_to_group):
    """
    Connects funds with different groups

    Parameters
    ----------
    `fund_to_group` : dictionary populated by fund name => group name 
    """
    global _df
    s = pd.Series(fund_to_group)
    _df["Group"] = s


def _all_funds():
    """
    Returns
        Returns all available funds
        In case of
            using groups the best fund of each group is returned
    """
    return _df


_get_funds = _all_funds
