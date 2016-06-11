import unittest
import datetime as dt
from fispy.fispy import Asset, Portfolio

a_cashpile = Asset(**{'kind': 'cash',
                      'max_cash': 50.,
                      'value': 15})

a_job = Asset(**{'kind': 'job',
                 'monthly_income': 1.5,
                 'monthly_expenses': 0.5,
                 'start_date': dt.date(2016, 6, 1)})

a_flat = Asset(**{'kind': 'real estate',
                  'value': 150})

class TestFispyMethods(unittest.TestCase):
    """Main class for fispy testing methods"""

    def test_asset_iterable(self):
        n = 0
        for k, v in a_cashpile:
            if v:
                n += 1
        self.assertEqual(n, 4)

    def test_count_cash(self):
        pfolio = Portfolio(a_cashpile)
        pfolio.count_cash()
        self.assertEqual(pfolio.cash, 15)

    def test_portfolio_monthly_income(self):
        pfolio = Portfolio(a_job, a_job)
        pfolio.monthly_ingres()
        self.assertEqual(pfolio.monthly_income, 3.0)

    def test_pay_expenses(self):
        pfolio = Portfolio(a_job)
        pfolio.monthly_ingres()
        pfolio.monthly_egres()
        self.assertEqual(pfolio.monthly_income, 1.5 - 0.5)

    def test_add_assets(self):
        """ Check you can add assets to a created Portfolio """
        pfolio = Portfolio(a_job)
        pfolio.add_new_asset(a_job)
        self.assertEqual(len(pfolio.assets), 2)

    def test_net_worth(self):
        """Check the net worth works"""
        pfolio = Portfolio(a_cashpile, a_flat)
        pfolio.calc_net_worth()
        self.assertEqual(pfolio.networth, 165)

if __name__ == '__main___':
    unittest.main()
