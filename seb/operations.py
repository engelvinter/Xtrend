
from seb.load.LoadService import LoadService, fund_names

from datetime import datetime

from common.Graph import Graph

from common.functions import read_fund_groups

from .collect.Factory import Factory

from .model.FundView import FundView

from .model.Evaluate import Evaluate

DB_PATH = r"C:\Temp\db"

GROUP_PATH = r"C:\Temp\Groups.ini"

_funds = None
_view = None
_evaluate = None

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
    global _funds, _view, _evaluate
    names = fund_names(DB_PATH)[:nbr_funds]

    service = LoadService(DB_PATH, 10, 10)
    result = service.execute(names)
    _funds = result.funds
    _view = FundView(result)
    _evaluate = Evaluate(_view)


def apply_groups(full_path=GROUP_PATH):
    """
    Applies a group ini file to the statistics. 
    """
    fund_to_group = read_fund_groups(full_path)
    _view.set_groups(fund_to_group)


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
    _view.available_funds(year, regexp)


def set_date(date):
    """
    Sets a new date. This new date will be used as
    the last date in trend calculations.

    Parameters
    ----------
    `date` : the actual date
    """
    global _date
    _view.set_date(date)


def reset():
    """ Resets into no filters """
    _view.reset()


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
    _view.filter_name(regexp)


def filter_above_ma(nbr_days):
    """
    Specifies to only use the funds that are above
    their moving average of nbr_days

    Parameters
    ----------
    `nbr_days` : number days to use in moving average

    """
    _view.filter_above_ma(nbr_days)


def best(nbr_funds=5):
    """
    This function chooces the top funds in three months perspective.

    Parameters
    ----------
    `nbr_funds` : number of funds chosen
    """
    return _evaluate.best(nbr_funds)


def trend(column_name, nbr_funds=3):
    """
    This functions chooses the funds with the highest compound value
    for each group. The compund value is calculated by an average
    of four other averages (12, 6, 3 ,1 month(s)).

    Returns
    -------
    A panda dataframe containing the best fund of each group
    """
    return _evaluate.trend(column_name, nbr_funds)


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
    return _evaluate.agg(nbr_funds)


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
    return _view.value(fund_name)