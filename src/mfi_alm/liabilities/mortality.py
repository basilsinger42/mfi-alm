from typing import Self

import pandas as pd
import numpy as np


class MortalityModel:
    def __init__(self, df_mortality: pd.DataFrame):
        if not {"x", "lx"}.issubset(df_mortality.columns):
            raise ValueError("Mortality table must contain 'x' and 'lx' columns.")

        self.df = df_mortality.set_index("x").copy()
        self.min_age = self.df.index.min()
        self.max_age = self.df.index.max()

    def tpx(self, t: int, x: int) -> float:
        if x < self.min_age:
            return 1.0
        if x + t > self.max_age:
            return 0.0
        return self.df.loc[x + t, "lx"] / self.df.loc[x, "lx"]

    def tqx(self, t: int, x: int) -> float:
        return 1 - self.tpx(t, x)

    def prob_Kx_equals_k(self, k: int, x: int) -> float:
        return self.tpx(k, x) * self.tqx(1, x + k)

    def discrete_remaining_mortality_probs(self, x: int, t_horizon: int = 120) -> np.ndarray:
        return np.array([self.prob_Kx_equals_k(k, x) for k in range(t_horizon + 1)])

    def simulate_remaining_death_year(self, x: int, seed: int = 42, t_horizon: int = 120) -> int:
        if x >= self.max_age:
            return 0

        probs = self.discrete_remaining_mortality_probs(x, t_horizon)
        probs /= probs.sum()
        rng = np.random.default_rng(seed)

        return rng.choice(len(probs), p=probs)

    def copy(self) -> Self:
        df_mortality = self.df.reset_index()[["x", "lx"]].copy()
        return MortalityModel(df_mortality=df_mortality)
