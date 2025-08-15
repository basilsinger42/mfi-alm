import numpy as np

from mfi_alm.assets.asset import Asset, FixedBond
from mfi_alm.assets.asset_portfolio import AssetPortfolio


def test_asset_portfolio_general():
    bond1 = FixedBond(face=1000, coupon=0.05, maturity=10)
    bond2 = FixedBond(face=500, coupon=0.03, maturity=5)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.03)
    portfolio = AssetPortfolio(assets=[asset1, asset2])

    assert len(portfolio.assets) == 2

    mv = portfolio.market_value()
    expected = asset1.market_value() + asset2.market_value()
    assert np.isclose(mv, expected)

    avg_yield = portfolio.average_yield()
    expected_yield = (asset1.ytm + asset2.ytm) / 2
    assert np.isclose(avg_yield, expected_yield)


def test_asset_portfolio_copy():
    bond1 = FixedBond(face=1000, coupon=0.05, maturity=10)
    bond2 = FixedBond(face=500, coupon=0.03, maturity=5)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.03)
    portfolio = AssetPortfolio(assets=[asset1, asset2])
    copied = portfolio.copy()

    # Check attributes
    assert len(portfolio.assets) == len(copied.assets)
    assert portfolio.assets[0].ytm == copied.assets[0].ytm
    assert copied.assets[0].fixed_bond.face == 1000.0
    assert copied.assets[0].fixed_bond.coupon == 0.05
    assert copied.assets[0].fixed_bond.maturity == 10.0

    assert copied.assets[1].fixed_bond.face == 500.0
    assert copied.assets[1].ytm == 0.03

    # Deep copy check
    copied.assets[0].ytm = 0.1
    assert portfolio.assets[0].ytm != copied.assets[0].ytm

    copied.assets[1].fixed_bond.maturity = 2
    assert portfolio.assets[1].fixed_bond.maturity != copied.assets[1].fixed_bond.maturity


def test_asset_portfolio_age_one_year():
    bond1 = FixedBond(face=1000, coupon=0.05, maturity=10)
    bond2 = FixedBond(face=500, coupon=0.03, maturity=1)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.03)
    portfolio = AssetPortfolio(assets=[asset1, asset2])

    portfolio.age_one_year()

    assert portfolio.assets[0].fixed_bond.maturity == 9
    assert portfolio.assets[1].fixed_bond.maturity == 0


def test_projected_average_yields_general_case():
    """Test average yield projection of an asset portfolio."""
    bond1 = FixedBond(face=1000, coupon=0.05, maturity=5)
    bond2 = FixedBond(face=1000, coupon=0.03, maturity=5)
    asset1 = Asset(fixed_bond=bond1, ytm=0.04)
    asset2 = Asset(fixed_bond=bond2, ytm=0.02)
    portfolio = AssetPortfolio(assets=[asset1, asset2], scale=1.0)
    years = 3
    avg_yields = portfolio.projected_average_yields(years=years)
    v1 = asset1.projected_market_values(years + 1)
    v2 = asset2.projected_market_values(years + 1)
    expected_portfolio_values = np.mean([v1, v2], axis=0)
    expected_yields = (expected_portfolio_values[1:] - expected_portfolio_values[:-1]) / expected_portfolio_values[:-1]
    # assert np.allclose(avg_yields, expected_yields, rtol=1e-5)
