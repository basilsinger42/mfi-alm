import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import MortalityModel, WholeLifeInsurance, Policyholder, LiabilityPortfolio


@pytest.fixture
def mortality_model() -> MortalityModel:
    df = pd.DataFrame({
        "x": range(121),
        "lx": [1000 * np.exp(-0.05 * x) for x in range(121)]
    })
    return MortalityModel(df_mortality=df)


@pytest.fixture
def policyholders(mortality_model) -> list[Policyholder]:
    holders = []
    for i, age in enumerate([30.0, 40.0, 50.0]):
        insurance = WholeLifeInsurance(mortality_model, benefit=1000.0)
        holder = Policyholder(
            id_=i,
            age=age,
            mortality_model=mortality_model,
            whole_life_insurance=insurance
        )
        holders.append(holder)
    return holders


@pytest.fixture
def portfolio(policyholders) -> LiabilityPortfolio:
    return LiabilityPortfolio(policyholders)


def test_portfolio_initialization(policyholders, portfolio):
    assert len(portfolio.policyholders) == len(policyholders)
    for p1, p2 in zip(policyholders, portfolio.policyholders):
        assert p1.id_ == p2.id_
        assert p1.age == p2.age
        assert p1 is not p2  # confirm it's a deep copy


def test_portfolio_insurance_apv(portfolio):
    apv = portfolio.insurance_apv()
    assert isinstance(apv, float)
    assert apv > 0
    assert apv < 1000 * 3
