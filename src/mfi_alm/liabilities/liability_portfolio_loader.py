import numpy as np
import pandas as pd
import json
from pathlib import Path
from typing import Optional

from mfi_alm.liabilities.insurance import WholeLifeInsurance
from mfi_alm.liabilities.mortality import MortalityModel
from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio
from mfi_alm.liabilities.policyholder import Policyholder


def create_mortality_model(mu: float, mortality_factor: float = 1.0) -> MortalityModel:
    ages = np.arange(0, 121)
    adjusted_mu = mu * mortality_factor
    lx = 1000 * np.exp(-adjusted_mu * ages)
    df = pd.DataFrame({"x": ages, "lx": lx})
    return MortalityModel(df_mortality=df)


def load_liability_portfolio(
    filepath: str = "data/policyholder_tape.csv", interest: float = 0.03, mortality_factor: float = 1.0
) -> LiabilityPortfolio:
    df = pd.read_csv(filepath)
    policyholders = []

    for _, row in df.iterrows():
        mortality_model = create_mortality_model(row["mu"], mortality_factor)
        insurance = WholeLifeInsurance(mortality_model, benefit=row["benefit"])
        policyholder = Policyholder(
            id_=int(row["policyholder_id"]),
            age=float(row["age"]),
            mortality_model=mortality_model,
            whole_life_insurance=insurance,
        )
        policyholders.append(policyholder)

    return LiabilityPortfolio(policyholders, interest=interest)


def load_liability_scenarios(config_path: str, scenario_name: Optional[str] = None) -> dict[str, LiabilityPortfolio]:

    config_path = Path(config_path).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Scene profile not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    project_root = Path(__file__).parent.parent.parent.parent
    liability_path = (project_root / config["liability_path"]).resolve()

    if not liability_path.exists():
        raise FileNotFoundError(f"Liability data file not found: {liability_path}")

    results = {}
    for scenario in config["scenarios"]:
        if scenario_name and scenario["name"] != scenario_name:
            continue

        portfolio = load_liability_portfolio(
            filepath=str(liability_path),
            interest=config["liability_interest"],
            mortality_factor=scenario["mortality_factor"],
        )

        results[scenario["name"]] = portfolio

    return results


# Test
if __name__ == "__main__":
    try:
        base_portfolio = load_liability_portfolio()
        print(f"Base liability portfolio loaded successfully, number of policies: {len(base_portfolio.policyholders)}")

        config_path = "src/mfi_alm/engine/config.json"
        print("\nLoading all scenarios...")
        scenarios = load_liability_scenarios(config_path)

        for name, portfolio in scenarios.items():
            print(
                f"  {name}: {len(portfolio.policyholders)}policies，"
                f"Adjusted mortality rate: {scenarios[name].policyholders[0].mortality_model.df['lx'][1] / 1000:.3f}"
            )

        print("\nLoading health_crisis...")
        crisis = load_liability_scenarios(config_path, "health_crisis")
        print(
            f"  Adjusted mortality rate: "
            f"{crisis['health_crisis'].policyholders[0].mortality_model.df['lx'][1] / 1000:.3f}"
        )

    except Exception as e:
        print(f"\n[error] {type(e).__name__}: {str(e)}")
