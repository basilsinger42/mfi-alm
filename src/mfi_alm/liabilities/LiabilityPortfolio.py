import numpy as np
from mfi_alm.liabilities import Policyholder


class LiabilityPortfolio:
    def __init__(self, policyholders: list[Policyholder]):
        self.policyholders = [p.copy() for p in policyholders]

    def insurance_apv(self) -> float:
        return np.sum([p.insurance_apv() for p in self.policyholders])
