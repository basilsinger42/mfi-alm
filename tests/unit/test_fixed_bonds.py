import numpy as np
import pytest

from mfi_alm.assets import FixedBond


@pytest.fixture
def sample_bond() -> FixedBond:
    return FixedBond(face=1000, coupon=0.05, maturity=5, freq=2)


def test_cashflows(sample_bond: FixedBond):
    flows = sample_bond.cashflows()

    assert len(flows) == 10
    assert flows[0] == (0.5, 25)
    assert flows[-1] == (5.0, 1025)


def test_price_at_par(sample_bond: FixedBond):
    price = sample_bond.price(ytm=0.05)
    assert np.isclose(price, 1000, rtol=1e-2)


def test_price_above_par(sample_bond: FixedBond):

    price = sample_bond.price(ytm=0.04)
    assert price > 1000


def test_price_below_par(sample_bond: FixedBond):
    price = sample_bond.price(ytm=0.06)
    assert price < 1000


# Age() test
def test_age_normal_case():
    """Test aging the bond by a valid number of years."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=10.0)
    bond.age(2)
    assert bond.maturity == 8.0


def test_age_boundary_case():
    """Test aging the bond exactly to maturity."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=5.0)
    bond.age(5)
    assert bond.maturity == 0.0


def test_age_beyond_maturity():
    """Test aging beyond maturity raises ValueError."""
    bond = FixedBond(face=1000, coupon=0.05, maturity=3.0)
    with pytest.raises(ValueError, match="You cannot age beyond maturity date."):
        bond.age(4)


def test_copy():
    original = FixedBond(face=1000, coupon=0.05, maturity=10, freq=2)

    copied = original.copy()

    assert original.face == copied.face
    assert original.coupon == copied.coupon
    assert original.maturity == copied.maturity
    assert original.freq == copied.freq
