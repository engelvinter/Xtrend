from empyrical import cum_returns

import matplotlib.pyplot as plt

import seaborn as sns
sns.set()


class Graph:    
    def __init__(self, name, ts):
        self._name = name
        self._ts = ts
        self._ax = None

    def show(self):
        if not self._ax:
            cum_ret, ma50, ma200 = self._make_stats()
            self._ax = self._draw(cum_ret, ma50, ma200)
        plt.show()

    def save(self, full_path):
        if not self._ax:
            cum_ret, ma50, ma200 = self._make_stats()
            self._ax = self._draw(cum_ret, ma50, ma200)
        fig = self._ax.get_figure()
        fig.savefig()

    def _make_stats(self):
        pct = self._ts.pct_change()
        cum_ret = cum_returns(pct) * 100
        ma200 = cum_ret.rolling(200).mean()
        ma50 = cum_ret.rolling(50).mean()
        return (cum_ret, ma50, ma200)

    def _draw(self, cum_ret, ma50, ma200):
        ax = sns.lineplot(data=cum_ret, label=self._name)
        sns.lineplot(data=ma50, label="MA50")
        sns.lineplot(data=ma200, label="MA200")
        ax.set(xlabel='time', ylabel='percent')
        return ax