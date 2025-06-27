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
