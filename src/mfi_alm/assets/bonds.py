
from mfi_alm.assets.asset import Asset

"""
TODO:

Create a class called FixedBond (e.g., leverage asset_type_pricing.ipynb logic). It should inherit attributes
from the general Asset class.
"""

from dataclasses import dataclass, field
from typing import Optional, Union
import datetime
from mfi_alm.assets.asset import Asset

DateLike = Union[str, datetime.date]

@dataclass
class FixedBond(Asset):
    """Inherent from Asset"""
    cusip: str
    par_value: float
    annual_coupon_rate: float
    annual_frequency: int
    maturity_date: datetime.date
    issue_date: datetime.date
    currency: str
    first_call_date: Optional[datetime.date] = None
    call_price: Optional[float] = None

    coupon_per_period: float = field(init=False)

    def __post_init__(self):
        """post-initialization processing"""
        if self.annual_coupon_rate > 1:
            self.annual_coupon_rate /= 100.0
        self.maturity_date = self._parse_date(self.maturity_date)
        self.issue_date = self._parse_date(self.issue_date)
        self.first_call_date = self._parse_date(self.first_call_date) if self.first_call_date else None
        self.coupon_per_period = (self.par_value * self.annual_coupon_rate) / self.annual_frequency
        if self.call_price and self.call_price < 0:
            raise ValueError("Redemption price cannot be negative")

    @staticmethod
    def _parse_date(date: DateLike) -> datetime.date:
        if isinstance(date, str):
            return datetime.datetime.strptime(date, "%m/%d/%Y").date()
        return date

    @classmethod
    def from_percent(cls, cusip: str, par_value: float, annual_coupon_rate: float, **kwargs) -> "FixedBond":
        return cls(cusip=cusip, par_value=par_value, annual_coupon_rate=annual_coupon_rate, **kwargs)