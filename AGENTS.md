# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python env lives in `.venv/` (Python 3.14, scipy, numpy, pandas, streamlit, plotly, pytest). Always call its binaries explicitly.

```bash
# Run the Streamlit app
.venv/bin/python -m streamlit run app.py

# All tests
.venv/bin/python -m pytest -q

# One file / one test
.venv/bin/python -m pytest -q test_pronosticos.py
.venv/bin/python -m pytest -q test_lp_core.py::test_helpers

# Regenerate the non-governmental monthly dataset (network: UN Comtrade + FNC)
.venv/bin/python scripts/fetch_datos_privados.py --out datos_privados.py
```

There is no linter or build step configured.

## Architecture

Streamlit ERP for Colombian agricultural products (Café, Arroz, Plátano) covering demand history, demand forecasting and inventory management, built on real public data. UI copy and domain vocabulary are in Spanish; code identifiers are English snake_case.

**Layering (flat, no packages):**

- `app.py` — the only UI. Sidebar sections: "Dashboard", "Demanda Histórica", "Proyección de Demanda", "Gestión de Inventario". Charts use Plotly with a shared dark layout helper (`_base_layout`); every chart cites the data source via `FUENTE`.
- `datos_eva.py` — embedded DANE EVA dataset (datos.gov.co resources `2pnw-mmge` 2007–2018 and `uejq-wxrr` 2019–2025). Exposes `PRODUCT_NAMES`, `DATA_SOURCE`, `get_product_data`. No live API calls at runtime.
- `pronosticos.py` — forecasting: moving average, weighted moving average (`weights[0]` = most recent period, must sum to 1), exponential smoothing, linear regression, plus `forecast_errors`. Forecast lists have length `len(values)+1`, with `None` where undefined; the last entry is the next-period forecast.
- `abastecimiento.py` — closed-form inventory math (EOQ, safety stock, reorder point). No solver.
- `scripts/fetch_datos_privados.py` — generates `datos_privados.py` (monthly series from UN Comtrade and Federación Nacional de Cafeteros). Comtrade is rate-limited (~1 req / 2 s, one period per request); the FNC XLSX is parsed with stdlib only because `openpyxl` is not installed. Output is deterministic except for the `accessed` stamp. `datos_privados.py` is not committed yet, so `test_datos_privados.py` fails at collection until it is generated.
- `lp_core.py` / `transporte.py` — LP wrapper (`scipy.optimize.linprog`, `method="highs"`) and balanced transportation problem from the original Arcor version. They are still tested but no longer imported by `app.py`.

**Conventions to keep:**

- Solver modules return plain dicts (`success`, `status`, `message`, result fields) and never raise on infeasibility; callers branch on `success`.
- Tests are plain pytest files `test_<module>.py` next to their module (no `tests/` dir, no conftest), asserting against hand-computed or textbook values.
- Formulas are documented in `README.md` ("Fórmulas"); keep them in sync if the math changes.

## Process

- Feature tracking docs live in `odd/tasks/`. Active features: `erp-demanda-colombiano.md` (Colombian data migration), `ui-premium.md`, `cinco-productos.md`; `erp-programacion-lineal.md` is the original LP build (complete).
- `.atl/` is local agent state and is not part of the app.
