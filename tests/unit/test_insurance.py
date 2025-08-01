import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import MortalityModel, WholeLifeInsurance


@pytest.fixture
def mortality_model() -> MortalityModel:
    df = pd.DataFrame({"x": range(100), "lx": [1000 * np.exp(-0.05 * x) for x in range(100)]})
    return MortalityModel(df)


def test_whole_life_insurance_apv(mortality_model: MortalityModel):
    insurance = WholeLifeInsurance(mortality_model, benefit=1000)
    apv = insurance.apv(x=30, interest=0.03)
    assert np.isclose(apv, 620.599642481655)


def test_whole_life_insurance_copy(mortality_model):
    insurance = WholeLifeInsurance(mortality_model, benefit=500)
    insurance_copy = insurance.copy()
    assert insurance_copy.benefit == insurance.benefit
    assert isinstance(insurance_copy.mortality_model, MortalityModel)
    assert insurance_copy.mortality_model.df.equals(insurance.mortality_model.df)
