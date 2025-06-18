
from mfi_alm.assets.asset import Asset

"""
TODO:

Create a class called FixedBond (e.g., leverage asset_type_pricing.ipynb logic). It should inherit attributes
from the general Asset class.
"""

import pandas as pd

import numpy as np

from typing import List, Tuple


class FixedBond:
    """ Vanilla non-callable fixed rate bonds """

    def __init__(self, face: float, coupon: float, maturity: float, freq: int = 2):
        """
        parameters:
            face: Face value
            coupon: Annual coupon rate
            maturity: Maturity
            freq: Coupon payment frequency
        """
        self.face = face
        self.coupon = coupon
        self.maturity = maturity
        self.freq = freq

    def cashflows(self) -> List[Tuple[float, float]]:
        """Generate all future cash flows from bonds (time, amount)"""
        # Calculate the amount of each interest payment
        c = self.coupon * self.face / self.freq
        # Calculate total number of interest payments
        n = int(self.maturity * self.freq)
        # Generate cash flow (excluding principal) for each period
        flows = [(i / self.freq, c) for i in range(1, n + 1)]
        # Final installment plus principal
        flows[-1] = (flows[-1][0], flows[-1][1] + self.face)
        return flows

    def price(self, ytm: float) -> float:
        """Calculate bond price by continuously compounding"""
        return sum(cf * self._disc(ytm, t) for t, cf in self.cashflows())

    @staticmethod
    def _disc(rate: float, t: float) -> float:
        """Continuously compounding discount factor"""
        return np.exp(-rate * t)
