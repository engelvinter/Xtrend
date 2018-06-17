
from .load.LoadService import LoadService

_df = None


def load(month=None):
    global _df
    ls = LoadService()
    _df = ls.execute(month)
    _df["Compound"] = (_df.Twelve_months +
                       _df.Six_months +
                       _df.Three_months +
                       _df.One_month) / 4


def categories():
    return _df.Category.unique()


def trend(nbr_funds=3, categories=None):
    trend = lambda x: x.nlargest(nbr_funds, "Compound")  # noqa: E731

    group = _df.groupby("Category")
    funds_per_category = group.apply(trend)[["Fund", "Compound"]]

    if categories:
        filter = " or ".join(["Category=='{}'".format(c) for c in categories])
        funds_per_category = funds_per_category.query(filter)

    funds_per_category.name = "Trend {}".format(_df.name)

    return funds_per_category


def agg(nbr_picked_funds, categories=None):
    funds = trend(1, categories)
    sorted_funds = funds.sort_values("Compound", ascending=False)
    picked_funds = sorted_funds.head(nbr_picked_funds)
    picked_funds.name = "Aggressive Global Growth {}".format(_df.name)

    return picked_funds
