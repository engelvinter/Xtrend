from re import match
from .load.LoadService import LoadService

_orig_df = None
_df = None

_categories = None


def load(month=None):
    global _df, _orig_df
    ls = LoadService()
    _df = ls.execute(month)
    _df["Compound"] = (_df.Twelve_months +
                       _df.Six_months +
                       _df.Three_months +
                       _df.One_month) / 4
    _orig_df = _df


def categories():
    return _df.Category.unique()


def filter_categories(categories):
    global _categories
    _categories = categories


def filter_name(regexp):
    matches = _orig_df.Fund.apply(lambda x: match(regexp, x) is not None)
    _filter_df(matches)


def filter_min_sharpe(min_sharpe):
    matches = _orig_df.Sharpe >= min_sharpe
    _filter_df(matches)


def reset():
    global _categories, _df
    _categories = None
    _df = _orig_df


def trend(nbr_funds=3):
    trend = lambda x: x.nlargest(nbr_funds, "Compound")  # noqa: E731

    group = _df.groupby("Category")
    funds_per_category = group.apply(trend)[["Fund", "Compound",
                                             "SD36", "Sharpe"]]

    if _categories:
        filter = " or ".join(["Category=='{}'".format(c) for c in _categories])
        funds_per_category = funds_per_category.query(filter)

    funds_per_category.name = "Trend {}".format(_df.name)

    return funds_per_category


def agg(nbr_funds):
    funds = trend(1)
    sorted_funds = funds.sort_values("Compound", ascending=False)
    picked_funds = sorted_funds.head(nbr_funds)
    picked_funds.name = "Aggressive Global Growth {}".format(_df.name)

    return picked_funds


def _filter_df(filter_series):
    global _df
    _df = _orig_df[filter_series]
    _df.name = _orig_df.name
    