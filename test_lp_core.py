import pytest

from lp_core import solve_lp, maximize_profits, minimize_costs


def test_maximize_profits_three_products():
    # max 3x1 + 5x2 + 4x3 s.t. 2x1+3x2+2x3 <= 100, x1+2x2+x3 <= 60
    res = solve_lp([3, 5, 4], sense="max", A_ub=[[2, 3, 2], [1, 2, 1]], b_ub=[100, 60])
    assert res["success"]
    assert res["variables"][0] == pytest.approx(0, abs=1e-7)
    assert res["variables"][1] == pytest.approx(0, abs=1e-7)
    assert res["variables"][2] == pytest.approx(50, abs=1e-5)
    assert res["optimal_value"] == pytest.approx(200, abs=1e-5)


def test_infeasible_reports_status():
    res = solve_lp([1, 1], sense="min", A_ub=[[-1, -1], [1, 1]], b_ub=[-10, 5])
    assert not res["success"]
    assert res["status"] == 2
    assert res["optimal_value"] is None


def test_helpers():
    res = maximize_profits(
        prices=[50, 70, 60],
        costs=[30, 45, 36],
        resources=[{"usage": [2, 3, 2], "available": 100}, {"usage": [1, 2, 1], "available": 60}],
    )
    assert res["success"]
    assert res["optimal_value"] == pytest.approx(1200, abs=1e-5)

    res2 = minimize_costs([4, 5], [{"coeffs": [-2, -1], "rhs": -4}, {"coeffs": [-1, -2], "rhs": -4}])
    assert res2["success"]
    assert res2["optimal_value"] == pytest.approx(12, abs=1e-5)
