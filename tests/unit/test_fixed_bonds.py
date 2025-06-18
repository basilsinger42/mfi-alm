"""
TODO: Create unit tests that test bonds.
"""

from mfi_alm.assets import FixedBond

import pytest
import numpy as np

@pytest.fixture
def sample_bond() -> FixedBond:
    """Example of a test bond"""
    return FixedBond(
        face=1000,
        coupon=0.05,
        maturity=5,
        freq=2
    )

def test_cashflows(sample_bond: FixedBond):
    """Test cashflow generation"""
    flows = sample_bond.cashflows()
    #It should generate 10 periods cashflow
    assert len(flows) == 10
    # First period cashflow should be 25 (0.5year, 25dollar)
    assert flows[0] == (0.5, 25)
    # Last period cashflow should be 1025 (5year, 1025dollar)
    assert flows[-1] == (5.0, 1025)

def test_price_at_par(sample_bond: FixedBond):
    """Testing parity bond pricing (YTM = coupon rate)"""
    price = sample_bond.price(ytm=0.05)
    # Prices should be close to face value (1% error allowed)
    assert np.isclose(price, 1000, rtol=1e-2)

def test_price_above_par(sample_bond: FixedBond):
    """Testing premium bond pricing (YTM<coupon rate)"""
    price = sample_bond.price(ytm=0.04)
    assert price > 1000  # Price should be higher than face value

def test_price_below_par(sample_bond: FixedBond):
    """Testing discount bond pricing (YTM > coupon rate)"""
    price = sample_bond.price(ytm=0.06)
    assert price < 1000  # Price should be lower than face value