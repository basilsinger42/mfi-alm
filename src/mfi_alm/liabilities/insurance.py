from typing import Protocol, Self

class MortalityModel(Protocol):
    def prob_Kx_equals_k(self, k: int, x: float) -> float: ...
    def copy(self) -> Self: ...

class WholeLifeInsurance:
    def __init__(self, mortality_model: MortalityModel, benefit: float | None = 1.0) -> None:
        self.mortality_model = mortality_model
        self.benefit = benefit

    def copy(self) -> Self:
        return WholeLifeInsurance(mortality_model=self.mortality_model.copy(), benefit=self.benefit)

    def apv(self, x: float, interest: float = 0.03, max_age: int = 120) -> float:
        """
        Compute actuarial present value of a whole life insurance benefit payable at end of year of death.
        """
        v = 1 / (1 + interest)
        return self.benefit * sum(
            v ** (k + 1) * self.mortality_model.prob_Kx_equals_k(k, x)
            for k in range(max_age)
        )
