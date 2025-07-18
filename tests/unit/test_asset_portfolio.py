from mfi_alm.assets.asset import Asset, FixedBond
from mfi_alm.assets.asset_portfolio import AssetPortfolio


def test_asse_portfolio_general():
    bond1 = FixedBond(face=1000, coupon=0.05, maturity=10)
    bond2 = FixedBond(face=500, coupon=0.03, maturity=5)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.03)
    portfolio = AssetPortfolio(assets=[asset1, asset2])
    assert len(portfolio.assets) == 2
    mv = portfolio.market_value()
    expected = asset1.market_value() + asset2.market_value()
    assert mv == expected


def test_asset_portfolio_copy():
    bond1 = FixedBond(face=1000, coupon=0.05, maturity=10)
    bond2 = FixedBond(face=500, coupon=0.03, maturity=5)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.03)
    portfolio = AssetPortfolio(assets=[asset1, asset2])
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
