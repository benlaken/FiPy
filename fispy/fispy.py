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
        self.date = dt.datetime(year=2016,month=5,day=1)
        self.salaries = d['pay']
        self.income = sum(d['pay'])
        self.cash = d['cash']
        self.max_cash = d['max_cash']
        self.debt = d['debt']
        self.repay = d['repay']
        self.stocks = d['stocks']
        self.stock_growth_rate = d['stock_growth']
        self.expenses = d['expenses']
        self.property_deposit = d['property_deposit'] # how much money before buy another flat?
        self.rent_out_flat = d['rent_first_flat']
        self.second_flat_cost = d['second_flat_cost']
        self.second_flat_monthly=d['second_flat_monthly_payment']
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
        #(For now negative sepending is not allowed...)
        assert self.income == 0.0, "Error: Salary @ end month = {0:5.2f}€".format(self.income)
        self.income = sum(self.salaries)  # <-- set up for next month
        self.stocks_grow()
        if self.stocks > self.property_deposit and self.current_flats < self.max_flats:
#           print("Buying a new flat!")
            self.buy_second_flat(rent_first = self.rent_out_flat,
                        flat_value=self.second_flat_cost,
                        repayment = self.second_flat_monthly)

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


if __name__ == '__main__':
# eg use..
    d = dict(
            pay=[1.5, 1.5],
            cash=19,
            debt=70.,
            repay=0.5,
            expenses=0.7,
            stocks=12,
            max_cash=30,
            stock_growth=0.04,
            property_deposit=100,
            second_flat_cost=200,
            second_flat_monthly_payment=0.8,
            rent_first_flat=0.8,
            max_flats=1,
            pay_debt_faster=True,
            prd=50,
            )
    print("Running as main")
    test = C1(d=d)
