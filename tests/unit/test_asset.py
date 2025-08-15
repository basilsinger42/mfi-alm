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


def test_projected_market_values_normal_case():
    """Test projected market values over the next years with typical YTM."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=5.0, freq=2)
    asset = Asset(fixed_bond=bond, ytm=0.04)
    expected_prices = np.array([1043.05899898, 1060.12201075, 1051.8611079, 1043.2630712, 1034.31414196])
    actual_prices = asset.projected_market_values(5)
    assert np.allclose(actual_prices, expected_prices, rtol=1e-5)
