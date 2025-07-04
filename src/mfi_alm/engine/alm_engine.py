from pathlib import Path

import os
import sys

from mfi_alm.assets.asset_portfolio_loader import AssetPortfolioLoader
from mfi_alm.liabilities.liability_portfolio_loader import load_liability_portfolio

os.getcwd()
sys.path.append("../src/mfi_alm/assets")
sys.path.append("../src/mfi_alm/liabilities")

print(os.getcwd())

current_script_path = Path(__file__).absolute()

project_root = current_script_path.parent.parent.parent.parent

os.chdir(project_root)

project_root = Path(os.getcwd())
experimental_dir = project_root / "experimental"

os.chdir(experimental_dir)

print(f"Current work path: {os.getcwd()}")

if __name__ == "__main__":
    try:
        portfolio = AssetPortfolioLoader.load_from_csv("asset_tape1.csv")
        print(f"Successfully loaded portfolio with {len(portfolio.assets)} assets")
        print(f"Portfolio market value: {portfolio.market_value():,.2f}")

        liability_portfolio = load_liability_portfolio(filepath="policyholder_tape.csv", interest=0.03)
        print(f"Loaded {len(liability_portfolio.policyholders)} policyholders")
        print(f"Liability portfolio total APV: {liability_portfolio.insurance_apv():,.2f}")
    except Exception as e:
        print(f"Error loading liability portfolio: {str(e)}")
