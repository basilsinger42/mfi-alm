"""
TODO: Create unit tests that test bonds.
"""
import pytest
import datetime
from mfi_alm.assets import FixedBond


class TestFixedBond:
    def test_dataclass_features(self):
        """Testing dataclass auto-generation"""
        bond1 = FixedBond(
            cusip="T123",
            par_value=1000,
            annual_coupon_rate=0.045,  # decimal
            annual_frequency=2,
            maturity_date="12/31/2030",
            issue_date=datetime.date(2020, 1, 1),  # Hybrid input
            currency="CAD"
        )

        bond2 = FixedBond.from_percent(
            cusip="T123",
            par_value=1000,
            annual_coupon_rate=4.5,  # Percentage
            annual_frequency=2,
            maturity_date="12/31/2030",
            issue_date="01/01/2020",
            currency="CAD"
        )

        # Testing of automated implementations__eq__
        assert bond1 == bond2

        # Testing__repr__readability
        assert "T123" in repr(bond1)

    def test_coupon_conversion(self):
        """Automatic conversion of test percentages"""
        bond = FixedBond.from_percent(
            cusip="C001",
            par_value=1000,
            annual_coupon_rate=5.0,  # input 5.0%
            annual_frequency=2,
            maturity_date="12/31/2030",
            issue_date="01/01/2023",
            currency="CNY"
        )
        assert bond.annual_coupon_rate == 0.05  # Transformed to decimal
        assert bond.coupon_per_period == 25.0  # (1000 * 0.05)/2
