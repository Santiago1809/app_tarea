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
- [x] t1 — LP core (pytest: 7 passed) — commit 56e17ec
- [x] t2 — transporte (ídem) — commit 56e17ec
- [x] t3 — abastecimiento (ídem) — commit 56e17ec
- [x] t4 — app Streamlit (healthz 200) — commit 56e17ec
- [x] t5 — README + cierre — incluido en commit 56e17ec
- [x] t6 — datos reales (Arcor) adaptados — commit 7d9c0ab; verificador independiente PASS, pytest 7 passed, healthz 200


## Verificación
- Writer: pytest 7 passed; streamlit healthz 200.
- Verificador independiente: PASS los 7 checks, fórmulas EOQ/SS/transporte/LP recomputadas, sin defectos.
- RDD: off (decisión global del usuario). Assessment: unassessable→tier alto por untracked; cubierto con verificador independiente.

## Estado: COMPLETO
