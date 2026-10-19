"""Tests for pronosticos.py — hand-computed known values."""

import math

import pytest

from pronosticos import (
    exponential_smoothing,
    forecast_errors,
    linear_regression,
    moving_average,
    weighted_moving_average,
)


class TestMovingAverage:
    def test_basic(self):
        result = moving_average([10, 20, 30, 40, 50], n=3)
        # MA(4) = (10+20+30)/3 = 20, MA(5) = (20+30+40)/3 = 30
        # MA(6/next) = (30+40+50)/3 = 40
        assert result["next_value"] == pytest.approx(40.0)
        assert result["forecast"][0] is None
        assert result["forecast"][1] is None
        assert result["forecast"][2] is None
        assert result["forecast"][3] == pytest.approx(20.0)
        assert result["forecast"][4] == pytest.approx(30.0)
        assert result["forecast"][5] == pytest.approx(40.0)

    def test_n_equals_length(self):
        result = moving_average([10, 20, 30], n=3)
        assert result["next_value"] == pytest.approx(20.0)
        assert len(result["forecast"]) == 4

    def test_forecast_length(self):
        vals = [1, 2, 3, 4, 5, 6]
        result = moving_average(vals, n=2)
        assert len(result["forecast"]) == len(vals) + 1


class TestWeightedMovingAverage:
    def test_basic(self):
        # weights[0]=0.5 (most recent), [1]=0.3, [2]=0.2 (oldest)
        result = weighted_moving_average(
            [10, 20, 30, 40, 50], weights=[0.5, 0.3, 0.2]
        )
        # WMA(6/next): 50*0.5 + 40*0.3 + 30*0.2 = 25+12+6 = 43
        assert result["next_value"] == pytest.approx(43.0)

    def test_weights_must_sum_to_one(self):
        with pytest.raises(ValueError, match="sum to 1"):
            weighted_moving_average([10, 20, 30], weights=[0.5, 0.3])


class TestExponentialSmoothing:
    def test_basic(self):
        result = exponential_smoothing([100, 200, 300], alpha=0.5)
        # F(1) = 100
        # F(2) = 0.5*100 + 0.5*100 = 100
        # F(3) = 0.5*200 + 0.5*100 = 150
        # F(4) = 0.5*300 + 0.5*150 = 225
        assert result["forecast"][0] == pytest.approx(100.0)
        assert result["forecast"][1] == pytest.approx(100.0)
        assert result["forecast"][2] == pytest.approx(150.0)
        assert result["next_value"] == pytest.approx(225.0)
        assert len(result["forecast"]) == 4

    def test_alpha_one(self):
        result = exponential_smoothing([10, 20, 30], alpha=1.0)
        # F(1)=10, F(2)=1*10+0*10=10, F(3)=1*20+0*10=20, F(4)=1*30+0*20=30
        assert result["next_value"] == pytest.approx(30.0)

    def test_alpha_zero(self):
        result = exponential_smoothing([10, 20, 30], alpha=0.0)
        # Everything stays at initial value
        assert result["next_value"] == pytest.approx(10.0)


class TestLinearRegression:
    def test_perfect_line(self):
        # y = 10*x + 0 => [10, 20, 30, 40, 50]
        result = linear_regression([10, 20, 30, 40, 50])
        assert result["slope"] == pytest.approx(10.0)
        assert result["intercept"] == pytest.approx(0.0)
        assert result["r_squared"] == pytest.approx(1.0)
        assert result["next_value"] == pytest.approx(60.0)

    def test_forecast_length(self):
        result = linear_regression([5, 10, 15])
        assert len(result["forecast"]) == 4

    def test_constant(self):
        result = linear_regression([7, 7, 7, 7])
        assert result["slope"] == pytest.approx(0.0)
        assert result["r_squared"] == pytest.approx(1.0)
        assert result["next_value"] == pytest.approx(7.0)


class TestForecastErrors:
    def test_basic(self):
        actual = [10, 20, 30]
        predicted = [12, 18, 33]
        result = forecast_errors(actual, predicted)
        # errors: |10-12|=2, |20-18|=2, |30-33|=3
        assert result["mad"] == pytest.approx(7 / 3)
        # MSE: (4+4+9)/3 = 17/3
        assert result["mse"] == pytest.approx(17 / 3)
        # MAPE: (2/10 + 2/20 + 3/30)/3 * 100 = (0.2+0.1+0.1)/3*100 = 13.33..
        assert result["mape"] == pytest.approx(100 * (0.2 + 0.1 + 0.1) / 3)

    def test_skips_none(self):
        actual = [None, 20, 30]
        predicted = [10, None, 33]
        result = forecast_errors(actual, predicted)
        # Only index 2 has both: |30-33|=3
        assert result["mad"] == pytest.approx(3.0)

    def test_empty(self):
        result = forecast_errors([], [])
        assert result["mad"] is None
