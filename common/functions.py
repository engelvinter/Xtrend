
def above_ma(nbr_days, ts):
    ma = ts[-nbr_days:].mean()
    return ts[-1] > ma
    