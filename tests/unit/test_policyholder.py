import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities.mortality import MortalityTable
from mfi_alm.liabilities.insurance import MortalityModel
from mfi_alm.liabilities.insurance import WholeLifeInsurance
from mfi_alm.liabilities.policyholder import Policyholder

@pytest.fixture
def mortality_model() -> MortalityTable:
    df = pd.DataFrame({"x": range(100), "lx": [1000 * np.exp(-0.05 * x) for x in range(100)]})
    return MortalityTable(df)

@pytest.fixture
def whole_life_insurance(mortality_model):
    return WholeLifeInsurance(mortality_model=mortality_model, benefit=1000)

def test_policyholder_init(mortality_model, whole_life_insurance):
    policyholder = Policyholder(id_=1, age=45.0, mortality_model=mortality_model, whole_life_insurance=whole_life_insurance)
    assert policyholder.id_ == 1
    assert policyholder.age == 45.0
    assert isinstance(policyholder.mortality_model, MortalityTable)
    assert isinstance(policyholder.whole_life_insurance, WholeLifeInsurance)

def test_policyholder_copy(mortality_model, whole_life_insurance):
    policyholder = Policyholder(id_=2, age=50.0, mortality_model=mortality_model, whole_life_insurance=whole_life_insurance)
    policyholder_copy = policyholder.copy()
    assert policyholder_copy.id_ == 2
    assert policyholder_copy.age == 50.0
    assert policyholder_copy is not policyholder
    assert policyholder_copy.mortality_model.df.equals(policyholder.mortality_model.df)
