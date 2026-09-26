from scipy.optimize import linprog


def solve_lp(objective_coeffs, sense="max", A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None):
    c = objective_coeffs if sense == "min" else [-x for x in objective_coeffs]
    if bounds is None:
        bounds = [(0, None)] * len(c)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    return {
        "success": bool(res.success),
        "status": res.status,
        "message": res.message,
        "optimal_value": (res.fun if sense == "min" else -res.fun) if res.success else None,
        "variables": list(res.x) if res.success else None,
    }


def maximize_profits(prices, costs, resources):
    margins = [p - c for p, c in zip(prices, costs)]
    A_ub = [r["usage"] for r in resources]
    b_ub = [r["available"] for r in resources]
    return solve_lp(margins, sense="max", A_ub=A_ub, b_ub=b_ub)


def minimize_costs(costs, constraints):
    A_ub = [c["coeffs"] for c in constraints]
    b_ub = [c["rhs"] for c in constraints]
    return solve_lp(costs, sense="min", A_ub=A_ub, b_ub=b_ub)
