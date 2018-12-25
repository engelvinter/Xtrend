import pandas as pd
import seb.operations as op

def backtest1():
    dates = pd.date_range("2000-02-28", "2018-12-15", freq="M")

    for d in dates:
        op.set_date(d.date())
        op.agg(3)