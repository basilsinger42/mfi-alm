import numpy as np
import pandas as pd


from mfi_alm.liabilities.insurance import WholeLifeInsurance
from mfi_alm.liabilities.mortality import MortalityModel
from mfi_alm.liabilities.liability_portfolio import LiabilityPortfolio
from mfi_alm.liabilities.policyholder import Policyholder


def create_mortality_model(mu: float) -> MortalityModel:
    ages = np.arange(0, 121)
    lx = 1000 * np.exp(-mu * ages)
    df = pd.DataFrame({"x": ages, "lx": lx})
    return MortalityModel(df_mortality=df)


def load_liability_portfolio(
    filepath: str = "data/policyholder_tape.csv", interest: float = 0.03
) -> LiabilityPortfolio:
    df = pd.read_csv(filepath)
    policyholders = []

    for _, row in df.iterrows():
        mortality_model = create_mortality_model(row["mu"])
        insurance = WholeLifeInsurance(mortality_model, benefit=row["benefit"])
        policyholder = Policyholder(
            id_=int(row["id"]), age=float(row["age"]), mortality_model=mortality_model, whole_life_insurance=insurance
        )
        policyholders.append(policyholder)

    return LiabilityPortfolio(policyholders, interest=interest)
