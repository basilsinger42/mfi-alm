from pathlib import Path

import csv
import json

from mfi_alm.assets.asset import Asset, FixedBond
from mfi_alm.assets.asset_portfolio import AssetPortfolio


class AssetPortfolioLoader:

    @staticmethod
    def load_from_csv(file_path: str) -> AssetPortfolio:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Asset file not found: {file_path}")

        assets = []
        total_ytm = 0.0
        asset_count = 0

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_columns = {"face", "coupon", "maturity", "ytm"}
            if not required_columns.issubset(reader.fieldnames):
                missing = required_columns - set(reader.fieldnames)
                raise ValueError(f"CSV missing required columns: {missing}")

            for row in reader:
                try:
                    # FixedBond
                    bond = FixedBond(
                        face=float(row["face"]),
                        coupon=float(row["coupon"]),
                        maturity=float(row["maturity"]),
                        freq=int(row.get("freq", 2)),
                    )

                    # Asset
                    ytm = float(row["ytm"])
                    asset = Asset(fixed_bond=bond, ytm=ytm)

                    assets.append(asset)
                    total_ytm += ytm
                    asset_count += 1

                except (ValueError, KeyError) as e:
                    raise ValueError(f"Error processing row {reader.line_num}: {str(e)}")

        if asset_count == 0:
            raise ValueError("No valid assets found in the file")

        avg_ytm = total_ytm / asset_count
        return AssetPortfolio(assets=assets, ytm=avg_ytm)

    @staticmethod
    def load_from_scenario(scenario_file: str, scenario_name: str = None) -> dict[str, AssetPortfolio]:
        scenario_path = Path(scenario_file).resolve()
        if not scenario_path.exists():
            raise FileNotFoundError(f"Scenario file not found: {scenario_path}")

        with open(scenario_path, "r", encoding="utf-8") as f:
            scenario_config = json.load(f)

        project_root = Path(__file__).parent.parent.parent.parent
        asset_path = (project_root / scenario_config["asset_path"]).resolve()

        if not asset_path.exists():
            raise FileNotFoundError(
                f"Asset file not found: {asset_path}\n"
                f"Project root: {project_root}\n"
                f"Config path: {scenario_path}"
        )

        base_portfolio = AssetPortfolioLoader.load_from_csv(str(asset_path))

        results = {}
        for scenario in scenario_config["scenarios"]:
            if scenario_name and scenario["name"] != scenario_name:
                continue

            adjusted_assets = []
            total_ytm = 0.0
            for asset in base_portfolio.assets:
                adjusted_ytm = asset.ytm * scenario["ytm_factor"]
                adjusted_asset = Asset(
                    fixed_bond=asset.fixed_bond,
                    ytm=adjusted_ytm
                )
                adjusted_assets.append(adjusted_asset)
                total_ytm += adjusted_ytm

            avg_ytm = total_ytm / len(adjusted_assets) if adjusted_assets else 0
            results[scenario["name"]] = AssetPortfolio(
                assets=adjusted_assets,
                ytm=avg_ytm
            )

        return results



# Test if loader works
if __name__ == "__main__":
    try:
        portfolio = AssetPortfolioLoader.load_from_csv(r"C:\Users\admin\mfi-alm\data\asset_tape.csv")
        print(f"Successfully loaded portfolio with {len(portfolio.assets)} assets")
        print(f"Portfolio market value: {portfolio.market_value():,.2f}")
    except Exception as e:
        print(f"Error loading portfolio: {str(e)}")

if __name__ == "__main__":
    try:
        project_root = Path(__file__).parent.parent.parent.parent
        print(project_root)

        csv_path = project_root / "data" / "asset_tape.csv"
        portfolio = AssetPortfolioLoader.load_from_csv(str(csv_path))
        print(f"[CSV test] Loading Assets Number: {len(portfolio.assets)}, Average YTM: {portfolio.ytm:.2%}")

        config_path = project_root / "src" / "mfi_alm" / "engine" / "config.json"
        print("\n[scenario test] Loading all senarios...")
        scenarios = AssetPortfolioLoader.load_from_scenario(str(config_path))
        print(scenarios)

        for name, scen in scenarios.items():
            print(f"  {name}: {len(scen.assets)}asset, YTM: {scen.ytm:.2%}")

        print("\n[scenario test] Only load health_crisis...")
        crisis = AssetPortfolioLoader.load_from_scenario(
            str(config_path),
            scenario_name="health_crisis"
        )
        print(f"  health_crisis YTM: {crisis['health_crisis'].ytm:.2%}")

    except Exception as e:
        print(f"\n[error] {type(e).__name__}: {str(e)}")
        if hasattr(e, "path"):
            print(f"Path error: {e.path}")