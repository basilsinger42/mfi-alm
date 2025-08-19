from typing import Optional
import numpy as np
import pandas as pd


class MortalityModel:
    """
    Vectorized mortality model based on an lx life table.
    Implementation avoids Python for-loops and DataFrame copies.
    """
    def __init__(self, df_mortality: pd.DataFrame, years_max: Optional[int] = None):
        if not {"x", "lx"}.issubset(df_mortality.columns):
            raise ValueError("Mortality table must contain 'x' and 'lx' columns.")

        # Use the provided table directly: set index to 'x' (ages) and ensure ascending order
        self.df = df_mortality.set_index("x").sort_index()
        ages = self.df.index.to_numpy()
        if (np.diff(ages) != 1).any():
            raise ValueError("Ages must be contiguous integers for fast lookup.")

        self.min_age = int(ages.min())
        self.max_age = int(ages.max())
        self.ages = ages
        self.lx = self.df["lx"].to_numpy(dtype=float)
        n = self.lx.size

        # One-year death probability qx (force last age to 1.0 = certain death)
        qx = np.empty_like(self.lx)
        qx[:-1] = 1.0 - (self.lx[1:] / self.lx[:-1])
        qx[-1] = 1.0
        self.qx = qx

        # Grid width (defaults to full table length)
        if years_max is None:
            years_max = n
        self.years_max = int(years_max)

        # Build tqx(1, x+t) lookup grid:
        # tqx_grid[i, t] = qx[i+t], with padding 1.0 beyond table
        # Shape: [n_ages, years_max]
        i = np.arange(n)[:, None]
        t = np.arange(self.years_max)[None, :]
        idx = i + t
        self.tqx_grid = np.where(idx < n, qx.take(idx, mode="clip"), 1.0)

    # -------- Scalar API --------
    def tpx(self, t: int, x: int) -> float:
        """t-year survival probability from age x."""
        if t <= 0:
            return 1.0
        x0 = max(x, self.min_age)
        if x0 > self.max_age:
            return 0.0
        end = x0 + t
        if end > self.max_age:
            return 0.0
        i = x0 - self.min_age
        j = end - self.min_age
        return float(self.lx[j] / self.lx[i])

    def tqx(self, t: int, x: int) -> float:
        """t-year death probability from age x."""
        return 1.0 - self.tpx(t, x)

    # -------- Fast vectorized API --------
    def tqx_1yr_lookup(self, x: int, t: int) -> float:
        """
        One-year death probability at attained age (x+t).
        Equivalent to q_{x+t}.
        """
        age = x + t
        if age < self.min_age:
            return 0.0
        if age > self.max_age:
            return 1.0
        return float(self.qx[age - self.min_age])

    def tqx_vector(self, x: int, years: int) -> np.ndarray:
        """
        Return vector of tqx(1, x), tqx(1, x+1), ..., tqx(1, x+years-1).
        Uses the precomputed tqx_grid and pads as needed.
        """
        if years <= 0:
            return np.empty(0, dtype=float)

        row = x - self.min_age

        # (1) x below table start: prepend zeros, then use table from min_age, then pad with ones
        if row < 0:
            pad_before = min(-row, years)
            head = np.zeros(pad_before, dtype=float)
            remaining = years - pad_before
            if remaining <= 0:
                return head
            take = min(remaining, self.years_max)
            body = self.tqx_grid[0, :take]
            tail_len = remaining - take
            return np.concatenate([head, body, np.ones(tail_len, dtype=float)]) if tail_len > 0 else np.concatenate([head, body])

        # (2) x beyond table end: return all ones
        if row >= self.ages.size:
            return np.ones(years, dtype=float)

        # (3) Normal case: slice from grid, then pad with ones if needed
        take = min(years, self.years_max)
        out = self.tqx_grid[row, :take]
        return np.concatenate([out, np.ones(years - take, dtype=float)]) if years > take else out

    def prob_Kx_equals_k(self, k: int, x: int) -> float:
        """
        Probability that future lifetime K_x = k.
        Formula: P(K_x = k) = tpx(k, x) * tqx(1, x+k).
        """
        if k < 0:
            return 0.0
        sp = self.tpx(k, x)  # survival to age x+k
        if sp == 0.0:
            return 0.0
        return sp * self.tqx_1yr_lookup(x, k)

    def discrete_remaining_mortality_probs(self, x: int, t_horizon: int = 120) -> np.ndarray:
        """
        Distribution of remaining lifetime K_x.
        Returns probabilities for k = 0, 1, ..., t_horizon.
        """
        k = np.arange(t_horizon + 1)
        base_idx = np.clip(x - self.min_age, 0, self.lx.size - 1)
        j = (x - self.min_age) + k
        in_tab = (j >= 0) & (j < self.lx.size)
        S = np.zeros_like(k, dtype=float)
        S[in_tab] = self.lx[j[in_tab]] / self.lx[base_idx]

        # One-year death probabilities at attained ages
        q_last = np.where(
            j < 0, 0.0,
            np.where(j >= self.lx.size, 1.0, self.qx[j])
        )

        probs = S * q_last
        s = probs.sum()
        return probs / s if s > 0 else probs

    def simulate_remaining_death_year(self, x: int, seed: int = 42, t_horizon: int = 120) -> int:
        """
        Simulate the future lifetime (in years) for an individual aged x.
        Returns an integer k such that K_x = k.
        """
        probs = self.discrete_remaining_mortality_probs(x, t_horizon)
        rng = np.random.default_rng(seed)
        return int(rng.choice(probs.size, p=probs))

