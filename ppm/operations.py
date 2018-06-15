
from .load.LoadService import LoadService

_df = None

def init():
    global _df
    ls = LoadService()
    _df = ls.execute()
    _df["Compound"] = (_df.Twelve_months + _df.Six_months + _df.Three_months + _df.One_month) / 4

def categories():
    return _df.Category.unique()

def trend(nbr_funds = 3, categories = None):
    group = _df.groupby("Category")
    trend = lambda x: x.nlargest(nbr_funds, "Compound")
    funds_per_category = group.apply(trend)[["Name", "Compound"]]
    
    if categories:
        filter = " or ".join(["Category=='{}'".format(c) for c in categories])
        funds_per_category = funds_per_category.query(filter)

    return funds_per_category

def agg(nbr_picked_funds, categories = None):
    funds = trend(1, categories)
    sorted_funds = funds.sort_values("Compound", ascending=False)
    return sorted_funds.head(nbr_picked_funds)

