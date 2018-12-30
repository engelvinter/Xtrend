
class Evaluate:
    def __init__(self, fund_view):
        self._view = fund_view
    
    def best(self, nbr_funds=5):
        """
        This function chooces the top funds in three months perspective.

        Parameters
        ----------
        `nbr_funds` : number of funds chosen
        """
        df_funds = self._view.snapshot()
        sorted_funds = df_funds.sort_values("Three_months", ascending=False)["Three_months"]
        return sorted_funds[0:nbr_funds]

    def trend(self, column_name, nbr_funds=3):
        """
        This functions chooses the funds with the highest compound value
        for each group. The compund value is calculated by an average
        of four other averages (12, 6, 3 ,1 month(s)).

        Returns
        -------
        A panda dataframe containing the best fund of each group
        """
        df_funds = self._view.snapshot()

        trend = lambda x: x.nlargest(nbr_funds, "Compound")  # noqa: E731

        group = df_funds.groupby(column_name)
        
        funds = group.apply(trend)[["Compound"]]

        funds.name = "Best groups {}".format(df_funds.name)

        return funds

    def agg(self, nbr_funds):
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
        df_funds = self._view.snapshot()
        sorted_funds = df_funds.sort_values("Compound", ascending=False)["Compound"]
        picked_funds = sorted_funds.head(nbr_funds)
        picked_funds.name = "Aggressive Global Growth {}".format(df_funds.name)
        return picked_funds
    