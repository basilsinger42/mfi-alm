import numpy as np
import pandas as pd

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


def load_liability_portfolio(filepath: str, mortality_factor: float, interest: float) -> LiabilityPortfolio:
    df = pd.read_csv(filepath)
    policyholders = []
    for _, r in df.iterrows():
        adjusted_mu = r["mu"] * mortality_factor
        mortality_model = create_mortality_model(adjusted_mu)
        policyholders.append(
            Policyholder(
                id_=r["policyholder_id"],
                age=r["age"],
                mortality_model=mortality_model,
                whole_life_insurance=WholeLifeInsurance(mortality_model=mortality_model, benefit=r["benefit"]),
            )
        )
    return LiabilityPortfolio(policyholders, interest=interest)
