from typing import Self

import numpy as np

from mfi_alm.liabilities.policyholder import Policyholder


class LiabilityPortfolio:
    def __init__(self, policyholders: list[Policyholder], interest: float):
        self.policyholders = [p.copy() for p in policyholders]
        self.interest = interest

    def insurance_apv(self) -> float:
        return np.sum([p.insurance_apv(interest=self.interest) for p in self.policyholders])

    def expected_yearly_benefit(self) -> float:
        return np.sum([p.benefit * p.mortality_model.tqx(t=1, x=p.age) for p in self.policyholders])

    def age_one_year(self) -> None:
        for p in self.policyholders:
            p.age += 1

    def copy(self) -> Self:
        return LiabilityPortfolio(policyholders=[p.copy() for p in self.policyholders], interest=self.interest)

    def projected_expected_yearly_benefits(self, years: int) -> np.ndarray:

        benefits = np.zeros(years)
        for p in self.policyholders:
            tqx_vector = p.mortality_model.tqx_vector(x=p.age, years=years)
            benefits += p.benefit * tqx_vector
        return benefits
