import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from abastecimiento import eoq, safety_stock
from datos_eva import DATA_SOURCE, PRODUCT_NAMES, get_product_data
from pronosticos import (
    exponential_smoothing,
    forecast_errors,
    linear_regression,
    moving_average,
    weighted_moving_average,
)

st.set_page_config(page_title="ERP Agrícola Colombia", layout="wide", initial_sidebar_state="auto")

# ---------------------------------------------------------------------------
# CSS — same design system, accent changed to emerald green
# ---------------------------------------------------------------------------
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
        --accent: #10b981;
        --accent-soft: rgba(16, 185, 129, 0.16);
        --text: #f5f5f4;
        --muted: #9ca3af;
        --ease-premium: cubic-bezier(0.32, 0.72, 0, 1);
      }
      html, body, [class*="stApp"] {
        background:
          radial-gradient(60rem 60rem at 85% -10%, rgba(16, 185, 129, 0.10), transparent 60%),
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
      .hero { padding: clamp(1.5rem, 4vw, 3rem) 0 1rem; }
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
        background: linear-gradient(180deg, var(--card-2), var(--card));
        border: none;
        border-radius: 1.75rem;
        box-shadow:
          0 0 0 1px rgba(255, 255, 255, 0.06),
          0 0 0 7px rgba(255, 255, 255, 0.025),
          inset 0 1px 1px rgba(255, 255, 255, 0.07);
        margin: 0.6rem;
        padding: 0.5rem;
        transition: transform 0.7s var(--ease-premium), box-shadow 0.7s var(--ease-premium);
      }
      div[data-testid="stDataFrame"]:hover, div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow:
          0 0 0 1px rgba(255, 255, 255, 0.14),
          0 0 0 7px rgba(255, 255, 255, 0.04),
          inset 0 1px 1px rgba(255, 255, 255, 0.12);
      }
      div[data-testid="stMetric"] { padding: 1.4rem 1.6rem; }
      div[data-testid="stMetric"] label { color: var(--muted); font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; }
      div[data-testid="stMetric"] [data-testid="stMetricValue"] { font-weight: 800; letter-spacing: -0.03em; font-size: 2rem; color: var(--accent); }
      /* ---------- Typography ---------- */
      h2, h3 { font-weight: 700; letter-spacing: -0.02em; }
      [data-testid="stCaptionContainer"] { color: var(--muted); font-weight: 300; }
      /* ---------- Buttons ---------- */
      button[kind="primary"], button[kind="secondary"], .stButton button {
        border-radius: 999px !important;
        padding: 0.65rem 1.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        transition: transform 0.6s var(--ease-premium), background-color 0.4s var(--ease-premium), box-shadow 0.6s var(--ease-premium) !important;
      }
      .stButton button:hover { transform: translateY(-1px) scale(1.02); }
      .stButton button:active { transform: scale(0.98); }
      .stButton button[kind="primary"] {
        background: var(--accent) !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35);
      }
      /* ---------- Entry animation ---------- */
      @keyframes rise {
        from { opacity: 0; transform: translateY(2rem); }
        to   { opacity: 1; transform: translateY(0); }
      }
      .main .block-container > * { animation: rise 0.8s var(--ease-premium) both; }
      .main .block-container > *:nth-child(2) { animation-delay: 0.08s; }
      .main .block-container > *:nth-child(3) { animation-delay: 0.16s; }
      /* ---------- Scrollbar ---------- */
      ::-webkit-scrollbar { width: 8px; height: 8px; }
      ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 99px; }
      ::-webkit-scrollbar-track { background: transparent; }
      /* ---------- Sidebar nav as pills ---------- */
      section[data-testid="stSidebar"] label[data-testid="stRadioOption"] {
        border: 1px solid transparent;
        border-radius: 999px;
        padding: 0.6rem 1rem;
        transition: background-color 0.5s var(--ease-premium), border-color 0.5s var(--ease-premium);
      }
      section[data-testid="stSidebar"] label[data-testid="stRadioOption"]:hover { background: rgba(255, 255, 255, 0.04); }
      section[data-testid="stSidebar"] label[data-testid="stRadioOption"][data-selected="true"] {
        background: var(--accent-soft);
        border-color: rgba(16, 185, 129, 0.35);
      }
      section[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div:first-child > div:first-child { display: none; }
      /* ---------- Grain (fixed, non-interactive) ---------- */
      .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 1;
        opacity: 0.035;
        background-image: url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
      }
      /* ---------- Data source banner ---------- */
      .source-banner {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.10), rgba(16, 185, 129, 0.04));
        border: 1px solid rgba(16, 185, 129, 0.22);
        border-radius: 1rem;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
      }
      .source-banner .source-icon {
        font-size: 1.6rem;
        flex-shrink: 0;
      }
      .source-banner .source-text {
        font-size: 0.85rem;
        color: var(--muted);
        line-height: 1.5;
      }
      .source-banner .source-text strong {
        color: var(--text);
        font-weight: 600;
      }
      .source-banner .source-text a {
        color: var(--accent);
        text-decoration: none;
      }
      .source-banner .source-text a:hover { text-decoration: underline; }
      /* ---------- Mobile (<768px): single column, 16px gutter ---------- */
      @media (max-width: 768px) {
        .main .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 2.5rem; }
        .hero h1 { font-size: 2.2rem; }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] { font-size: 1.6rem; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
      <span class="eyebrow">Investigación de Operaciones · DANE Colombia</span>
      <h1>ERP Agrícola Colombia</h1>
      <p>Análisis de demanda, pronósticos y gestión de inventario para tres
         productos agrícolas nacionales con datos del DANE (EVA 2007–2018).</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="source-banner">
      <span class="source-icon">📊</span>
      <div class="source-text">
        <strong>Fuente de datos:</strong> {DATA_SOURCE['entity']} —
        {DATA_SOURCE['dataset']}<br>
        Portal <a href="https://www.datos.gov.co" target="_blank">datos.gov.co</a>,
        recursos <code>{'</code>, <code>'.join(DATA_SOURCE['resource_ids'])}</code>
        · Período {DATA_SOURCE['date_range']}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
section = st.sidebar.radio(
    "Sección",
    ["Dashboard", "Demanda Histórica", "Proyección de Demanda", "Gestión de Inventario"],
)

# ---------------------------------------------------------------------------
# Plotly helpers
# ---------------------------------------------------------------------------
COLORS = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444"]
FUENTE = (
    f"Fuente: {DATA_SOURCE['entity']} — {DATA_SOURCE['dataset']}, "
    f"datos.gov.co, recursos {', '.join(DATA_SOURCE['resource_ids'])} ({DATA_SOURCE['date_range']})"
)


def _base_layout() -> dict:
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#f5f5f4"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        margin=dict(l=50, r=30, t=50, b=40),
    )


def _line_fig(x, y, name="", color=COLORS[0], title=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers", name=name,
        line=dict(color=color, width=2.5),
        marker=dict(size=6),
    ))
    fig.update_layout(**_base_layout(), title=title)
    return fig


# ---------------------------------------------------------------------------
# Section: Dashboard
# ---------------------------------------------------------------------------
if section == "Dashboard":
    st.header("Dashboard")
    cols = st.columns(3)
    for i, name in enumerate(PRODUCT_NAMES):
        data = get_product_data(name)
        latest_prod = data["production"][-1]
        delta = data["production"][-1] - data["production"][-2]
        with cols[i]:
            st.metric(
                label=f"{name} ({data['years'][-1]})",
                value=f"{latest_prod:,.0f} t",
                delta=f"{delta:+,.0f} t",
            )
    st.write("")
    cols2 = st.columns(3)
    for i, name in enumerate(PRODUCT_NAMES):
        data = get_product_data(name)
        fig = _line_fig(
            data["years"], data["production"],
            name=name, color=COLORS[i],
            title=f"{name} — Producción (t)",
        )
        fig.update_layout(height=280, showlegend=False)
        cols2[i].plotly_chart(fig, use_container_width=True)
    st.caption(FUENTE)

# ---------------------------------------------------------------------------
# Section: Demanda Histórica
# ---------------------------------------------------------------------------
elif section == "Demanda Histórica":
    st.header("Demanda Histórica")
    product = st.selectbox("Producto", PRODUCT_NAMES)
    data = get_product_data(product)

    # Production line chart
    fig_prod = _line_fig(
        data["years"], data["production"],
        name="Producción", color=COLORS[0],
        title=f"{product} — Producción anual (t)",
    )
    fig_prod.update_layout(height=400)
    st.plotly_chart(fig_prod, use_container_width=True)

    # Area sown vs harvested
    fig_area = go.Figure()
    fig_area.add_trace(go.Bar(
        x=data["years"], y=data["area_sown"], name="Área sembrada (ha)",
        marker_color=COLORS[1], opacity=0.7,
    ))
    fig_area.add_trace(go.Bar(
        x=data["years"], y=data["area_harvested"], name="Área cosechada (ha)",
        marker_color=COLORS[0], opacity=0.85,
    ))
    fig_area.update_layout(
        **_base_layout(), barmode="group", height=360,
        title=f"{product} — Área sembrada vs. cosechada (ha)",
        legend=dict(orientation="h", y=-0.15),
    )
    st.plotly_chart(fig_area, use_container_width=True)

    # Yield chart
    fig_yield = _line_fig(
        data["years"], [round(y, 2) for y in data["yield_per_ha"]],
        name="Rendimiento", color=COLORS[2],
        title=f"{product} — Rendimiento (t/ha)",
    )
    fig_yield.update_layout(height=320)
    st.plotly_chart(fig_yield, use_container_width=True)

    # Data table
    st.subheader("Datos tabulados")
    df = pd.DataFrame({
        "Año": data["years"],
        "Producción (t)": data["production"],
        "Área sembrada (ha)": data["area_sown"],
        "Área cosechada (ha)": data["area_harvested"],
        "Rendimiento (t/ha)": [round(y, 2) for y in data["yield_per_ha"]],
    })
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.caption(FUENTE)

# ---------------------------------------------------------------------------
# Section: Proyección de Demanda
# ---------------------------------------------------------------------------
elif section == "Proyección de Demanda":
    st.header("Proyección de Demanda")
    product = st.selectbox("Producto", PRODUCT_NAMES)
    data = get_product_data(product)
    values = data["production"]
    years = data["years"]
    next_year = years[-1] + 1

    # Parameters
    with st.expander("Parámetros de pronóstico", expanded=True):
        c1, c2, c3 = st.columns(3)
        ma_n = c1.slider("Períodos para Media Móvil (n)", 2, 6, 3)
        ses_alpha = c2.slider("Alpha (Suavización Exponencial)", 0.05, 0.95, 0.3, 0.05)
        wma_default_n = min(3, len(values))
        wma_n = c3.slider("Períodos para Media Móvil Ponderada", 2, 6, wma_default_n)

    # Generate default weights (linearly decreasing, most recent highest)
    raw_weights = list(range(wma_n, 0, -1))
    total_w = sum(raw_weights)
    wma_weights = [w / total_w for w in raw_weights]

    # Run models
    ma_result = moving_average(values, n=ma_n)
    wma_result = weighted_moving_average(values, weights=wma_weights)
    ses_result = exponential_smoothing(values, alpha=ses_alpha)
    lr_result = linear_regression(values)

    forecast_years = years + [next_year]

    # Metric cards for next-year forecast
    st.subheader(f"Pronóstico para {next_year}")
    mc = st.columns(4)
    models = [
        ("Media Móvil", ma_result),
        ("Media Móvil Pond.", wma_result),
        ("Suav. Exponencial", ses_result),
        ("Regresión Lineal", lr_result),
    ]
    for col, (name, res) in zip(mc, models):
        col.metric(name, f"{res['next_value']:,.0f} t")

    # Comparison chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values, mode="lines+markers", name="Datos reales",
        line=dict(color="#f5f5f4", width=2.5), marker=dict(size=7),
    ))
    model_series = [
        ("Media Móvil", ma_result["forecast"], COLORS[0]),
        ("Media Móvil Ponderada", wma_result["forecast"], COLORS[1]),
        ("Suavización Exp.", ses_result["forecast"], COLORS[2]),
        ("Regresión Lineal", lr_result["forecast"], COLORS[3]),
    ]
    for label, fc, color in model_series:
        fig.add_trace(go.Scatter(
            x=forecast_years, y=fc, mode="lines", name=label,
            line=dict(color=color, width=2, dash="dot"),
            connectgaps=False,
        ))
    fig.update_layout(
        **_base_layout(), height=480,
        title=f"{product} — Comparación de pronósticos",
        legend=dict(orientation="h", y=-0.18),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Error metrics
    st.subheader("Métricas de error")
    error_rows = []
    for label, res, _c in model_series:
        predicted = res[:len(values)]
        errs = forecast_errors(values, predicted)
        error_rows.append({
            "Modelo": label,
            "MAD": f"{errs['mad']:,.1f}" if errs["mad"] is not None else "—",
            "MSE": f"{errs['mse']:,.0f}" if errs["mse"] is not None else "—",
            "MAPE (%)": f"{errs['mape']:.2f}" if errs["mape"] is not None else "—",
        })
    st.dataframe(pd.DataFrame(error_rows), hide_index=True, use_container_width=True)

    # Model formulas
    with st.expander("Fórmulas de los modelos"):
        st.markdown(r"""
**Media Móvil Simple (SMA)**

$$F_{t+1} = \frac{1}{n}\sum_{i=t-n+1}^{t} y_i$$

**Media Móvil Ponderada (WMA)**

$$F_{t+1} = \sum_{i=1}^{n} w_i \cdot y_{t-i+1}, \quad \sum w_i = 1$$

**Suavización Exponencial Simple (SES)**

$$F_1 = y_1, \quad F_{t+1} = \alpha \cdot y_t + (1-\alpha) \cdot F_t$$

**Regresión Lineal**

$$\hat{y} = a + bx, \quad b = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}, \quad a = \bar{y} - b\bar{x}$$
        """)
    if "r_squared" in lr_result:
        st.caption(
            f"Regresión lineal — pendiente: {lr_result['slope']:,.2f} t/año, "
            f"intercepto: {lr_result['intercept']:,.0f}, R²: {lr_result['r_squared']:.4f}"
        )
    st.caption(FUENTE)

# ---------------------------------------------------------------------------
# Section: Gestión de Inventario
# ---------------------------------------------------------------------------
else:
    st.header("Gestión de Inventario")
    st.caption(
        "Modelo EOQ y stock de seguridad aplicados a los tres productos agrícolas. "
        "La demanda anual se toma de la producción del último año disponible."
    )

    # Default parameters
    DEFAULTS = {
        "Café":    {"S": 3_250_000_000, "H_pct": 0.22, "unit_value": 8_500_000, "lead_time": 14},
        "Arroz":   {"S": 1_150_000_000, "H_pct": 0.25, "unit_value": 2_200_000, "lead_time": 7},
        "Plátano": {"S": 225_000_000, "H_pct": 0.55, "unit_value": 1_600_000, "lead_time": 2},
    }

    with st.expander("Parámetros editables", expanded=True):
        service_factor = st.number_input(
            "Factor de servicio (z)", min_value=0.0, value=1.65, step=0.05,
            help="1.65 corresponde a un nivel de servicio del 95%",
        )
        param_cols = st.columns(3)
        edited_params = {}
        for col, name in zip(param_cols, PRODUCT_NAMES):
            d = DEFAULTS[name]
            with col:
                st.markdown(f"**{name}**")
                S = st.number_input(
                    f"Costo de pedido (COP)", value=d["S"],
                    step=10_000, key=f"S_{name}",
                )
                uv = st.number_input(
                    f"Valor unitario (COP/t)", value=d["unit_value"],
                    step=100_000, key=f"uv_{name}",
                )
                H_pct = st.number_input(
                    f"% mantenimiento", value=d["H_pct"],
                    step=0.01, format="%.2f", key=f"H_{name}",
                )
                lt = st.number_input(
                    f"Lead time (días)", value=d["lead_time"],
                    step=1, key=f"lt_{name}",
                )
                edited_params[name] = {
                    "S": S, "H": H_pct * uv, "lead_time": lt,
                }

    products_eoq = []
    products_ss = []
    results_table = []

    for name in PRODUCT_NAMES:
        data = get_product_data(name)
        D = data["production"][-1]  # annual demand = latest year production
        params = edited_params[name]

        # Daily statistics (365-day year). The daily standard deviation comes
        # straight from the historical production series, with no CV ratio.
        # Lead-time variability (sigma_L) is not modelled: the textbook form is
        # SS = z * sqrt(L*sigma_d^2 + d^2*sigma_L^2), but sigma_L has no data source
        # either, so it stays documented in README.md instead of hardcoded here.
        daily_demand = D / 365
        daily_std = np.std(data["production"], ddof=1) / 365

        products_eoq.append({
            "name": name,
            "demand_per_year": D,
            "order_cost": params["S"],
            "holding_cost": params["H"],
        })
        products_ss.append({
            "name": name,
            "demand_std": daily_std,
            "avg_daily_demand": daily_demand,
            "lead_time": params["lead_time"],
        })

    eoq_res = eoq(products_eoq)
    ss_res = safety_stock(products_ss, service_factor)

    # Results
    st.subheader("Resultados EOQ y Stock de Seguridad")
    for i, name in enumerate(PRODUCT_NAMES):
        q = eoq_res["products"][i]
        s = ss_res[i]
        D = products_eoq[i]["demand_per_year"]
        orders_year = D / q["q_star"]
        days_between = 365 / orders_year
        results_table.append({
            "Producto": name,
            "Demanda anual (t)": f"{D:,.0f}",
            "Q* (t)": f"{q['q_star']:,.1f}",
            "Pedidos/año": f"{orders_year:,.1f}",
            "Días entre pedidos": f"{days_between:,.1f}",
            "Costo anual inv. (COP)": f"{q['annual_cost']:,.0f}",
            "Stock seguridad (t)": f"{s['safety_stock']:,.1f}",
            "Punto de reorden (t)": f"{s['reorder_point']:,.1f}",
        })

    st.dataframe(
        pd.DataFrame(results_table), hide_index=True, use_container_width=True,
    )

    st.metric(
        "Costo anual total de inventario (COP)",
        f"${eoq_res['total_annual_cost']:,.0f}",
    )

    # Q* comparison bar chart
    fig_q = go.Figure()
    fig_q.add_trace(go.Bar(
        x=PRODUCT_NAMES,
        y=[eoq_res["products"][i]["q_star"] for i in range(3)],
        marker_color=[COLORS[i] for i in range(3)],
        text=[f"{eoq_res['products'][i]['q_star']:,.0f}" for i in range(3)],
        textposition="outside",
    ))
    fig_q.update_layout(
        **_base_layout(), height=350,
        title="Cantidad óptima de pedido (Q*) por producto",
        yaxis_title="Toneladas",
    )
    st.plotly_chart(fig_q, use_container_width=True)

    # Sawtooth inventory pattern
    st.subheader("Política de inventario (patrón diente de sierra)")
    for i, name in enumerate(PRODUCT_NAMES):
        q_star = eoq_res["products"][i]["q_star"]
        ss_val = ss_res[i]["safety_stock"]
        rop = ss_res[i]["reorder_point"]
        D_daily = products_eoq[i]["demand_per_year"] / 365
        lt = products_ss[i]["lead_time"]
        cycle_days = q_star / D_daily

        # Build 3 cycles
        t_points = []
        inv_points = []
        t = 0
        for _cycle in range(3):
            t_points.extend([t, t + cycle_days])
            inv_points.extend([q_star + ss_val, ss_val])
            t += cycle_days

        fig_saw = go.Figure()
        fig_saw.add_trace(go.Scatter(
            x=t_points, y=inv_points, mode="lines",
            name="Inventario", line=dict(color=COLORS[i], width=2.5),
        ))
        # Safety stock line
        fig_saw.add_hline(
            y=ss_val, line_dash="dash",
            line_color="rgba(255,255,255,0.3)",
            annotation_text="Stock de seguridad",
            annotation_font_color="#9ca3af",
        )
        # Reorder point line
        fig_saw.add_hline(
            y=rop, line_dash="dot",
            line_color=COLORS[2],
            annotation_text="Punto de reorden",
            annotation_font_color=COLORS[2],
        )
        fig_saw.update_layout(
            **_base_layout(), height=300,
            title=f"{name} — Ciclo de inventario",
            xaxis_title="Días", yaxis_title="Toneladas",
            showlegend=False,
        )
        st.plotly_chart(fig_saw, use_container_width=True)

    st.caption(FUENTE)
