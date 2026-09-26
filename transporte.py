from scipy.optimize import linprog


def solved_transport(supply, demand, cost_matrix):
    m, n = len(supply), len(demand)
    assert sum(supply) == sum(demand), (
        f"Balanced problem required: total supply={sum(supply)} != total demand={sum(demand)}"
    )
    total = m * n
    A_eq, b_eq = [], []
    for i in range(m):
        row = [0.0] * total
        for j in range(n):
            row[i * n + j] = 1.0
        A_eq.append(row)
        b_eq.append(supply[i])
    for j in range(n):
        row = [0.0] * total
        for i in range(m):
            row[i * n + j] = 1.0
        A_eq.append(row)
        b_eq.append(demand[j])
    c = [cost_matrix[i][j] for i in range(m) for j in range(n)]
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * total, method="highs")
    if not res.success:
        return {"success": False, "status": res.status, "message": res.message,
                "optimal_cost": None, "shipments": None}
    shipments = [list(res.x[i * n:(i + 1) * n]) for i in range(m)]
    return {"success": True, "status": res.status, "message": res.message,
            "optimal_cost": res.fun, "shipments": shipments}
