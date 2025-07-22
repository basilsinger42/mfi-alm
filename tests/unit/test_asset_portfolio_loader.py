import csv
import os
import tempfile
import json

import pytest

from mfi_alm.assets.asset_portfolio_loader import AssetPortfolioLoader


@pytest.fixture
def valid_csv_file():
    # set up
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "valid_assets.csv")

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["face", "coupon", "maturity", "ytm", "freq"])
        writer.writeheader()
        writer.writerow({"face": "1000", "coupon": "0.05", "maturity": "5.0", "ytm": "0.04", "freq": "2"})
        writer.writerow({"face": "2000", "coupon": "0.06", "maturity": "3.0", "ytm": "0.05", "freq": "2"})

    yield file_path

    # tear-down.
    os.remove(file_path)
    os.rmdir(temp_dir)


def test_load_valid_csv(valid_csv_file):
    portfolio = AssetPortfolioLoader.load_asset_portfolio(file_path=valid_csv_file, ytm_factor=1.0)
    assert len(portfolio.assets) == 2
    asset1 = portfolio.assets[0]
    assert asset1.fixed_bond.face == 1000
    assert asset1.fixed_bond.coupon == 0.05
    assert asset1.ytm == 0.04
    asset2 = portfolio.assets[1]
    assert asset2.fixed_bond.face == 2000
    assert asset2.fixed_bond.coupon == 0.06
    assert asset2.ytm == 0.05


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        AssetPortfolioLoader.load_asset_portfolio(file_path="nonexistent.csv", ytm_factor=1.0)


# scenario test
def test_ytm_adjustment(valid_csv_file):
    portfolio = AssetPortfolioLoader.load_asset_portfolio(file_path=valid_csv_file, ytm_factor=0.5)
    assert portfolio.assets[0].ytm == 0.02
    assert portfolio.assets[1].ytm == 0.025


def test_load_from_config():
    temp_dir = tempfile.mkdtemp()
    config_path = os.path.join(temp_dir, "test_config.json")
    test_data = {
        "asset_path": "data/asset_tape.csv",
        "scenarios": [{"name": "base", "ytm_factor": 1.0}, {"name": "high_yield", "ytm_factor": 1.5}],
    }
    with open(config_path, "w") as f:
        json.dump(test_data, f)

    portfolios = AssetPortfolioLoader.load_from_config(config_path)
    assert isinstance(portfolios, dict)
    assert len(portfolios) == 2
    assert "base" in portfolios
    assert "high_yield" in portfolios
    assert portfolios["base"].market_value() == 116599.54913845785
    assert portfolios["high_yield"].market_value() == 85050.15521766715

    os.remove(config_path)
    os.rmdir(temp_dir)
