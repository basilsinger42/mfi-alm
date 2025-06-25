import numpy as np

from mfi_alm.liabilities.policyholder import Policyholder


class LiabilityPortfolio:
    def __init__(self, policyholders: list[Policyholder], interest: float):
        self.policyholders = [p.copy() for p in policyholders]
        self.interest = interest

    def insurance_apv(self) -> float:
        return np.sum([p.insurance_apv(interest=self.interest) for p in self.policyholders])
