import pandas as pd
import streamlit as st

from abastecimiento import eoq, safety_stock
from lp_core import maximize_profits, minimize_costs
from transporte import solved_transport

st.set_page_config(page_title="Investigación de Operaciones", layout="wide")
st.title("Herramientas de Investigación de Operaciones")

section = st.sidebar.radio(
    "Sección",
    [
        "Maximizar ganancias",
        "Minimizar costos",
        "Logística de transporte",
        "Abastecimiento (Q* y stock de seguridad)",
    ],
)

PRODUCT_NAMES = ["Galletitas", "Chocolates", "Golosinas"]
RESOURCE_NAMES = ["Horas de línea", "Materia prima (t azúcar/derivados)"]

DISCLAIMER = (
    "Datos unitarios estimados a partir de fuentes públicas de Arcor; "
    "no son cifras oficiales por producto."
)

if section in ("Maximizar ganancias", "Minimizar costos"):
    st.header(section)
    if section == "Maximizar ganancias":
        st.caption(
            "Ancla real: los tres segmentos principales de Arcor; precios y costos en "
            "ARS miles por tonelada, calibrados para un margen operativo aprox. del 6 % "
            "(resultado operativo 2025 de $293.291 millones sobre $4.902.647 millones). "
            + DISCLAIMER
        )
        defaults = {"Precio": [2500.0, 4200.0, 3000.0], "Costo": [2350.0, 3950.0, 2820.0]}
        df = pd.DataFrame(defaults, index=PRODUCT_NAMES)
        edited = st.data_editor(df, use_container_width=True)
        res_df = pd.DataFrame(
            {"Uso por unidad": [[2.0, 3.0, 2.0], [0.40, 0.55, 0.60]], "Disponible": [100.0, 60.0]},
            index=RESOURCE_NAMES,
        )
        st.subheader("Restricciones de recursos")
        edited_res = st.data_editor(res_df, use_container_width=True)
        if st.button("Resolver"):
            result = maximize_profits(
                prices=list(edited["Precio"]),
                costs=list(edited["Costo"]),
                resources=[
                    {"usage": list(row["Uso por unidad"]), "available": row["Disponible"]}
                    for _, row in edited_res.iterrows()
                ],
            )
            if result["success"]:
                st.success(f"Ganancia óptima: {result['optimal_value']:.2f}")
                st.table(pd.DataFrame(
                    {"Cantidad a producir": result["variables"]}, index=PRODUCT_NAMES
                ))
            else:
                st.error(f"Sin solución: {result['message']}")
    else:
        st.caption(
            "Ancla real: mix de insumos (ej. azúcar de Agronegocios vs. mercado externo); "
            "costos en ARS miles por tonelada. Los montos son aproximados. " + DISCLAIMER
        )
        df = pd.DataFrame(
            {"Costo unitario": [40.0, 55.0]},
            index=["Insumo interno (Agronegocios)", "Insumo de mercado"],
        )
        edited = st.data_editor(df, use_container_width=True)
        cons_df = pd.DataFrame(
            {"Coeficientes": [[2.0, 1.0], [1.0, 2.0]], "Requerimiento mínimo": [4.0, 4.0]},
            index=["Restricción 1", "Restricción 2"],
        )
        st.subheader("Restricciones (se convierten en >=)")
        edited_cons = st.data_editor(cons_df, use_container_width=True)
        if st.button("Resolver"):
            result = minimize_costs(
                list(edited["Costo unitario"]),
                [
                    {"coeffs": [-x for x in row["Coeficientes"]], "rhs": -row["Requerimiento mínimo"]}
                    for _, row in edited_cons.iterrows()
                ],
            )
            if result["success"]:
                st.success(f"Costo óptimo: {result['optimal_value']:.2f}")
                st.table(pd.DataFrame(
                    {"Cantidad": result["variables"]}, index=list(edited.index)
                ))
            else:
                st.error(f"Sin solución: {result['message']}")

elif section == "Logística de transporte":
    st.header(section)
    plants = ["Arcor Arroyito (Córdoba)", "Arcor Recreo (Tucumán)", "Arcor Mar del Plata"]
    dests = ["CABA", "Rosario", "Mendoza", "Montevideo"]
    st.subheader("Matriz de costos")
    st.caption(
        "Ancla real: plantas públicas de Arcor y principales centros de distribución; "
        "costos en ARS miles por tonelada, aproximados por distancia. " + DISCLAIMER
    )
    cost_df = pd.DataFrame(
        [[14.0, 6.0, 10.0, 17.0], [20.0, 15.0, 12.0, 24.0], [7.0, 9.0, 20.0, 10.0]],
        index=plants, columns=dests,
    )
    edited_costs = st.data_editor(cost_df, use_container_width=True)
    st.subheader("Oferta y demanda")
    supply_df = pd.DataFrame({"Oferta (miles de t/año)": [35.0, 50.0, 40.0]}, index=plants)
    demand_df = pd.DataFrame({"Demanda (miles de t/año)": [45.0, 20.0, 30.0, 30.0]}, index=dests)
    c1, c2 = st.columns(2)
    edited_supply = c1.data_editor(supply_df, use_container_width=True)
    edited_demand = c2.data_editor(demand_df, use_container_width=True)
    if st.button("Resolver"):
        try:
            result = solved_transport(
                list(edited_supply["Oferta (miles de t/año)"]),
                list(edited_demand["Demanda (miles de t/año)"]),
                edited_costs.values.tolist(),
            )
        except AssertionError as e:
            st.error(str(e))
        else:
            if result["success"]:
                st.success(f"Costo óptimo de transporte: {result['optimal_cost']:.2f}")
                st.table(pd.DataFrame(result["shipments"], index=plants, columns=dests))
            else:
                st.error(f"Sin solución: {result['message']}")

else:
    st.header(section)
    st.subheader("Datos de productos")
    st.caption(
        "Ancla real: escala derivada de los ingresos 2025 de Arcor "
        "($4.902.647 millones); demandas en toneladas/año, costos en ARS miles. "
        + DISCLAIMER
    )
    inv_df = pd.DataFrame(
        {
            "Demanda anual (t)": [12000.0, 8000.0, 6000.0],
            "Costo de pedido (miles ARS)": [150.0, 180.0, 160.0],
            "Costo de mantenimiento (miles ARS/t·año)": [40.0, 70.0, 50.0],
            "Desvío estándar diario (t)": [6.0, 4.0, 3.0],
            "Demanda diaria promedio (t)": [33.0, 22.0, 17.0],
            "Tiempo de entrega (días)": [4.0, 6.0, 5.0],
        },
        index=PRODUCT_NAMES,
    )
    edited = st.data_editor(inv_df, use_container_width=True)
    service_factor = st.number_input("Factor de servicio (z)", min_value=0.0, value=1.65, step=0.05)
    if st.button("Calcular"):
        products = [
            {
                "name": name,
                "demand_per_year": row["Demanda anual (t)"],
                "order_cost": row["Costo de pedido (miles ARS)"],
                "holding_cost": row["Costo de mantenimiento (miles ARS/t·año)"],
                "demand_std": row["Desvío estándar diario (t)"],
                "avg_daily_demand": row["Demanda diaria promedio (t)"],
                "lead_time": row["Tiempo de entrega (días)"],
            }
            for name, row in edited.iterrows()
        ]
        eoq_res = eoq(products)
        ss_res = safety_stock(products, service_factor)
        table = pd.DataFrame(
            {
                "Cantidad óptima de pedido (Q*)": [p["q_star"] for p in eoq_res["products"]],
                "Costo anual": [p["annual_cost"] for p in eoq_res["products"]],
                "Stock de seguridad": [p["safety_stock"] for p in ss_res],
                "Punto de reorden": [p["reorder_point"] for p in ss_res],
            },
            index=PRODUCT_NAMES,
        )
        st.table(table)
        st.success(f"Costo anual total: {eoq_res['total_annual_cost']:.2f}")
