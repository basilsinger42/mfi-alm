import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import LiabilityPortfolio, MortalityModel, Policyholder, WholeLifeInsurance


@pytest.fixture
def mortality_model() -> MortalityModel:
    df = pd.DataFrame({"x": range(121), "lx": [1000 * np.exp(-0.05 * x) for x in range(121)]})
    return MortalityModel(df_mortality=df)


@pytest.fixture
def policyholders(mortality_model) -> list[Policyholder]:
    holders = []
    for i, age in enumerate([30.0, 40.0, 50.0]):
        insurance = WholeLifeInsurance(mortality_model, benefit=1000.0)
        holder = Policyholder(id_=i, age=age, mortality_model=mortality_model, whole_life_insurance=insurance)
        holders.append(holder)
    return holders


@pytest.fixture
def portfolio(policyholders) -> LiabilityPortfolio:
    return LiabilityPortfolio(policyholders=policyholders, interest=0.03)


def test_portfolio_initialization(policyholders, portfolio):
    assert len(portfolio.policyholders) == len(policyholders)
    for p1, p2 in zip(policyholders, portfolio.policyholders):
        assert p1.id_ == p2.id_
        assert p1.age == p2.age
        assert p1 is not p2  # confirm it's a deep copy.


def test_portfolio_insurance_apv(portfolio):
    apv = portfolio.insurance_apv()
    expected_apv = np.sum([p.insurance_apv(interest=0.03) for p in portfolio.policyholders])
    assert np.isclose(apv, expected_apv)


def test_expected_yearly_benefit(portfolio):
    expected = np.sum(
        [p.whole_life_insurance.benefit * p.mortality_model.tqx(t=1, x=p.age) for p in portfolio.policyholders]
    )
    actual = portfolio.expected_yearly_benefit()
    assert np.isclose(actual, expected)


def test_age_one_year(portfolio):
    original_ages = [p.age for p in portfolio.policyholders]
    portfolio.age_one_year()
    updated_ages = [p.age for p in portfolio.policyholders]
    for orig, updated in zip(original_ages, updated_ages):
        assert updated == orig + 1
