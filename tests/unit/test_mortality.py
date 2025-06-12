import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import MortalityTable


@pytest.fixture
def mortality_table() -> MortalityTable:
    df_mortality = pd.DataFrame({"x": range(100), "lx": [10**3*np.exp(-0.05*x) for x in range(100)]})
    return MortalityTable(df_mortality=df_mortality)

def test_tpx(mortality_table: MortalityTable):
    result = mortality_table.tpx(t=5, x=10)
    expected = mortality_table.df.loc[15, 'lx'] / mortality_table.df.loc[10, 'lx']
    assert np.isclose(result, expected)

def test_tqx(mortality_table: MortalityTable):
    result = mortality_table.tqx(t=5, x=10)
    expected = 1 - mortality_table.df.loc[15, 'lx'] / mortality_table.df.loc[10, 'lx']
    assert np.isclose(result, expected)

def test_invalid_tpx_input(mortality_table: MortalityTable):
    with pytest.raises(ValueError):
        mortality_table.tpx(t=200, x=10)