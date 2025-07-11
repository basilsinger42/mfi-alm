import os
import tempfile

import pandas as pd
import pytest

from pathlib import Path

from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio
from mfi_alm.liabilities.liability_portfolio_loader import load_liability_portfolio, load_liability_scenarios


@pytest.fixture
def sample_csv_file():
    temp_dir = tempfile.TemporaryDirectory()
    filepath = os.path.join(temp_dir.name, "policyholder_tape.csv")
    df = pd.DataFrame({"policyholder_id": [0, 1], "age": [30, 40], "benefit": [1000, 1500], "mu": [0.05, 0.04]})
    df.to_csv(filepath, index=False)
    yield filepath  # setup.
    temp_dir.cleanup()  # teardown.


def test_load_liability_portfolio(sample_csv_file):
    interest = 0.03
    portfolio = load_liability_portfolio(sample_csv_file, interest=interest)
    assert isinstance(portfolio, LiabilityPortfolio)
    apv = portfolio.insurance_apv()
    assert isinstance(apv, float)


def test_load_success():
    scenarios = load_liability_scenarios(
        Path(__file__).parent.parent.parent / "src" / "mfi_alm" / "engine" / "config.json"
    )

    assert len(scenarios) == 4
    assert "base" in scenarios
    assert "health_crisis" in scenarios
    assert scenarios["base"].policyholders[0].age == 58


def test_load_single_scenario(tmp_path):

    scenarios = load_liability_scenarios(
        Path(__file__).parent.parent.parent / "src" / "mfi_alm" / "engine" / "config.json", "health_crisis"
    )

    assert len(scenarios) == 1
    assert "health_crisis" in scenarios
