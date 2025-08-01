from typing import Self

import numpy as np

from mfi_alm.assets.asset import Asset


class AssetPortfolio:
    def __init__(self, assets: list[Asset], scale: float = 1.0):
        self.assets = [a.copy() for a in assets]
        self.scale = scale

    def market_value(self) -> float:
        return self.scale * np.sum([a.market_value() for a in self.assets])

    def average_yield(self) -> float:
        if len(self.assets) == 0:
            return 0.0
        return np.mean([a.ytm for a in self.assets])

    def age_one_year(self) -> None:
        for asset in self.assets:
            asset.fixed_bond.maturity = max(asset.fixed_bond.maturity - 1, 0)

    def scale_to_target(self, target: float):
        base_value = np.sum([a.market_value() for a in self.assets])
        self.scale = target / base_value

    def copy(self) -> Self:
        return AssetPortfolio(assets=[a.copy() for a in self.assets], scale=self.scale)
