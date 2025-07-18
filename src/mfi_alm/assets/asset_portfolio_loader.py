import pandas as pd
import json
from mfi_alm.assets.asset import Asset, FixedBond
from mfi_alm.assets.asset_portfolio import AssetPortfolio


class AssetPortfolioLoader:
    def load_asset_portfolio(file_path: str, ytm_factor: float) -> AssetPortfolio:
        df = pd.read_csv(file_path)
        assets = []
        for i, r in df.iterrows():
            bond = FixedBond(face=r["face"], coupon=r["coupon"], maturity=r["maturity"], freq=r["freq"])
            assets.append(Asset(fixed_bond=bond, ytm=r["ytm"] * ytm_factor))

        return AssetPortfolio(assets=assets)

    def load_from_config(config_path: str) -> dict:
        with open(config_path) as f:
            config = json.load(f)
        portfolios = {}
        for scenario in config["scenarios"]:
            portfolio = AssetPortfolioLoader.load_asset_portfolio(
                file_path=config["asset_path"], ytm_factor=scenario["ytm_factor"]
            )
            portfolios[scenario["name"]] = portfolio
        return portfolios
