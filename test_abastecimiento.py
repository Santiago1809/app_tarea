import pytest

from abastecimiento import eoq, safety_stock


def test_eoq_classic():
    res = eoq([{"name": "X", "demand_per_year": 1000, "order_cost": 10, "holding_cost": 0.5}])
    assert res["products"][0]["q_star"] == pytest.approx(200, abs=1e-6)
    assert res["products"][0]["annual_cost"] == pytest.approx(100, abs=1e-6)
    assert res["total_annual_cost"] == pytest.approx(100, abs=1e-6)


def test_safety_stock_known_z():
    # z=1 (service_factor), sigma=5, lead_time=4 => SS = 1*5*2 = 10; ROP = 20*4 + 10 = 90
    res = safety_stock(
        [{"name": "Y", "demand_std": 5, "lead_time": 4, "avg_daily_demand": 20}],
        service_factor=1.0,
    )
    assert res[0]["safety_stock"] == pytest.approx(10, abs=1e-6)
    assert res[0]["reorder_point"] == pytest.approx(90, abs=1e-6)
