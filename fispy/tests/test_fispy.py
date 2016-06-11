import unittest
import datetime as dt
from fispy.fispy import Asset, Portfolio


class TestFispyMethods(unittest.TestCase):
    """Main class for fispy testing methods"""

    def test_count_cash(self):
        a1 = Asset(**{'kind': 'cash',
                      'max_cash': 50.,
                      'value': 15})
        p1 = Portfolio(a1)
        p1.count_cash()
        self.assertEqual(p1.cash, 15)

    def test_portfolio_monthly_income(self):
        d1 = {'kind': 'job',
              'monthly_income': 1.5,
              'start_date': dt.date(2016, 6, 1)}
        d2 = {'kind': 'job',
              'monthly_income': 1.5,
              'start_date': dt.date(2016, 6, 1)}
        test2 = Portfolio(Asset(**d1), Asset(**d2))
        test2.monthly_ingres()
        self.assertEqual(test2.monthly_income, 3.0)

    def test_pay_expenses(self):
        d1 = {'kind': 'job',
              'monthly_income': 1.5,
              'start_date': dt.date(2016, 6, 1),
              'monthly_expenses': 0.5}
        test2 = Portfolio(Asset(**d1))
        test2.monthly_ingres()
        test2.monthly_egres()
        self.assertEqual(test2.monthly_income,
                         d1['monthly_income']-d1['monthly_expenses'])

    def test_add_assets(self):
        """ Check you can add assets to a created Portfolio """
        a1 = Asset(**{'kind': 'job',
                      'monthly_income': 1.5,
                      'monthly_expenses': 0.7})
        p1 = Portfolio(a1)
        p1.add_new_asset(a1)
        self.assertEqual(len(p1.assets), 2)

    def test_net_worth(self):
        """Check the net worth works"""
        a1 = Asset(**{'kind': 'cash',
                      'max_value': 50.,
                      'value': 15})
        a2 = Asset(**{'kind': 'real estate',
                      'value': 150})
        p1 = Portfolio(a1, a2)
        p1.calc_net_worth()
        self.assertEqual(p1.networth, 165)

if __name__ == '__main___':
    unittest.main()
