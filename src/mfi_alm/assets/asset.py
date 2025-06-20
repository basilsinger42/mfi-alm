from .bonds import FixedBond


class Asset:
    """An asset class representing a fixed-rate bond and its market value."""
    def __init__(self, fixed_bond: FixedBond, ytm: float):
        self.fixed_bond = fixed_bond
        self.ytm = ytm

    def market_value(self) -> float:
        return self.fixed_bond.price(ytm=self.ytm)
