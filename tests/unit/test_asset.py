import numpy as np

from mfi_alm.assets.asset import Asset, FixedBond, AssetPortfolio


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

    original_bond = FixedBond(face=1000, coupon=0.05, maturity=10, freq=2)  # 填入实际参数
    original_ytm = 0.05
    original_asset = Asset(original_bond, original_ytm)

    copied_asset = original_asset.copy()

    assert original_asset.ytm == copied_asset.ytm
    assert original_asset.market_value() == copied_asset.market_value()


def test_asset():

    bond1 = FixedBond(face=1000, coupon=0.05, maturity=10)
    bond2 = FixedBond(face=500, coupon=0.03, maturity=5)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.03)
    portfolio = AssetPortfolio(assets=[asset1, asset2], ytm=0.035)

    assert len(portfolio.assets) == 2
    assert portfolio.ytm == 0.035

    mv = portfolio.market_value()
    expected = asset1.market_value() + asset2.market_value()
    assert mv == expected


def test_portfolio_copy():
    bond1 = FixedBond(face=1000, coupon=0.05, maturity=10)
    bond2 = FixedBond(face=500, coupon=0.03, maturity=5)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.03)
    portfolio = AssetPortfolio(assets=[asset1, asset2], ytm=0.035)
    copied = portfolio.copy()

    # First asset
    assert len(portfolio.assets) == len(copied.assets)

    assert portfolio.assets[0].ytm == copied.assets[0].ytm
    assert portfolio.assets[0].fixed_bond.face == 1000.0
    assert copied.assets[0].fixed_bond.face, 1000.0
    assert portfolio.assets[0].fixed_bond.coupon, 0.05
    assert portfolio.assets[0].fixed_bond.maturity, 10.0

    # second asset
    assert portfolio.assets[1].ytm == copied.assets[1].ytm
    assert portfolio.assets[1].fixed_bond.face == 500.0
    assert copied.assets[1].fixed_bond.face == 500.0

    # deep test
    copied.assets[0].ytm = 0.1
    assert portfolio.assets[0].ytm != copied.assets[0].ytm

    original_maturity = portfolio.assets[1].fixed_bond.maturity
    copied.assets[1].fixed_bond.maturity = 2
    assert original_maturity != copied.assets[1].fixed_bond.maturity
