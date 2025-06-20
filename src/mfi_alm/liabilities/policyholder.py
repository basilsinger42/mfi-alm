from dataclasses import dataclass, field
from typing import Self

from mfi_alm.liabilities.insurance import WholeLifeInsurance
from mfi_alm.liabilities.insurance import MortalityModel   # use Protocol if applicable

@dataclass(frozen=True, slots=True)
class Policyholder:
    id_: int
    age: float
    mortality_model: MortalityModel = field(repr=False)
    whole_life_insurance: WholeLifeInsurance = field(repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "mortality_model", self.mortality_model.copy())
        object.__setattr__(self, "whole_life_insurance", self.whole_life_insurance.copy())

    def copy(self) -> Self:
        return Policyholder(
            id_=self.id_,
            age=self.age,
            mortality_model=self.mortality_model.copy(),
            whole_life_insurance=self.whole_life_insurance.copy()
        )
