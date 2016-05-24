import unittest
from fispy.fispy import C1

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

    def test_objectCreated(self):
        projection = C1(d=d)
        self.assertIsNotNone(projection)

if __name__ == '__main___':
    unittest.main()
