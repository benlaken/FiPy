import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta


class Asset(object):
    """Asset items are essentially dictionaries, and should be of
    a kind = 'real_estate', 'stocks', 'job', or 'cash'. There can be
    infite assets in a Portfolio, but there should be only one cash
    Asset, which should specify a maximum amount of cash to hold. """
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
        for key, value in sorted(self.__dict__.items()):
            yield key, value


class Portfolio(object):
    """ Operates on lists of assets. Can add assets individually
    with addNewAsset() function, or can initilize object with a
    list of asset objects.

    :param Asset: n number of Asset objects
    :param prd: integer indicating number of months to run
    :returns: A Portfolio instance
    """

    def __init__(self, *assets, prd=60):
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
        self.prd = prd
        self.cash = 0
        self._temporary_capitol = None
        self.networth = 0
        self.fi = False
        self.buy_property_threshold = 80
        self.passive_income = 0

    def buy_property(self, asset):
        """Subtract value of asset from investments"""
        print('placeholder function Portfolio.buy_property()')
        self.sell_shares(amount=asset.value - asset.debt)
        self.add_new_asset(new_asset=asset)

    def sell_shares(self, amount):
        """Need a method to handel liquidating a share portfolio"""
        # gather up all stock assets
        # rmv required value from stocks and place in self._temporary_capitol
        print("placeholder function in Portfolio.sell_shares()")
        self._temporary_capitol = amount
        for asset in self.assets:
            if asset.kind.lower() == 'stocks':
                if asset.value > amount:
                    asset.value -= amount
                    self._temporary_capitol = amount
                else:
                    # if one asset cant meet all requirements look for more
                    amount -= asset.value
                    asset.value = 0

    def check_fi(self):
        """Check if FI has been reached. Point at which monthly incoming
        is greater than monthly outgoings before counting wages from jobs.
        """
        negative = 0
        positive = 0
        for asset in self.assets:
            if asset.monthly_expenses:
                negative += asset.monthly_expenses
            if asset.monthly_repayment:
                negative += asset.monthly_repayment
            if asset.kind != 'job' and asset.monthly_income:
                positive += asset.monthly_income
        self.passive_income = positive
        if positive > negative:
            self.fi = True
        else:
            self.fi = False

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
        print("Passive income: {0:3.2f}".format(self.passive_income))

    def add_new_asset(self, new_asset):
        """Add a new Asset() obect to an existing Portfolio instance.
        This will be useful for modifying established portfolios once this is
        running as a web app.

        :param Asset(): Instance of Asset() object
        :returns: Updates Portfolio object
        """
        self.assets.append(new_asset)

    def monthly_ingres(self):
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

    def monthly_egres(self):
        """Calculate and update the monthly outgoing money by summing
        monthly_expenses from asset items.

        :param self.assets.monthly_expenses: Sums list of asset.monthly_expense
        :returns self.monthly_expenses: float
        """
        tmp_expenses = 0
        for asset in self.assets:
            if asset.monthly_expenses:
                tmp_expenses += asset.monthly_expenses
        self.monthly_expenses = tmp_expenses
        assert tmp_expenses < self.monthly_income, "Error: spending too much"
        self.monthly_income -= tmp_expenses

    def investment_portfolio(self):
        """Start of portflio methods."""
        tmp_net = 0
        for asset in self.assets:
            if asset.kind.lower() == 'stocks':
                tmp_net += asset.value
                asset.value *= 1.00333
                if self.monthly_income > 0:
                    asset.value += self.monthly_income
                    self.monthly_income = 0
        self.net_investments = tmp_net

    def count_cash(self):
        """Examines assets for 'cash' type asset and does various actions.
        nb. this function only expects to find one cash asset

        :param self.asset.value: float
        :results self.cash: float
        """
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
        """Examines a flag (asset.pay_debt_asap) from asset objects with debt.
        If an asset has the flag set to True, it will take as much as possible
        from the montly avaiable money (after expenses account for), and spend
        it on minimizing the debt. The minimum repayments should be covered
        for all assets before additional payments are considered.

        :param self.asset:
        :returns self.asset.debt: float
        """
        error1 = "Error: cant meet monthly repayment :("
        for asset in self.assets:
            if asset.debt and asset.monthly_repayment:
                assert self.monthly_income > asset.monthly_repayment, error1
                # Pay all minimum debts for the month
                if (asset.debt - asset.monthly_repayment) <= 0.0:
                    # if this is the last payment, remove the debt
                    self.monthly_income -= asset.debt
                    asset.debt = None
                    asset.monthly_repayment = None
                else:
                    # otherwise, just take the minimum and dont worry
                    asset.debt -= asset.monthly_repayment
                    self.monthly_income -= asset.monthly_repayment
        for asset in self.assets:
            if asset.debt and asset.pay_debt_asap and self.monthly_income > 0:
                asset.debt -= self.monthly_income
                self.monthly_income = 0.0

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
            if asset.value:
                net_value += asset.value
        self.networth = net_value - self.debt

    def update_monthly(self):
        self.date = self.date + relativedelta(months=1)
        if self.net_investments > self.buy_property_threshold:
            print('triggered buy property')
            # temp hack - keep buying same kind of place
            self.buy_property(asset=Asset(**{'kind': 'real estate',
                                             'debt': 70,
                                             'value': 150,
                                             'monthly_repayment': 0.5,
                                             'monthly_income': 0.8,
                                             'start_date': self.date,
                                             'pay_debt_asap': True}))
        self.monthly_ingres()
        self.monthly_egres()
        self.monthly_repay()
        self.monthly_debt()
        self.count_cash()
        self.investment_portfolio()
        self.calc_net_worth()
        self.check_fi()

    def quad_positions(self, left, right, bottom, top, color):
        """Assign values to the left, right, bottom, and top position
        labels and a color value for the Bokeh Quad glyph. Uses two
        diffrent colors depending on if FI has been reached.

        :param self, left, right, bottom, top, color:
        :returns: Assigns values to the list items.
        """
        # Add debt marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        top.append(0.0)
        bottom.append(self.debt * -1)
        if self.fi:
            color.append('#e65c00')
        else:
            color.append('#ff944d')
        # Add cash marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(0.0)
        top.append(self.cash)
        if self.fi:
            color.append('#008000')
        else:
            color.append('#00e600')
        # Add stock marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(self.cash)
        top.append(self.cash + self.net_investments)
        if self.fi:
            color.append('#800080')
        else:
            color.append('#e600e6')
        # Add net worth marker (including  primary property)
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(self.cash + self.net_investments)
        top.append(self.networth)
        if self.fi:
            color.append('#75a3a3')
        else:
            color.append('#b3cccc')
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
