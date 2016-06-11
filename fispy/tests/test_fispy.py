import unittest
import datetime as dt
from fispy.fispy import C1, Asset, Portfolio

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


class TestFispyMethods(unittest.TestCase):

    def test_C1objectCreated(self):
        projection = C1(d=d)
        self.assertIsNotNone(projection)

    def test_PortfolioMonthlyIncome(self):
        d1 = {'kind': 'job',
              'monthly_income': 1.5,
              'start_date': dt.date(2016, 6, 1)}
        d2 = {'kind': 'job',
              'monthly_income': 1.5,
              'start_date': dt.date(2016, 6, 1)}
        test2 = Portfolio(Asset(**d1), Asset(**d2))
        test2.monthly_income()
        self.assertEqual(test2.monthly_income, 3.0)

    def test_PayExpenses(self):
        d1 = {'kind': 'job',
              'monthly_income': 1.5,
              'start_date': dt.date(2016, 6, 1),
              'monthly_expenses': 0.5}
        test2 = Portfolio(Asset(**d1))
        test2.monthly_income()
        test2.monthly_expenses()
        self.assertEqual(test2.monthly_income,
                         d1['monthly_income']-d1['monthly_expenses'])

    def test_AddAssets(self):
        """ Check you can add assets to a created Portfolio """
        a1 = Asset(**{'kind': 'job',
                      'monthly_income': 1.5,
                      'monthly_expenses': 0.7})
        p1 = Portfolio(a1)
        p1.add_new_asset(a1)
        self.assertEqual(len(p1.assets), 2)

if __name__ == '__main___':
    unittest.main()
