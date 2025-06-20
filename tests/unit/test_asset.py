from mfi_alm.assets.asset import Asset, FixedBond


"""
def test_asset() -> None:
    asset = Asset(market_price=100.0, growth_rate=0.05)
    assert True
"""

import pytest

def test_market_value_normal_case():
    """Test market value calculation with typical YTM."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=5.0, freq=2)
    asset = Asset(fixed_bond=bond, ytm=0.04)
    mv = asset.market_value()

    expected_price = sum(
        cf * FixedBond._disc(0.04, t)
        for t, cf in bond.cashflows()
    )
    assert mv == pytest.approx(expected_price, rel=1e-6)


def test_market_value_at_par():
    """Test market value when YTM equals coupon rate."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=5.0, freq=2)
    asset = Asset(fixed_bond=bond, ytm=0.05)
    assert asset.market_value() == pytest.approx(1000.0, rel=1e-2)

