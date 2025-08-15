from time import perf_counter
from typing import Any
import os
import json
import csv
import numpy as np

from mfi_alm.assets.asset_portfolio import AssetPortfolio
from mfi_alm.assets.asset_portfolio_loader import AssetPortfolioLoader
from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio
from mfi_alm.liabilities.liability_portfolio_loader import load_liability_portfolio
from mfi_alm.utils import get_time

CONFIG_PATH = "data/config.json"
OUTPUT_DIR = "data/outputs"


def ensure_output_dir_exists():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


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


class ScenarioSimulator:
    def __init__(
        self,
        asset_portfolio: AssetPortfolio,
        liability_portfolio: LiabilityPortfolio,
        initial_capital: float,
        maximum_capital: float,
        years: int,
        max_iterations: int = 30,
        tolerance: float = 1000,
        minimum_capital: float = 0.0,
    ):
        self.asset_portfolio = asset_portfolio
        self.liability_portfolio = liability_portfolio
        self.initial_capital = initial_capital
        self.maximum_capital = maximum_capital
        self.minimum_capital = minimum_capital
        self.years = years
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.iteration_info = {}
        self.final_capital = None
        self.total_time = None
        self.converged = False

    def run(self) -> None:
        tic = perf_counter()
        min_val = self.minimum_capital
        max_val = self.maximum_capital
        capital = self.initial_capital

        for i in range(self.max_iterations):
            print(f"Iteration {i + 1:02d}...", end=" ")
            scaled_assets = self.asset_portfolio.copy()
            scaled_assets.scale_to_target(capital)
            liabilities_copy = self.liability_portfolio.copy()

            tic_iteration = perf_counter()
            iteration_result = self.simulate_cashflows(
                capital=capital, asset_portfolio=scaled_assets, liability_portfolio=liabilities_copy
            )
            final_reserve = iteration_result["reserves"][-1]
            toc_iteration = perf_counter()
            t, units = get_time(t=toc_iteration - tic_iteration, dp=2)

            print(f"Capital=${capital:,.2f}, Final Reserve=${final_reserve:,.2f}, Time taken={t} {units}.")

            # Ensure the dictionary includes 'min_val' and 'max_val'
            self.iteration_info[i] = {
                "iteration": i + 1,
                "capital": capital,
                "final_reserve": final_reserve,
                "min_val": min_val,  # Ensure 'min_val' is always included
                "max_val": max_val,  # Ensure 'max_val' is always included
                **iteration_result,
            }

            if abs(final_reserve) < self.tolerance:
                self.converged = True
                break

            if final_reserve < 0:
                min_val = capital
            else:
                max_val = capital

            capital = (min_val + max_val) / 2

        self.final_capital = capital
        toc = perf_counter()
        t, units = get_time(toc - tic, dp=2)
        self.total_time = {"t": t, "units": units}

    def simulate_cashflows(
        self, capital: float, asset_portfolio: AssetPortfolio, liability_portfolio: LiabilityPortfolio
    ) -> dict[str, list[float]]:
        asset_yields = asset_portfolio.projected_average_yields(self.years)
        liability_benefits = liability_portfolio.projected_expected_yearly_benefits(self.years)

        growth_factors = np.cumprod(1 + asset_yields)

        adjusted_liabilities = np.cumsum(liability_benefits / growth_factors) * growth_factors

        reserves = capital * growth_factors - adjusted_liabilities

        reserves = np.concatenate([[capital], reserves])

        return {
            "reserves": reserves.tolist(),
            "asset_yields": asset_yields.tolist(),
            "liability_expected_yearly_benefits": liability_benefits.tolist(),
        }

    def output_report(self, scenario_name: str) -> None:
        detailed_path = os.path.join(OUTPUT_DIR, f"output_{scenario_name}_report_detailed.csv")
        summary_path = os.path.join(OUTPUT_DIR, f"output_{scenario_name}_report.csv")

        # Detailed report (all iterations, all years)
        with open(detailed_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Iteration",
                    "Capital",
                    "Final Reserve",
                    "Min Bound",
                    "Max Bound",
                    "Year",
                    "Reserve",
                    "Asset Yield",
                    "Liability Benefit",
                ]
            )
            for i, info in self.iteration_info.items():
                for year, (reserve, yld, liability) in enumerate(
                    zip(
                        info["reserves"],
                        [None] + info["asset_yields"],
                        [None] + info["liability_expected_yearly_benefits"],
                    )
                ):
                    writer.writerow(
                        [
                            i + 1,
                            info["capital"],
                            info["final_reserve"],
                            info["min_val"],
                            info["max_val"],
                            year,
                            reserve,
                            yld,
                            liability,
                        ]
                    )

        # Summary report (only final result)
        with open(summary_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Scenario", "Final Capital", "Converged", "Final Reserve", "Time", "Units"])
            last_iter = list(self.iteration_info.values())[-1] if self.iteration_info else {}
            writer.writerow(
                [
                    scenario_name,
                    self.final_capital,
                    self.converged,
                    last_iter.get("final_reserve", None),
                    self.total_time["t"],
                    self.total_time["units"],
                ]
            )


if __name__ == "__main__":
    print("*" * 100)
    print("Starting programme.")
    tic_overall = perf_counter()

    config_data = step0_load_config(step=0)
    ensure_output_dir_exists()
    paths = (config_data["asset_path"], config_data["liability_path"])
    max_years = config_data.get("projection_horizon", 30)
    max_iterations = config_data.get("max_iterations", 30)

    for scenario in config_data["scenarios"]:
        print(f"\nProcessing scenario: {scenario['name']}")

        tic_scenario = perf_counter()

        asset_portfolio, liability_portfolio = step1_load_asset_and_liability_tapes(
            paths=paths, scenario_data=scenario, liability_interest=config_data["liability_interest"], step=1
        )

        scenario_simulator = ScenarioSimulator(
            asset_portfolio=asset_portfolio,
            liability_portfolio=liability_portfolio,
            initial_capital=config_data["initial_capital"],
            maximum_capital=config_data["maximum_capital"],
            years=max_years,
            max_iterations=max_iterations,
        )

        scenario_simulator.run()
        print(f"Final capital required for scenario '{scenario['name']}': ${scenario_simulator.final_capital:,.2f}")
        scenario_simulator.output_report(scenario_name=scenario["name"])

        toc_scenario = perf_counter()
        t, units = get_time(toc_scenario - tic_scenario, dp=2)
        print(f"Time taken for scenario '{scenario['name']}' = {t} {units}.")

    toc_overall = perf_counter()
    t, units = get_time(toc_overall - tic_overall, dp=2)
    print(f"\nTime taken (overall) = {t} {units}.")
    print("Ending programme.")
    print("*" * 100)
