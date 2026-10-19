"""Forecasting models for time-series production data.

Four methods: simple moving average, weighted moving average,
simple exponential smoothing, and linear regression.
"""

import math

import numpy as np


def moving_average(values: list, n: int = 3) -> dict:
    """Simple moving average of the last *n* periods.

    Returns a dict with:
      - forecast: list of length len(values)+1 (None for the first n-1
        entries, then each MA value, last entry is the next-period forecast).
      - next_value: the forecast for the next period.
    """
    forecast: list = [None] * len(values) + [None]
    for i in range(n, len(values) + 1):
        forecast[i] = sum(values[i - n : i]) / n
    return {"forecast": forecast, "next_value": forecast[-1]}


def weighted_moving_average(values: list, weights: list) -> dict:
    """Weighted moving average.

    *weights* must sum to 1.0.  ``weights[0]`` applies to the MOST RECENT
    period and ``weights[-1]`` to the OLDEST period in the window.

    Returns dict with *forecast* (list, len = len(values)+1) and *next_value*.
    """
    n = len(weights)
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1.0")

    forecast: list = [None] * len(values) + [None]
    for i in range(n, len(values) + 1):
        window = values[i - n : i]
        # weights[0] -> most recent, weights[-1] -> oldest
        wma = sum(w * v for w, v in zip(reversed(weights), window))
        forecast[i] = wma
    return {"forecast": forecast, "next_value": forecast[-1]}


def exponential_smoothing(values: list, alpha: float = 0.3) -> dict:
    """Simple exponential smoothing.

    F(1) = values[0], F(t+1) = alpha * values[t] + (1 - alpha) * F(t).

    Returns dict with *forecast* (list, len = len(values)+1) and *next_value*.
    """
    forecast = [values[0]]  # F(1)
    for t in range(len(values)):
        f_next = alpha * values[t] + (1 - alpha) * forecast[t]
        forecast.append(f_next)
    return {"forecast": forecast, "next_value": forecast[-1]}


def linear_regression(values: list) -> dict:
    """Ordinary least-squares linear regression y = a + b*x.

    x = [1, 2, ..., n], y = values.

    Returns dict with *forecast* (list, len = len(values)+1), *next_value*,
    *slope*, *intercept*, and *r_squared*.
    """
    n = len(values)
    x = np.arange(1, n + 1, dtype=float)
    y = np.array(values, dtype=float)

    x_mean = x.mean()
    y_mean = y.mean()

    ss_xy = np.sum((x - x_mean) * (y - y_mean))
    ss_xx = np.sum((x - x_mean) ** 2)

    slope = ss_xy / ss_xx
    intercept = y_mean - slope * x_mean

    fitted = intercept + slope * x
    forecast = list(fitted) + [intercept + slope * (n + 1)]

    ss_res = np.sum((y - fitted) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0

    return {
        "forecast": forecast,
        "next_value": forecast[-1],
        "slope": float(slope),
        "intercept": float(intercept),
        "r_squared": float(r_squared),
    }


def forecast_errors(actual: list, predicted: list) -> dict:
    """Calculate MAD, MSE, and MAPE over overlapping non-None entries.

    Returns dict with *mad*, *mse*, *mape* (percentage).
    """
    pairs = [
        (a, p)
        for a, p in zip(actual, predicted)
        if a is not None and p is not None
    ]
    if not pairs:
        return {"mad": None, "mse": None, "mape": None}

    errors = [abs(a - p) for a, p in pairs]
    mad = sum(errors) / len(errors)
    mse = sum(e ** 2 for e in errors) / len(errors)
    mape = (
        sum(abs((a - p) / a) for a, p in pairs if a != 0) / len(pairs) * 100
    )
    return {"mad": mad, "mse": mse, "mape": mape}
