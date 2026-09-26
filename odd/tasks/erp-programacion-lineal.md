# ERP — Programación Lineal (3 productos)

## Objetivo
App web (Streamlit) para una empresa con 3 productos, resolviendo problemas de
investigación de operaciones: maximización de ganancias, minimización de costos,
logística de transporte, logística de abastecimiento (Q* EOQ + stock de seguridad).

## Scope autorizado
- Módulo LP con scipy.linprog: max ganancias + min costos (restricciones editables)
- Transporte (transportation problem, balanceado) vía linprog
- EOQ (Q*) + stock de seguridad con demanda variable
- UI Streamlit con datos de ejemplo precargados y parámetros editables
- Tests cortos por módulo (assert-based o pytest simple)

Fuera de scope: auth, base de datos persistente, multi-empresa, más de 3 productos.

## TDD: off (sin configuración del proyecto; se usan checks funcionales por tarea)

## Ruta por tarea
| ID | Tarea | Ruta | Evidencia |
|----|-------|------|-----------|
| t1 | Módulo `lp_core.py`: resolución LP genérica + max ganancias + min costos + tests | delegado | verificación: `.venv/bin/python -m pytest -q` |
| t2 | Módulo `transporte.py`: problema de transporte balanceado + tests | delegado | verificación: `.venv/bin/python -m pytest -q` |
| t3 | Módulo `abastecimiento.py`: EOQ Q* + stock de seguridad + tests | delegado | verificación: `.venv/bin/python -m pytest -q` |
| t4 | `app.py` Streamlit con 4 secciones y datos de ejemplo | delegado | verificación: app compila, smoke test con `streamlit run --server.headless true` |
| t5 | README con fórmulas y modo de uso + cierre | inline | readback |

## Progreso
- [ ] t1 — LP core
- [ ] t2 — transporte
- [ ] t3 — abastecimiento (Q*, SS)
- [ ] t4 — app Streamlit
- [ ] t5 — README + cierre
