import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta


class C1(object):
    """ Generate financial development for a given scenario.

    Parameters
    ----------
    d: dict
        A dictionary object with keys required by __init__()

    Returns
    -------
    return: gen_quads()
        A pandas.DataFrame object with plotting values for a
        Bokeh Quad plot.
    """
    def __init__(self, d):
        self.date = dt.datetime(year=2016, month=5, day=1)
        self.salaries = d['pay']
        self.income = sum(d['pay'])
        self.cash = d['cash']
        self.max_cash = d['max_cash']
        self.debt = d['debt']
        self.repay = d['repay']
        self.stocks = d['stocks']
        self.stock_growth_rate = d['stock_growth']
        self.expenses = d['expenses']
        self.property_deposit = d['property_deposit']
        # how much money before buy another flat?
        self.rent_out_flat = d['rent_first_flat']
        self.second_flat_cost = d['second_flat_cost']
        self.second_flat_monthly = d['second_flat_monthly_payment']
        self.max_flats = d['max_flats']
        self.current_flats = 1
        self.pay_debt_faster = d['pay_debt_faster']
        self.prd = d['prd']

    def pay_expenses_and_debt(self):
        self.income -= self.expenses
        in_debt = self.debt > 0.00
        can_pay = self.repay < self.income
        if in_debt and can_pay:
            self.income -= self.repay
            self.debt -= self.repay

    def stocks_grow(self):
        self.stocks += self.stock_growth_rate

    def debt_save_or_shares(self):
        """ Build up cash, pay extra debt, or invest """
        salary_left = self.income > 0.0
        in_debt = self.debt > 0.00
        if salary_left:
            #print("Saving")
            if(self.cash < self.max_cash):
                self.cash += self.income
                self.income -= self.income
            elif(in_debt and self.pay_debt_faster):
                #print("Paying extra debt")
                tmp_dbt = self.debt
                self.debt -= self.income
                if self.debt < 0.0:
                    self.debt = 0.0
                    self.income = self.income - tmp_dbt
                self.income -= self.income
            elif(self.income != 0.0):
                #print("Investing")
                self.stocks += self.income
                self.income -= self.income

    def buy_second_flat(self, rent_first=None, flat_value=None, repayment=None):
        assert rent_first != None, "Error: No rent specified"
        assert flat_value != None, "Error: No flat value specified"
        assert repayment != None, "Error: No repayment specified"
        existing_debt = self.debt > 0.00
        self.debt = self.debt + (flat_value - self.stocks)
        self.stocks = 0.0
        self.salaries.append(rent_first)
        # Bug - need to change repayment to be a list of debts and
        # track those individually
        self.repay = repayment
        self.current_flats += 1

    def update_monthly(self):
        self.date = self.date + relativedelta(months=1)
        self.pay_expenses_and_debt()
        self.debt_save_or_shares()
        # Need to make a case of going into debt.
        # (For now negative sepending is not allowed...)
        assert self.income == 0.0, "Error: Salary @ end month = {0:5.2f}€".format(self.income)
        self.income = sum(self.salaries)  # <-- set up for next month
        self.stocks_grow()
        if self.stocks > self.property_deposit and self.current_flats < self.max_flats:
            self.buy_second_flat(rent_first=self.rent_out_flat,
                        flat_value=self.second_flat_cost,
                        repayment=self.second_flat_monthly)

    def give_values(self):
        return self.date, self.cash, self.debt, self.stocks


    def quad_positions(self, left, right, bottom, top, color):
        # Add debt marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        top.append(0.0)
        bottom.append(self.debt * -1)
        color.append('#ff9d68')
        # Add cash marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(0.0)
        top.append(self.cash)
        color.append('#95ff68')
        # Add stock marker
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(self.cash)
        top.append(self.cash + self.stocks)
        color.append('#d268ff')
        return

    def gen_quads(self):
        left = []
        right = []
        top=[]
        bottom=[]
        color=[]
        for i in range(self.prd):
            self.update_monthly()
            self.quad_positions(left=left, top=top, bottom=bottom,
                                right=right, color=color)
        return pd.DataFrame({'left': left, 'right': right, 'top': top,
                            'bottom': bottom, 'color': color})



class Asset(object):
    def __init__(self, **kwargs):
        self.kind = kwargs.get('kind', None)
        assert self.kind.lower() in [None, 'real estate', 'stocks', 'job', 'cash']
        self.monthly_income = kwargs.get('monthly_income', None)
        self.monthly_expenses = kwargs.get('monthly_expenses', None)
        self.start_date = kwargs.get('start_date', dt.datetime.now().date())
        self.end_date = kwargs.get('end_date', None)
        self.debt = kwargs.get('debt', None)
        self.value = kwargs.get('value', None)
        self.max_cash = kwargs.get('max_cash', None)
        self.monthly_repayment = kwargs.get('monthly_repayment', None)
        self.pay_debt_asap = kwargs.get('pay_debt_asap', None)

    def __str__(self):
        return str("Asset = {0}".format(self.kind))

    def __iter__(self):
        for key, value in sorted(a1.__dict__.items()):
            yield key, value



class Portfolio(object):
    """ Operates on lists of assets. Can add assets individually
    with addNewAsset() function, or can initilize object with a
    list of asset objects.

    Add a test that at most only one cash asset (a summary asset) is given.
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
        self.netInvestments = 0
        self.debt = 0
        self.prd = 60
        self.cash = 0
        self.networth = 0 # (cash + investments + property value) - debt


    def summary(self):
        print("--Summary--\nIncome: {0:3.2f} \nCash: {1:3.2f} \nDebt: {3:3.2f} \nInvestments: {2:3.2f}".format(
                self.monthly_income, self.cash, self.netInvestments, self.debt))
        print("Net worth: {0:3.2f}".format(self.networth))

    def addNewAsset(self, new_asset):
        self.assets.append(new_asset)

    def monthlyIncome(self):
        tmp_income = 0
        for asset in self.assets:
            if asset.monthly_income:
                tmp_income += asset.monthly_income
        self.monthly_income = tmp_income

    def monthlyExpenses(self):
        tmp_expenses = 0
        for asset in self.assets:
            if asset.monthly_expenses:
                tmp_expenses += asset.monthly_expenses
        self.monthly_expenses = tmp_expenses
        assert tmp_expenses < self.monthly_income, "Error: spending too much money..."
        self.monthly_income -= tmp_expenses

    def investmentPortfolio(self):
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
        self.netInvestments = tmp_net

    def countCash(self):
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

    def monthlyRepay(self):
        for asset in self.assets:
            if asset.debt and asset.monthly_repayment:
                assert self.monthly_income > asset.monthly_repayment, "Error: cant meet monthly repayment :("
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

    def monthlyDebt(self):
        tmp_debt = 0
        for asset in self.assets:
            if asset.debt:
                tmp_debt += asset.debt
        self.debt = tmp_debt


    def calcNetWorth(self):
        net_value = 0
        for asset in self.assets:
            # cash, property and investments all have a value property (not jobs)
            if asset.value:
                net_value += asset.value
        self.networth = net_value - self.debt

    def update_monthly(self):
        self.date = self.date + relativedelta(months=1)
        self.monthlyIncome()   # Gather income at start of month
        self.monthlyExpenses()  # Work out living expenses and subtract it from the income
        self.monthlyRepay()    # Repay monthly morgage expenses from income
        self.monthlyDebt()     # Work out remaining size of accumulated debt
        self.countCash()       # Count the cash and add to pile if required
        self.investmentPortfolio() # Gather investments value, and grow, also buy more if money left
        self.calcNetWorth()

    def quad_positions(self, left, right, bottom, top, color):
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
        top.append(self.cash + self.netInvestments)
        color.append('#BF00FF')
        # Add net worth marker (including  primary property)
        left.append(self.date)
        right.append(self.date + relativedelta(months=1))
        bottom.append(self.cash + self.netInvestments)
        top.append(self.networth)
        color.append('#BDBDBD')
        return

    def gen_quads(self):
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
