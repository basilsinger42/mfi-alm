from typing import Self
import numpy as np


class FixedBond:
    """Vanilla non-callable fixed rate bonds."""

    def __init__(self, face: float, coupon: float, maturity: float, freq: int = 2):
        self.face = face
        self.coupon = coupon
        self.maturity = maturity
        self.freq = freq

    def cashflows(self) -> list[tuple[float, float]]:
        """Generate all future cash flows from bonds (time, amount)."""
        c = self.coupon * self.face / self.freq
        n = int(self.maturity * self.freq)

        # Generate cash flow (excluding principal) for each period.
        flows = [(i / self.freq, c) for i in range(1, n + 1)]

        # Final installment plus principal.
        flows[-1] = (flows[-1][0], flows[-1][1] + self.face)

        return flows

    def price(self, ytm: float) -> float:
        """Calculate bond price by continuously compounding."""
        return sum(cf * self._disc(ytm, t) for t, cf in self.cashflows())

    @staticmethod
    def _disc(rate: float, t: float) -> float:
        """Continuously compounding discount factor."""
        return np.exp(-rate * t)

    def project_prices(self, ytm: float, years: int) -> np.ndarray:
        flows = self.cashflows()
        prices = np.zeros(years)
        times = np.array([t for t, _ in flows])
        cfs = np.array([cf for _, cf in flows])

        for t in range(years):
            mask = times >= t
            t_adjusted = times[mask] - t
            discounted = cfs[mask] * np.exp(-ytm * t_adjusted)
            prices[t] = np.sum(discounted)

        return prices

    def copy(self) -> Self:
        return FixedBond(face=self.face, coupon=self.coupon, maturity=self.maturity, freq=self.freq)
