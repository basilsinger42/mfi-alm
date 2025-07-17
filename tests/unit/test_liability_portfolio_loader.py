import os
import tempfile

import pandas as pd
import pytest

from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio
from mfi_alm.liabilities.liability_portfolio_loader import load_liability_portfolio


@pytest.fixture
def sample_csv_file():
    temp_dir = tempfile.TemporaryDirectory()
    filepath = os.path.join(temp_dir.name, "policyholder_tape.csv")
    df = pd.DataFrame({"policyholder_id": [0, 1], "age": [30, 40], "benefit": [1000, 1500], "mu": [0.05, 0.04]})
    df.to_csv(filepath, index=False)
    yield filepath  # setup.
    temp_dir.cleanup()  # teardown.


def test_load_liability_portfolio(sample_csv_file):
    portfolio = load_liability_portfolio(filepath=sample_csv_file, mortality_factor=1.0, interest=0.03)
    assert isinstance(portfolio, LiabilityPortfolio)
    assert len(portfolio.policyholders) == 2
    assert portfolio.policyholders[0].age == 30
    assert portfolio.policyholders[1].whole_life_insurance.benefit == 1500
    assert portfolio.interest == 0.03


def test_mortality_factor_application(sample_csv_file):
    base_portfolio = load_liability_portfolio(filepath=sample_csv_file, mortality_factor=1.0, interest=0.03)
    crisis_portfolio = load_liability_portfolio(filepath=sample_csv_file, mortality_factor=1.25, interest=0.03)
    base_qx = base_portfolio.policyholders[0].mortality_model.tqx(1, 30)
    crisis_qx = crisis_portfolio.policyholders[0].mortality_model.tqx(1, 30)
    assert crisis_qx == pytest.approx(base_qx * 1.25, rel=0.01)
