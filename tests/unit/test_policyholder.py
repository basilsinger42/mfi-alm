import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import WholeLifeInsurance, Policyholder, MortalityModel


@pytest.fixture
def mortality_model() -> MortalityModel:
    ages = np.arange(0, 121)
    lx_values = 1000 * np.exp(-0.05 * ages)
    df = pd.DataFrame({"x": ages, "lx": lx_values})
    return MortalityModel(df_mortality=df)


@pytest.fixture
def default_age() -> float:
    return 40.0


@pytest.fixture
def default_benefit() -> float:
    return 1000.0


@pytest.fixture
def whole_life_insurance(mortality_model, default_benefit) -> WholeLifeInsurance:
    return WholeLifeInsurance(mortality_model=mortality_model, benefit=default_benefit)


@pytest.fixture
def policyholder(mortality_model, whole_life_insurance, default_age) -> Policyholder:
    return Policyholder(
        id_=123,
        age=default_age,
        mortality_model=mortality_model,
        whole_life_insurance=whole_life_insurance,
    )


def test_policyholder_init(policyholder, default_age):
    assert policyholder.id_ == 123
    assert policyholder.age == default_age


def test_policyholder_copy(policyholder):
    ph_copy = policyholder.copy()

    assert ph_copy.id_ == policyholder.id_
    assert ph_copy.age == policyholder.age
    assert ph_copy is not policyholder


@pytest.mark.parametrize("interest", [0.01, 0.03, 0.05])
def test_insurance_apv_from_policyholder(policyholder, interest, whole_life_insurance):
    apv = policyholder.insurance_apv(interest=interest)
    assert np.isclose(apv, whole_life_insurance.apv(policyholder.age, interest=interest))


def test_policyholder_benefit_property(policyholder, default_benefit):
    assert policyholder.benefit == default_benefit
