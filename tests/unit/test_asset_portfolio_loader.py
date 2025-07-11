import csv
import os
import tempfile

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


@pytest.fixture
def invalid_csv_file():
    # setup.
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "invalid_assets.csv")

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["face", "coupon", "maturity", "ytm"])
        writer.writeheader()
        writer.writerow({"face": "invalid", "coupon": "0.05", "maturity": "5.0", "ytm": "0.04"})

    yield file_path

    # tear-down.
    os.remove(file_path)
    os.rmdir(temp_dir)


def test_load_valid_csv(valid_csv_file):
    portfolio = AssetPortfolioLoader.load_from_csv(valid_csv_file)

    assert len(portfolio.assets) == 2
    assert portfolio.ytm == 0.045

    asset1 = portfolio.assets[0]
    assert asset1.fixed_bond.face == 1000
    assert asset1.fixed_bond.coupon == 0.05
    assert asset1.ytm == 0.04


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        AssetPortfolioLoader.load_from_csv("nonexistent.csv")


def test_invalid_data(invalid_csv_file):
    with pytest.raises(ValueError):
        AssetPortfolioLoader.load_from_csv(invalid_csv_file)


def test_missing_columns():
    # setup.
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "missing_col.csv")

    try:
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["face", "coupon", "maturity"])
            writer.writeheader()
            writer.writerow({"face": "1000", "coupon": "0.05", "maturity": "5.0"})

        with pytest.raises(ValueError) as excinfo:
            AssetPortfolioLoader.load_from_csv(file_path)
        assert "missing required columns" in str(excinfo.value).lower()

    finally:
        # tear-down.
        os.remove(file_path)
        os.rmdir(temp_dir)

# scenario test
def test_load_all_scenarios():
    config_path = r"C:\Users\admin\mfi-alm\src\mfi_alm\engine\config.json"
    result = AssetPortfolioLoader.load_from_scenario(str(config_path))

    assert isinstance(result, dict)
    assert len(result) == 4

    for scen in result.values():
        assert len(scen.assets) == 8

def test_load_single_scenario():
    config_path = r"C:\Users\admin\mfi-alm\src\mfi_alm\engine\config.json"
    result = AssetPortfolioLoader.load_from_scenario(str(config_path),scenario_name="health_crisis")

    assert len(result) == 1
    assert "health_crisis" in result
    assert result["health_crisis"].ytm == 0.04

def test_ytm_adjustment():
    """验证YTM调整因子是否正确应用"""
    config_path = r"C:\Users\admin\mfi-alm\src\mfi_alm\engine\config.json"
    results = AssetPortfolioLoader.load_from_scenario(str(config_path))

    base_ytm = results["base"].ytm
    assert base_ytm == 0.04

    assert results["health_crisis"].ytm == 0.04

    assert results["crazy_markets"].ytm == 0.04*0.75

    assert results["double_whammy"].ytm == 0.04*0.75