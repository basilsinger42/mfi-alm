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
