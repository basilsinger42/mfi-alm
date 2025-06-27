from pathlib import Path

import csv

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


# Test if loader works
if __name__ == "__main__":
    try:
        portfolio = AssetPortfolioLoader.load_from_csv(r"C:\Users\admin\mfi-alm\experimental/asset_tape1.csv")
        print(f"Successfully loaded portfolio with {len(portfolio.assets)} assets")
        print(f"Portfolio market value: {portfolio.market_value():,.2f}")
    except Exception as e:
        print(f"Error loading portfolio: {str(e)}")
