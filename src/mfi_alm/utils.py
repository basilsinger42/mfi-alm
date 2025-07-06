import numpy as np


def get_time(t: float, dp: int | None = 1) -> tuple[float, str]:
    if t < 60:
        return np.around(t, dp), "seconds"
    if t < 60 * 60:
        return np.around(t / 60, dp), "minutes"
    if t < 60 * 60 * 24:
        return np.around(t / (60 * 60), dp), "hours"

    return np.around(t / (60 * 60 * 24), dp), "days"
