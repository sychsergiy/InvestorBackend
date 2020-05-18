import unittest
import typing as t

from apps.purchase.models import Purchase
from apps.purchase import profit


class PurchaseMock(t.NamedTuple):
    absolute_amount: float
    asset_amount: float
    type: Purchase.Types


class CalculateProfitTestCase(unittest.TestCase):
    def test_zero_invested_error(self):
        purchases = [
            PurchaseMock(200, 1, Purchase.Types.SELL),
        ]
        with self.assertRaises(profit.ZeroInvestedAmountError):
            profit.calculate_profit(purchases)

    def test_zero_asset_returned_error(self):
        purchases = [
            PurchaseMock(100, 1, Purchase.Types.BUY),
        ]
        with self.assertRaises(profit.ZeroAssetReturnedAmountError):
            profit.calculate_profit(purchases)

    def test_invested_asset_amount_less_than_returned_error(self):
        purchases = [
            PurchaseMock(100, 1, Purchase.Types.BUY),
            PurchaseMock(25, 1, Purchase.Types.SELL),
            PurchaseMock(25, 1, Purchase.Types.SELL),
        ]
        with self.assertRaises(profit.InvestedAssetAmountLessThanReturnedError):
            profit.calculate_profit(purchases)

    def test_ok(self):
        payments = [
            PurchaseMock(100, 1, Purchase.Types.BUY),
            PurchaseMock(100, 1, Purchase.Types.BUY),
            PurchaseMock(200, 1, Purchase.Types.SELL),
        ]
        result = profit.calculate_profit(payments)
        self.assertEqual(result, 2)

    def test_ok_2(self):
        purchases = [
            PurchaseMock(100, 1, Purchase.Types.BUY),
            PurchaseMock(25, 0.5, Purchase.Types.SELL),
            PurchaseMock(25, 0.5, Purchase.Types.SELL),
        ]
        result = profit.calculate_profit(purchases)
        self.assertEqual(result, 0.5)
