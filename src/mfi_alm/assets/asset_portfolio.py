from typing import Self

import numpy as np

from mfi_alm.assets.asset import Asset


class AssetPortfolio:
    def __init__(self, assets: list[Asset]):
        self.assets = [a.copy() for a in assets]

    def market_value(self) -> float:
        return np.sum([a.market_value() for a in self.assets])

    def copy(self) -> Self:
        return AssetPortfolio(assets=self.assets.copy())
