import pytest

from transporte import solved_transport


def test_balanced_known_optimum():
    supply = [20, 30]
    demand = [15, 35]
    cost_matrix = [[4, 8], [6, 2]]
    res = solved_transport(supply, demand, cost_matrix)
    # plant1->dest1 15, plant1->dest2 5, plant2->dest2 30 => 15*4 + 5*8 + 30*2 = 160
    assert res["success"]
    assert res["optimal_cost"] == pytest.approx(160)
    assert res["shipments"][0][0] == pytest.approx(15)
    assert res["shipments"][0][1] == pytest.approx(5)
    assert res["shipments"][1][0] == pytest.approx(0, abs=1e-7)
    assert res["shipments"][1][1] == pytest.approx(30)


def test_unbalanced_raises():
    with pytest.raises(AssertionError, match="total supply=50 != total demand=40"):
        solved_transport([20, 30], [40], [[1], [2]])
