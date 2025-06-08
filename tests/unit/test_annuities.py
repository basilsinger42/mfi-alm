import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import AnnuityDue, MortalityTable


@pytest.fixture
def mortality_table() -> MortalityTable:
    df_mortality = pd.DataFrame({"x": range(100), "lx": [10**3*np.exp(-0.05*x) for x in range(100)]})
    return MortalityTable(df_mortality=df_mortality)


def test_annuity_due(mortality_table: MortalityTable):
    annuity_due = AnnuityDue(mortality_table=mortality_table, i=0.05)
    assert True ### REMOVE.
    ## assert annuity_due.apv(...) === correct_answer