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

    def projected_average_yields(self, years: int) -> np.ndarray:
        if len(self.assets) == 0:
            return np.zeros(years)

        all_values = np.array(
            [a.projected_market_values(years + 1) for a in self.assets]
        )  # shape: (num_assets, years+1)
        portfolio_values = self.scale * np.mean(all_values, axis=0)  # shape: (years+1,)

        yields = (portfolio_values[1:] - portfolio_values[:-1]) / portfolio_values[:-1]
        return yields

    def age_one_year(self) -> None:
        for asset in self.assets:
            asset.fixed_bond.maturity = max(asset.fixed_bond.maturity - 1, 0)

    def scale_to_target(self, target: float):
        base_value = np.sum([a.market_value() for a in self.assets])
        self.scale = target / base_value if base_value > 0 else 0.0

    def copy(self) -> Self:
        return AssetPortfolio(assets=[a.copy() for a in self.assets], scale=self.scale)
