import typing as t

from apps.purchase.models import Purchase


class Sums(t.NamedTuple):
    invested: float
    returned: float
    asset_invested: float
    asset_returned: float


def _calc_sums(purchases: t.List[Purchase]) -> Sums:
    buys = [item for item in purchases if item.type == Purchase.Types.BUY]
    invested = sum([item.absolute_amount for item in buys])
    asset_invested = sum([item.asset_amount for item in buys])

    sells = [item for item in purchases if item.type == Purchase.Types.SELL]
    returned = sum([item.absolute_amount for item in sells])
    asset_returned = sum([item.asset_amount for item in sells])

    return Sums(invested, returned, asset_invested, asset_returned)


class ZeroAssetReturnedAmountError(Exception):
    def __str__(self):
        return "Zero returned amount"


class ZeroInvestedAmountError(Exception):
    def __str__(self):
        return "Zero invested amount"


class InvestedAssetAmountLessThanReturnedError(Exception):
    def __str__(self):
        return "Invested asset amount less than returned"


def calculate_profit(purchases: t.List[Purchase]) -> float:
    sums = _calc_sums(purchases)

    if sums.invested == 0:
        raise ZeroInvestedAmountError()

    if sums.asset_returned == 0:
        raise ZeroAssetReturnedAmountError()

    if sums.asset_returned > sums.asset_invested:
        raise InvestedAssetAmountLessThanReturnedError()

    assert_rest_part = (sums.asset_invested - sums.asset_returned) / sums.asset_invested
    asset_spend_part = 1 - assert_rest_part

    sold_part = sums.returned / sums.invested

    return sold_part / asset_spend_part
