from time import perf_counter

import os

from mfi_alm.assets.asset_portfolio import AssetPortfolio
from mfi_alm.assets.asset_portfolio_loader import AssetPortfolioLoader
from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio
from mfi_alm.liabilities.liability_portfolio_loader import load_liability_portfolio
from mfi_alm.utils import get_time

CONFIG = {
    "asset_path": os.path.join("data", "asset_tape.csv"),
    "liability_path": os.path.join("data", "policyholder_tape.csv"),
    "liability_interest": 0.03,
    "initial_capital": 1_000_000,
    "scenarios": [
        {"name": "base", "ytm_factor": 1.0, "mortality_factor": 1.0},
        {"name": "health_crisis", "ytm_factor": 1.0, "mortality_factor": 1.25},
        {"name": "crazy_markets", "ytm_factor": 0.75, "mortality_factor": 1.0},
        {"name": "double_whammy", "ytm_factor": 0.75, "mortality_factor": 1.25},
    ],
}


def check_paths(config: dict[str, float | str]) -> None:
    for k, v in config.items():
        if "path" in k:
            if not os.path.exists(v):
                raise ValueError(f"path={k} not found.")


def step0_load_asset_and_liability_tapes(
    config: dict[str, float | str], step: int
) -> tuple[AssetPortfolio, LiabilityPortfolio]:
    tic = perf_counter()
    print(f"Step{step}: Loading asset & liability tapes.")
    check_paths(config=config)
    interest = config["liability_interest"]
    asset_portfolio = AssetPortfolioLoader.load_from_csv(config["asset_path"])
    liability_portfolio = load_liability_portfolio(filepath=config["liability_path"], interest=interest)

    print(f"Successfully loaded portfolio with {len(asset_portfolio.assets)} assets.")
    print(f"Liability portfolio total APV: {liability_portfolio.insurance_apv():,.2f}")
    toc = perf_counter()
    t, units = get_time(t=toc - tic, dp=2)
    print(f"Time taken (loading asset & liability tapes) = {t} {units}.")
    return asset_portfolio, liability_portfolio


if __name__ == "__main__":
    print("*" * 100)
    print("*" * 100)
    print("Starting programme.")
    tic_overall = perf_counter()

    asset_portfolio, liability_portfolio = step0_load_asset_and_liability_tapes(config=CONFIG, step=0)
    initial_capital = CONFIG["initial_capital"]

    toc_overall = perf_counter()
    t, units = get_time(t=toc_overall - tic_overall, dp=2)
    print(f"\nTime taken (overall) = {t} {units}.")
    print("Ending programme.")
    print("*" * 100)
    print("*" * 100)
