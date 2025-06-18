import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import MortalityTable


@pytest.fixture
def mortality_table() -> MortalityTable:
    df_mortality = pd.DataFrame({"x": range(100), "lx": [10**3*np.exp(-0.05*x) for x in range(100)]})
    return MortalityTable(df_mortality=df_mortality)


def test_tpx(mortality_table: MortalityTable):
    assert np.isclose(mortality_table.tpx(t=5, x=10), 0.7788007830714048)


def test_tqx(mortality_table: MortalityTable):
    assert np.isclose(mortality_table.tqx(t=5, x=10), 0.22119921692859523)


def test_tpx_out_of_bounds(mortality_table: MortalityTable):
    assert mortality_table.tpx(t=5, x=-5) == 1.0
    assert mortality_table.tpx(t=200, x=10) == 0.0


def test_tqx_out_of_bounds(mortality_table: MortalityTable):
    assert mortality_table.tqx(t=5, x=-5) == 0.0
    assert mortality_table.tqx(t=200, x=10) == 1.0


def test_prob_Kx_equals_k(mortality_table: MortalityTable):
    prob = mortality_table.prob_Kx_equals_k(5, 30)
    assert 0 <= prob <= 1
    assert isinstance(prob, float)


def test_discrete_probs_sum_to_one(mortality_table: MortalityTable):
    probs = mortality_table.discrete_remaining_mortality_probs(40, 60)
    assert isinstance(probs, np.ndarray)
    assert np.isclose(probs.sum(), 1.0, atol=1e-6)


def test_simulate_remaining_death_year(mortality_table: MortalityTable):
    year = mortality_table.simulate_remaining_death_year(x=35, seed=123)
    assert isinstance(year, int)
    assert 0 <= year <= 120


def test_simulate_remaining_death_year_for_dead(mortality_table: MortalityTable):
    assert mortality_table.simulate_remaining_death_year(x=150) == 0
