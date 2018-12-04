"""
This module contains different operations using avanza fund data
Supports loading, filtering, and trend analysis of the data.
The trend analysis is based on Meb Fabers AGG which uses a compund
value which is the average of the averages (1, 3, 6 and 12 months).

The link to the ppm fund data is in LoadService._download_link

A typical flow might look like:
import aza.operations as op
op.load()                                       # load the latest ppm fund data

op.apply_groups()                               # reads the group.ini file and 
                                                # applies group names to
                                                # the fund dataset.

op.filter_name("SEB.*|Handelsb.*|Lannebo.*")    # only use funds form SEB,
                                                # Handelsbanken and Lannebo

op.agg(3)                                       # Pick the 3 top fonds
                                                # according to the compound
                                                # value
"""
from re import match
from .fund_summary.load.LoadService import LoadService

from common.functions import read_fund_groups

import pandas as pd

_orig_df = None
_df = None

_categories = None

GROUP_PATH = r"C:\Temp\Groups.ini"


def load():
    """
    This function loads the current statistics of the funds from avanza
    into a dataframe.
    """

    global _df, _orig_df
    ls = LoadService()
    _df = ls.execute()
    _df["Compound"] = (_df.Twelve_months +
                       _df.Six_months +
                       _df.Three_months +
                       _df.One_month) / 4
    _orig_df = _df


def apply_categories():
    """Use catogies defined by Avanza"""
    global _get_funds
    _get_funds = lambda: trend("Category", 1)  # noqa: E731


def apply_groups(full_path=GROUP_PATH):
    """Use own defined groups of funds"""
    global _get_funds
    fund_to_group = read_fund_groups(full_path)
    _set_groups(fund_to_group)
    _get_funds = lambda: trend("Group", 1)  # noqa: E731


def categories():
    """ Returns a list of categories from the funds """
    return _df.Category.unique()


def filter_categories(categories):
    """
    Specify which categories to use when doing trend analysis

    Parameters
    ----------
    `categories` : list of categories to use
    """
    global _categories
    _categories = categories


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


def filter_max_fee(max_fee):
    """
    Specify the max fee for the funds when doing trend analysis

    Parameters
    ----------
    `max_fee` : the max fee in percent for a fund e.g 1.2

    """
    matches = _orig_df.apply(axis=1, func=lambda x: x.Fee < max_fee)
    _filter_df(matches)


def filter_min_sharpe(min_sharpe):
    """
    Specify the minimal sharp limit for the funds when doing trend analysis

    Parameters
    ----------
    `min_sharpe` : the minimal sharpe limit e.g. 1.0

    """
    matches = _orig_df.Sharpe >= min_sharpe
    _filter_df(matches)


def reset():
    """ Resets into no filters """
    global _categories, _get_funds, _df
    _categories = None
    _get_funds = _all_funds
    _df = _orig_df


def trend(column_name, nbr_funds=3):
    """
    This functions choses the funds with the highest compound value
    for each unique column value. The compund value is calculated by 
    an average of four other averages (12, 6, 3 ,1 month(s)).

    Parameters
    ----------
    `column_name` : The name of the column which creates groups of funds
                    for each unique column value
    `nbr_funds`   : Default is 3, but possible to specify any amount

    Returns
    -------
    A panda dataframe containing the trending funds
    """
    trend = lambda x: x.nlargest(nbr_funds, "Compound")  # noqa: E731

    groups = _df.groupby(column_name)
    
    funds_per_unique_value = groups.apply(trend)[["Compound"]]

    if _categories:
        filter = " or ".join(["Category=='{}'".format(c) for c in _categories])
        funds_per_unique_value = funds_per_unique_value.query(filter)

    funds_per_unique_value.name = "Trend {}".format(_df.name)

    return funds_per_unique_value


def agg(nbr_funds):
    """
    Picks the top trending funds across all categories using the compund
    value. The compund value is calculated by an average
    of four other averages (12, 6, 3 ,1 month(s)).

    Parameters
    ----------
    `nbr_funds` : number of funds to pick, must be less than number of
                  categories.

    Returns
    -------
    A panda dataframe containing the trending funds
    """
    funds = _get_funds()
    sorted_funds = funds.sort_values("Compound", ascending=False)
    picked_funds = sorted_funds.head(nbr_funds)["Compound"]
    picked_funds.name = "Aggressive Global Growth {}".format(_df.name)

    return picked_funds


def _filter_df(filter_series):
    """"Performs a filtering using the given True/False series."""
    global _df
    _df = _orig_df[filter_series]
    _df.name = _orig_df.name


"""
Private functions of module
"""


def _all_funds():
    """
    Returns
        Returns all available funds
        In case of
            using groups the best fund of each group is returned
            using categories the best fund of each category is returned
    """
    return _df


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


_get_funds = _all_funds
