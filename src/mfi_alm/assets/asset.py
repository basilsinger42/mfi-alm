from dataclasses import dataclass
"""
TODO:
Create a general asset class that contains the following attributes:
price, cusip. Can leverage info from placeholder function.ipynb.
@dataclass
class Asset:
    market_price: float
    growth_rate: float

    def evolve_end_of_month(self, scenario: dict):
        # Placeholder logic (e.g. apply growth)
        pass

    def scale(self, reserve: float):
        # Placeholder logic
        pass

    def sell(self, expense: float):
        # Placeholder logic
        pass

Include the following methods:
evolve_end_of_month
scale
sell
buy
"""

"""
@dataclass
class Asset:
    market_price: float
    growth_rate: float

    def evolve_end_of_month(self, scenario: dict):
        # Placeholder logic (e.g. apply growth)
        pass

    def scale(self, reserve: float):
        # Placeholder logic
        pass

    def sell(self, expense: float):
        # Placeholder logic
        pass
"""

from .bonds import FixedBond


class Asset:
    """An asset class representing a fixed-rate bond and its market value."""
    def __init__(self, fixed_bond: FixedBond, ytm: float):
        self.fixed_bond = fixed_bond
        self.ytm = ytm

    def market_value(self) -> float:
        return self.fixed_bond.price(ytm=self.ytm)