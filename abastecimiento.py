import math


def eoq(products):
    results = []
    total_annual_cost = 0.0
    for p in products:
        D = p["demand_per_year"]
        S = p["order_cost"]
        H = p["holding_cost"]
        q_star = math.sqrt(2 * D * S / H)
        annual_cost = (D / q_star) * S + (q_star / 2) * H
        total_annual_cost += annual_cost
        results.append({"name": p.get("name", "product"), "q_star": q_star, "annual_cost": annual_cost})
    return {"products": results, "total_annual_cost": total_annual_cost}


def safety_stock(products, service_factor):
    results = []
    for p in products:
        ss = service_factor * p["demand_std"] * math.sqrt(p["lead_time"])
        rop = p["avg_daily_demand"] * p["lead_time"] + ss
        results.append({"name": p.get("name", "product"), "safety_stock": ss, "reorder_point": rop})
    return results
