"""
This module contains different operations using avanza fund data
Supports loading, filtering, and trend analysis of the data.
The trend analysis is based on Meb Fabers AGG which uses a compund
value which is the average of the averages (1, 3, 6 and 12 months).

The link to the ppm fund data is in LoadService._download_link

A typical flow might look like:
import aza.operations as op
op.load()                                       # load the latest ppm fund data

op.filter_name("SEB.*|Handelsb.*|Lannebo.*")    # only use funds form SEB,
                                                # Handelsbanken and Lannebo

op.agg(3)                                       # Pick the 3 top fonds
                                                # according to the compound
                                                # value
"""
from re import match
from .fund_summary.load.LoadService import LoadService

_orig_df = None
_df = None

_categories = None


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
    global _categories, _df
    _categories = None
    _df = _orig_df


def trend(nbr_funds=3):
    """
    This functions choses the funds with the highest compound value
    for each category. The compund value is calculated by an average
    of four other averages (12, 6, 3 ,1 month(s)).

    Parameters
    ----------
    `nbr_funds` : Default is 3, but possible to specify any amount

    Returns
    -------
    A panda dataframe containing the trending funds
    """
    trend = lambda x: x.nlargest(nbr_funds, "Compound")  # noqa: E731

    group = _df.groupby("Category")
    funds_per_category = group.apply(trend)[["Compound", "Sharpe", "Fee"]]

    if _categories:
        filter = " or ".join(["Category=='{}'".format(c) for c in _categories])
        funds_per_category = funds_per_category.query(filter)

    funds_per_category.name = "Trend {}".format(_df.name)

    return funds_per_category


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
    funds = trend(1)
    sorted_funds = funds.sort_values("Compound", ascending=False)
    picked_funds = sorted_funds.head(nbr_funds)
    picked_funds.name = "Aggressive Global Growth {}".format(_df.name)

    return picked_funds


def _filter_df(filter_series):
    """"Performs a filtering using the given True/False series."""
    global _df
    _df = _orig_df[filter_series]
    _df.name = _orig_df.name
