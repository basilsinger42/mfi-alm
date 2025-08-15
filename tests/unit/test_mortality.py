import numpy as np
import pandas as pd
import pytest

from mfi_alm.liabilities import MortalityModel


@pytest.fixture
def mortality_table() -> MortalityModel:
    df_mortality = pd.DataFrame({"x": range(100), "lx": [10**3 * np.exp(-0.05 * x) for x in range(100)]})
    return MortalityModel(df_mortality=df_mortality)


def test_tpx(mortality_table: MortalityModel):
    result = mortality_table.tpx(t=5, x=10)
    expected = mortality_table.df.loc[15, "lx"] / mortality_table.df.loc[10, "lx"]
    assert np.isclose(result, expected)


def test_tqx(mortality_table: MortalityModel):
    result = mortality_table.tqx(t=5, x=10)
    expected = 1 - mortality_table.df.loc[15, "lx"] / mortality_table.df.loc[10, "lx"]
    assert np.isclose(result, expected)


def test_tpx_out_of_bounds(mortality_table: MortalityModel):
    assert mortality_table.tpx(t=5, x=-5) == 1.0
    assert mortality_table.tpx(t=200, x=10) == 0.0


def test_tqx_out_of_bounds(mortality_table: MortalityModel):
    assert mortality_table.tqx(t=5, x=-5) == 0.0
    assert mortality_table.tqx(t=200, x=10) == 1.0


def test_prob_Kx_equals_k(mortality_table: MortalityModel):
    prob = mortality_table.prob_Kx_equals_k(5, 30)
    assert 0 <= prob <= 1
    assert isinstance(prob, float)


def test_discrete_probs_sum_to_one(mortality_table: MortalityModel):
    probs = mortality_table.discrete_remaining_mortality_probs(40, 60)
    assert isinstance(probs, np.ndarray)
    assert np.isclose(probs.sum(), 1.0, atol=1e-6)


def test_simulate_remaining_death_year(mortality_table: MortalityModel):
    year = mortality_table.simulate_remaining_death_year(x=35, seed=123)
    assert isinstance(year, int)
    assert 0 <= year <= 120


def test_simulate_remaining_death_year_for_dead(mortality_table: MortalityModel):
    assert mortality_table.simulate_remaining_death_year(x=150) == 0


def test_tqx_vector_correctness(mortality_table: MortalityModel):
    x = 30
    years = 5
    result = mortality_table.tqx_vector(x=x, years=years)

    expected = np.array([mortality_table.tqx(1, x + t) for t in range(years)])
    assert isinstance(result, np.ndarray)
    assert result.shape == (years,)
    assert np.allclose(result, expected, atol=1e-8)
