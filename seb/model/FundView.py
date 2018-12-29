from .MakeStats import MakeStats

from common.assign_date import assign_date

from datetime import datetime

from re import match

from .FilterName import FilterName
from .FilterAboveMA import FilterAboveMA
from .AddColumn import AddColumn


class FundView:
    def __init__(self, fund_result):
        self._funds = fund_result.funds
        self._date = fund_result.last_updated
        self._transform_list = []

    def filter_name(self, regexp):
        f = FilterName(regexp)
        self._transform_list.append(f)
    
    def filter_above_ma(self, nbr_days):
        f = FilterAboveMA(self._funds, self._date, nbr_days)
        self._transform_list.append(f)
        
    def snapshot(self):
        ms = MakeStats(self._date, 10)
        df = ms.execute(self._funds)

        for filter in self._transform_list:
            df = filter.execute(df)

        return df

    def set_date(self, date):
        """
        Sets a new date. This new date will be used as
        the last date in trend calculations.

        Parameters
        ----------
        `date` : the actual date
        """
        self._date = assign_date(date)

    def set_groups(self, fund_to_group):
        """
        Connects funds with different groups

        Parameters
        ----------
        `fund_to_group` : dictionary populated by fund name => group name 
        """
        f = AddColumn("Group", fund_to_group)
        self._transform_list.append(f)

    def reset(self):
        self._filter_list = []

    def available_funds(self, year, regexp=".*"):
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
        for fund, data in self.funds.items():
            if match(regexp, fund) is None:
                continue
            start_fund = data.index[0]
            end_fund = data.index[-1]
            if start_fund < start_year and end_fund > end_year:
                avail_funds.append(fund)
        return avail_funds
        

    