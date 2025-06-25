from .bonds import FixedBond
from typing import Self
import numpy as np
from copy import deepcopy


class Asset:
    """An asset class representing a fixed-rate bond and its market value."""

    def __init__(self, fixed_bond: FixedBond, ytm: float):
        self.fixed_bond = fixed_bond
        self.ytm = ytm

    def market_value(self) -> float:
        return self.fixed_bond.price(ytm=self.ytm)

    def copy(self) -> Self:
        return Asset(fixed_bond=self.fixed_bond.copy(), ytm=self.ytm)


class AssetPortfolio:

    def __init__(self, assets: list[Asset], ytm: float):
        self.assets = [a.copy() for a in assets]
        self.ytm = ytm

    def market_value(self) -> float:
        return np.sum([a.market_value() for a in self.assets])

    def copy(self) -> Self:
        return AssetPortfolio(assets=deepcopy(self.assets), ytm=self.ytm)
