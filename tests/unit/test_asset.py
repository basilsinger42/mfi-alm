import numpy as np

from mfi_alm.assets.asset import Asset, FixedBond


def test_market_value_normal_case():
    """Test market value calculation with typical YTM."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=5.0, freq=2)
    asset = Asset(fixed_bond=bond, ytm=0.04)
    assert np.isclose(asset.market_value(), 1_043.05899897892)


def test_market_value_at_par():
    """Test market value when YTM equals coupon rate."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=5.0, freq=2)
    asset = Asset(fixed_bond=bond, ytm=0.05)
    assert np.isclose(asset.market_value(), 997.246530460935)


def test_copy_asset():
    original_bond = FixedBond(face=1000, coupon=0.05, maturity=10, freq=2)
    original_ytm = 0.05
    original_asset = Asset(original_bond, original_ytm)
    copied_asset = original_asset.copy()

    assert original_asset.ytm == copied_asset.ytm
    assert original_asset.market_value() == copied_asset.market_value()
