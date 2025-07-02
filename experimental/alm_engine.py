#%%
import os
import sys

sys.path.append(r"C:/Users/simia/mfi_alm/src")

from mfi_alm.assets.asset_portfolio_loader import AssetPortfolioLoader
from mfi_alm.liabilities.liability_portfolio_loader import load_liability_portfolio

#%%
if __name__ == "__main__":
    try:
        portfolio = AssetPortfolioLoader.load_from_csv(r"asset_tape1.csv")
        print(f"Successfully loaded portfolio with {len(portfolio.assets)} assets")
        print(f"Portfolio market value: {portfolio.market_value():,.2f}")

        liability_portfolio = load_liability_portfolio(
            filepath=r"C:/Users/simia/mfi_alm/src/mfi_alm/liabilities/policyholder_tape.csv",
            interest=0.03
        )
        print(f"Loaded {len(liability_portfolio.policyholders)} policyholders")
        print(f"Liability portfolio total APV: {liability_portfolio.insurance_apv():,.2f}")
    except Exception as e:
        print(f"Error loading liability portfolio: {str(e)}")