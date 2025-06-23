
from typing import Self
from mfi_alm.liabilities import WholeLifeInsurance, MortalityModel


class Policyholder:
    def __init__(
        self,
        id_: int,
        age: float,
        mortality_model: MortalityModel,
        whole_life_insurance: WholeLifeInsurance,
    ):
        self.id_ = id_
        self.age = age
        self.mortality_model = mortality_model.copy()
        self.whole_life_insurance = whole_life_insurance.copy()

    def copy(self) -> Self:
        return Policyholder(
            id_=self.id_,
            age=self.age,
            mortality_model=self.mortality_model.copy(),
            whole_life_insurance=self.whole_life_insurance.copy(),
        )

    def insurance_apv(self, interest: float = 0.03) -> float:
        return self.whole_life_insurance.apv(self.age, interest)
