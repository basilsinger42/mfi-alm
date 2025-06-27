import os
import tempfile
import pandas as pd
import pytest

from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio


@pytest.fixture
def sample_csv_file():
    temp_dir = tempfile.TemporaryDirectory()
    filepath = os.path.join(temp_dir.name, "policyholder_tape.csv")
    df = pd.DataFrame({
        "id": [0, 1],
        "age": [30, 40],
        "benefit": [1000, 1500],
        "mu": [0.05, 0.04]
    })
    df.to_csv(filepath, index=False)
    yield filepath  # setup
    temp_dir.cleanup()  # teardown


def test_load_liability_portfolio(sample_csv_file):
    interest = 0.03
    portfolio = load_liability_portfolio(sample_csv_file, interest=interest)
    assert isinstance(portfolio, LiabilityPortfolio)
    apv = portfolio.insurance_apv()
    assert isinstance(apv, float)

