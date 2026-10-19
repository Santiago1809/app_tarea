# Feature: ERP Demanda Colombiano

## Objective
Replace the Arcor-based ERP with a Colombian agricultural ERP using real public data from the DANE EVA dataset (Evaluaciones Agropecuarias Municipales, datos.gov.co resource `2pnw-mmge`). Three products: Café, Arroz, Caña Panelera with 12 years of national production data (2007–2018).

## Problem
The user needs an enterprise-grade operations research tool showing demand analysis, forecasting models, and inventory management for 3 Colombian products sourced from public data.

## Why
University Operations Research assignment requiring real public data from a Colombian source, with demand forecasting models and inventory optimization.

## Scope
- Data from DANE EVA dataset embedded in the app (no live API dependency)
- 4 forecasting models: Moving Average, Weighted Moving Average, Exponential Smoothing, Linear Regression
- EOQ (Q*), safety stock, reorder point calculations per product
- Plotly charts for all visualizations
- Enterprise-quality dark UI (existing design system)

## Constraints
- Flat module architecture (no packages)
- Python 3.14, scipy, numpy, pandas, streamlit, plotly, pytest
- Spanish UI, English code identifiers
- Existing `abastecimiento.py` EOQ/SS module reused as-is

## Data source
- Portal: datos.gov.co (Datos Abiertos Colombia)
- Dataset: Evaluaciones Agropecuarias Municipales (EVA)
- Resource ID: `2pnw-mmge`
- API: `https://www.datos.gov.co/resource/2pnw-mmge.json`
- Fields used: `a_o` (year), `cultivo` (crop), `producci_n_t` (production tons), `rea_sembrada_ha`, `rea_cosechada_ha`
- Aggregation: national sum by year per crop

## Tasks

- [x] T1: Create `datos_eva.py` — embedded DANE EVA data for 3 products (12 years each)
- [x] T2: Create `pronosticos.py` — 4 forecasting models with error metrics
- [x] T3: Create `test_pronosticos.py` — tests for forecasting module
- [x] T4: Rewrite `app.py` — enterprise UI with Plotly charts, 4 sections + data source banner
- [x] T5: Run tests (14 passed), verify app (health 200), pending commit

## Acceptance criteria
- App loads with 3 Colombian products from DANE data
- Each product shows historical demand chart
- At least 4 forecasting models with comparison chart
- EOQ, safety stock, reorder point calculated and displayed
- All charts use Plotly
- `pytest -q` passes

## Route
Delegated direct (4 files, 2 new modules + app rewrite)

## Forecast: ~350 authored changed lines
## Delivery strategy: single-pr
