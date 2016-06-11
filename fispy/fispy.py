import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta


class Asset(object):
    def __init__(self, **kwargs):
        self.kind = kwargs.get('kind')
        assert self.kind.lower() in [None, 'real estate', 'stocks',
                                     'job', 'cash']
        self.monthly_income = kwargs.get('monthly_income')
        self.monthly_expenses = kwargs.get('monthly_expenses')
        self.start_date = kwargs.get('start_date', dt.datetime.now().date())
        self.end_date = kwargs.get('end_date')
        self.debt = kwargs.get('debt')
        self.value = kwargs.get('value')
        self.max_cash = kwargs.get('max_cash')
        self.monthly_repayment = kwargs.get('monthly_repayment')
        self.pay_debt_asap = kwargs.get('pay_debt_asap')

    def __str__(self):
        return str("Asset = {0}".format(self.kind))

    def __iter__(self):
        for key, value in sorted(a1.__dict__.items()):
            yield key, value

class Portfolio(object):
    """ Operates on lists of assets. Can add assets individually
    with addNewAsset() function, or can initilize object with a
    list of asset objects.

    :param Asset: n number of Asset objects
    :returns: A Portfolio instance
    """

    def __init__(self, *assets):
        self.assets = []
        print("{0} items passed".format(len(assets)))
        if assets:
            for asset in assets:
                self.assets.append(asset)
            self.date = min([asset.start_date for asset in self.assets])
        self.monthly_income = 0
        self.monthly_expenses = 0
        self.net_investments = 0
        self.debt = 0
        self.prd = 60
        self.cash = 0
        self.networth = 0 # (cash + investments + property value) - debt


    def summary(self):
        """Print a summary of the Portfolio instance values of Income, Cash
        Debt, Investments and Net worth.

        :param self:
        :returns: A series of string items
        """
        print("--Summary--\nIncome: {0:3.2f} \nCash: {1:3.2f}".format(
                self.monthly_income, self.cash))
        print("Debt: {0:3.2f}".format(self.debt))
        print("Investments: {0:3.2f}".format(self.net_investments))
        print("Net worth: {0:3.2f}".format(self.networth))

    def add_new_asset(self, new_asset):
        """Add a new Asset() obect to an existing Portfolio instance.
        This will be useful for modifying established portfolios once this is
        running as a web app.

        :param Asset(): Instance of Asset() object
        :returns: Updates Portfolio object
        """
        self.assets.append(new_asset)

    def monthly_income(self):
        """Calculate avaiable monthly cash based on monthly_income from all
        Asset() objects of a portfolio.

        :param self.assets: Sums asset.monthly_income across asset objects
        :returns self.monthly_income: float
        """
        tmp_income = 0
        for asset in self.assets:
            if asset.monthly_income:
                tmp_income += asset.monthly_income
        self.monthly_income = tmp_income

    def monthly_expenses(self):
        tmp_expenses = 0
        for asset in self.assets:
            if asset.monthly_expenses:
                tmp_expenses += asset.monthly_expenses
        self.monthly_expenses = tmp_expenses
        assert tmp_expenses < self.monthly_income, "Error: spending too much"
        self.monthly_income -= tmp_expenses

    def investment_portfolio(self):
        tmp_net = 0
        for asset in self.assets:
            if asset.kind.lower() == 'stocks':
                # Work out value of assets
                tmp_net += asset.value
                # Increment assets (this should be replaced with historical monthly flux)
                asset.value *= 1.00333  # placeholder way of incrementing value of an asset
                # Buy more assets (at the moment this is naieve,
                # and will spend all money on first stock it encounters in asset list)
                if self.monthly_income > 0:  # If money left at end of month, invest it
                    asset.value += self.monthly_income
                    self.monthly_income = 0
        self.net_investments = tmp_net

    def count_cash(self):
        """nb. this function only expects to find one cash asset"""
        max_cash = 0
        for asset in self.assets:
            if asset.kind.lower() == 'cash':
                self.cash = asset.value
                max_cash = asset.max_cash
                if self.cash < max_cash and self.monthly_income > 0:
                    asset.value += self.monthly_income
                    self.monthly_income = 0.0
                    self.cash = asset.value

    def monthly_repay(self):
        error1 = "Error: cant meet monthly repayment :("
        for asset in self.assets:
            if asset.debt and asset.monthly_repayment:
                assert self.monthly_income > asset.monthly_repayment, error1
                if (asset.debt - asset.monthly_repayment) <= 0.0:
                    #if this is the last payment...
                    self.monthly_income -= asset.debt
                    asset.debt = None
                    asset.monthly_repayment = None
                    return
                else:
                    if asset.pay_debt_asap:
                        asset.debt -= self.monthly_income
                        self.monthly_income = 0.0
                    else:
                        asset.debt -= asset.monthly_repayment
                        self.monthly_income -= asset.monthly_repayment

    def monthly_debt(self):
        """Calculate debt each month. Examines the Assets held in the Portfolio
        object, and sums the debt. Assigns this value to self.debt.

        :param self: Examines Portfolio objects assets.debt floats
        :returns self.debt: float
        """
        tmp_debt = 0
        for asset in self.assets:
            if asset.debt:
                tmp_debt += asset.debt
        self.debt = tmp_debt

    def calc_net_worth(self):
        """Calculates Net worth by summing value of assets and subtracting debt.

        :param self: Examines attributes of Portfolio object
        :returns: self.networth in Portfolio object
        """
        net_value = 0
        for asset in self.assets:
            # cash, property and investments all have a value property (not jobs)
            if asset.value:
                net_value += asset.value
        self.networth = net_value - self.debt

    def update_monthly(self):
        self.date = self.date + relativedelta(months=1)
        self.monthly_income()   # Gather income at start of month
        self.monthly_expenses()  # Work out living expenses and subtract it from the income
        self.monthly_repay()    # Repay monthly morgage expenses from income
        self.monthly_debt()     # Work out remaining size of accumulated debt
        self.count_cash()       # Count the cash and add to pile if required
        self.investment_portfolio() # Gather investments value, and grow, also buy more if money left
        self.calc_net_worth()

    def quad_positions(self, left, right, bottom, top, color):
        """Assign values to the left, right, bottom, and top position
        labels and a color value for the Bokeh Quad glyph.

        :param self, left, right, bottom, top, color:
        :returns: Assigns values to the list items.
        """
        # Add debt marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        top.append(0.0)
        bottom.append(self.debt * -1)
        color.append('#FE642E')
        # Add cash marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(0.0)
        top.append(self.cash)
        color.append('green')
        # Add stock marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(self.cash)
        top.append(self.cash + self.net_investments)
        color.append('#BF00FF')
        # Add net worth marker (including  primary property)
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(self.cash + self.net_investments)
        top.append(self.networth)
        color.append('#BDBDBD')
        return

    def gen_quads(self):
        """For the current state of Portfolio properties generate quad plot
        dataframe object to be consumed by Bokeh plots.

        :param self: Examines attributes of Portfolio object
        :returns: a pd.DataFrame object
        """
        left = []
        right = []
        top = []
        bottom = []
        color = []
        for i in range(self.prd):
            self.update_monthly()
            self.quad_positions(left=left, top=top, bottom=bottom,
                                right=right, color=color)
        return pd.DataFrame({'left': left, 'right': right, 'top': top,
                            'bottom': bottom, 'color': color})
