import pandas as pd
import streamlit as st

from abastecimiento import eoq, safety_stock
from lp_core import maximize_profits, minimize_costs
from transporte import solved_transport

st.set_page_config(page_title="Arcor Ops Planner", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
    <style>
      :root {
        --bg: #050505;
        --card: #0d0d0f;
        --card-2: #121215;
        --hairline: rgba(255, 255, 255, 0.08);
        --accent: #e7402b;            /* rojo Arcor */
        --accent-soft: rgba(231, 64, 43, 0.16);
        --text: #f5f5f4;
        --muted: #9ca3af;
        --ease-premium: cubic-bezier(0.32, 0.72, 0, 1);
      }
      html, body, [class*="stApp"] {
        background:
          radial-gradient(60rem 60rem at 85% -10%, rgba(231, 64, 43, 0.10), transparent 60%),
          radial-gradient(50rem 50rem at -10% 110%, rgba(99, 102, 241, 0.08), transparent 60%),
          var(--bg);
        color: var(--text);
        font-family: 'Plus Jakarta Sans', sans-serif;
      }
      #MainMenu, footer, header { visibility: hidden; }
      /* ---------- Hero ---------- */
      .eyebrow {
        display: inline-block;
        border: 1px solid var(--hairline);
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 10px;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 1.2rem;
        backdrop-filter: blur(12px);
      }
      .hero h1 {
        font-size: clamp(2.4rem, 5vw, 4rem);
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.05;
        margin: 0;
        background: linear-gradient(120deg, #ffffff 30%, #a3a3a3 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
      }
      .hero p {
        color: var(--muted);
        font-size: 1.05rem;
        font-weight: 300;
        max-width: 44rem;
        margin-top: 0.9rem;
      }
      /* ---------- Sidebar ---------- */
      section[data-testid="stSidebar"] {
        background: rgba(10, 10, 12, 0.82);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--hairline);
      }
      section[data-testid="stSidebar"] * { font-family: 'Plus Jakarta Sans', sans-serif; }
      /* ---------- Cards / editors / tables ---------- */
      div[data-testid="stDataFrame"], div[data-testid="stDataEditor"],
      div[data-testid="stMetric"], div[data-testid="stAlert"] {
        background: var(--card);
        border: 1px solid var(--hairline);
        border-radius: 1.25rem;
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        transition: transform 0.5s var(--ease-premium), border-color 0.5s var(--ease-premium);
      }
      div[data-testid="stDataFrame"]:hover, div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.16);
      }
      div[data-testid="stMetric"] { padding: 1.2rem 1.4rem; }
      div[data-testid="stMetric"] label { color: var(--muted); font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; }
      div[data-testid="stMetric"] [data-testid="stMetricValue"] { font-weight: 800; letter-spacing: -0.03em; font-size: 2rem; color: var(--accent); }
      /* ---------- Typography ---------- */
      h2, h3 { font-weight: 700; letter-spacing: -0.02em; }
      [data-testid="stCaptionContainer"] { color: var(--muted); font-weight: 300; }
      /* ---------- Buttons ---------- */
      button[kind="primary"], button[kind="secondary"], .stButton button {
        border-radius: 999px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        transition: all 0.4s var(--ease-premium) !important;
      }
      .stButton button:hover { transform: translateY(-1px) scale(1.02); }
      .stButton button:active { transform: scale(0.97); }
      .stButton button[kind="primary"] {
        background: var(--accent) !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(231, 64, 43, 0.35);
      }
      /* ---------- Entry animation ---------- */
      @keyframes rise {
        from { opacity: 0; transform: translateY(1.5rem); filter: blur(6px); }
        to   { opacity: 1; transform: translateY(0); filter: blur(0); }
      }
      .main .block-container > * { animation: rise 0.8s var(--ease-premium) both; }
      .main .block-container > *:nth-child(2) { animation-delay: 0.08s; }
      .main .block-container > *:nth-child(3) { animation-delay: 0.16s; }
      /* ---------- Scrollbar ---------- */
      ::-webkit-scrollbar { width: 8px; height: 8px; }
      ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 99px; }
      ::-webkit-scrollbar-track { background: transparent; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <span class="eyebrow">Investigación de Operaciones · Arcor</span>
      <h1>Optimizador de operaciones</h1>
      <p>Programación lineal, transporte y abastecimiento sobre los tres segmentos
         principales: galletitas, chocolates y golosinas.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

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
        edited = st.data_editor(df, width="stretch")
        res_df = pd.DataFrame(
            {"Uso por unidad": [[2.0, 3.0, 2.0], [0.40, 0.55, 0.60]], "Disponible": [100.0, 60.0]},
            index=RESOURCE_NAMES,
        )
        st.subheader("Restricciones de recursos")
        edited_res = st.data_editor(res_df, width="stretch")
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
                st.metric("Ganancia óptima (miles ARS)", f"{result['optimal_value']:,.0f}")
                st.table(pd.DataFrame(
                    {"Cantidad a producir (t)": result["variables"]}, index=PRODUCT_NAMES
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
        edited = st.data_editor(df, width="stretch")
        cons_df = pd.DataFrame(
            {"Coeficientes": [[2.0, 1.0], [1.0, 2.0]], "Requerimiento mínimo": [4.0, 4.0]},
            index=["Restricción 1", "Restricción 2"],
        )
        st.subheader("Restricciones (se convierten en >=)")
        edited_cons = st.data_editor(cons_df, width="stretch")
        if st.button("Resolver"):
            result = minimize_costs(
                list(edited["Costo unitario"]),
                [
                    {"coeffs": [-x for x in row["Coeficientes"]], "rhs": -row["Requerimiento mínimo"]}
                    for _, row in edited_cons.iterrows()
                ],
            )
            if result["success"]:
                st.metric("Costo óptimo (miles ARS)", f"{result['optimal_value']:,.0f}")
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
    edited_costs = st.data_editor(cost_df, width="stretch")
    st.subheader("Oferta y demanda")
    supply_df = pd.DataFrame({"Oferta (miles de t/año)": [35.0, 50.0, 40.0]}, index=plants)
    demand_df = pd.DataFrame({"Demanda (miles de t/año)": [45.0, 20.0, 30.0, 30.0]}, index=dests)
    c1, c2 = st.columns(2)
    edited_supply = c1.data_editor(supply_df, width="stretch")
    edited_demand = c2.data_editor(demand_df, width="stretch")
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
                st.metric("Costo óptimo de transporte (miles ARS)", f"{result['optimal_cost']:,.0f}")
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
    edited = st.data_editor(inv_df, width="stretch")
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
        st.metric("Costo anual total de inventario (miles ARS)", f"{eoq_res['total_annual_cost']:,.0f}")
