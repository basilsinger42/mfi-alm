from time import perf_counter
from typing import Any

import os
import json

from mfi_alm.assets.asset_portfolio import AssetPortfolio
from mfi_alm.assets.asset_portfolio_loader import AssetPortfolioLoader
from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio
from mfi_alm.liabilities.liability_portfolio_loader import load_liability_portfolio
from mfi_alm.utils import get_time

CONFIG_PATH = "src/mfi_alm/engine/config.json"


def check_paths(config: dict[str, float | str]) -> None:
    for k, v in config.items():
        if "path" in k:
            if not os.path.exists(v):
                raise ValueError(f"path={k} not found.")


def step0_load_config(step: int) -> dict[str, Any]:
    tic = perf_counter()
    with open(CONFIG_PATH) as f:
        config_data = json.load(f)
    toc = perf_counter()
    t, units = get_time(toc - tic)
    print(f"Step {step} (load config) took {t} {units}")
    return config_data


def step1_load_asset_and_liability_tapes(
    paths: tuple[str, str], scenario_data: dict[str, float], liability_interest: float, step: int
) -> tuple[AssetPortfolio, LiabilityPortfolio]:
    tic = perf_counter()
    asset_portfolio = AssetPortfolioLoader.load_asset_portfolio(
        file_path=paths[0], ytm_factor=scenario_data["ytm_factor"]
    )
    liability_portfolio = load_liability_portfolio(
        filepath=paths[1], mortality_factor=scenario_data["mortality_factor"], interest=liability_interest
    )
    toc = perf_counter()
    t, units = get_time(toc - tic)
    print(f"Step {step} (load tapes) took {t} {units}")
    return asset_portfolio, liability_portfolio


if __name__ == "__main__":
    print("*" * 100)
    print("*" * 100)
    print("Starting programme.")
    tic_overall = perf_counter()
    # step0
    config_data = step0_load_config(step=0)
    paths = (config_data["asset_path"], config_data["liability_path"])
    # Outer loop
    for scenario in config_data["scenarios"]:
        print(f"\nProcessing scenario: {scenario['name']}")
        # Step1
        asset_portfolio, liability_portfolio = step1_load_asset_and_liability_tapes(
            paths=paths, scenario_data=scenario, liability_interest=config_data["liability_interest"], step=1
        )
        initial_capital = config_data["initial_capital"]
        print(f"Scenario '{scenario['name']}' loaded:")
        print(f"  - Asset MV: {asset_portfolio.market_value():,.2f}")
        print(f"  - Initial capital: {initial_capital:,.2f}")
    toc_overall = perf_counter()
    t, units = get_time(t=toc_overall - tic_overall, dp=2)
    print(f"\nTime taken (overall) = {t} {units}.")
    print("Ending programme.")
    print("*" * 100)
    print("*" * 100)
