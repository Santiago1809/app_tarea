# ERP — Programación Lineal (3 productos)

App web (Streamlit) para una empresa con 3 productos que resuelve problemas de
investigación de operaciones:

- **Maximización de ganancias** — LP de producción con restricciones de recursos
- **Minimización de costos** — LP con restricciones de cumplimiento de demanda
- **Logística de transporte** — problema de transporte balanceado (plantas x destinos)
- **Abastecimiento** — EOQ (Q*) y stock de seguridad con punto de reorden

## Uso

```bash
.venv/bin/python -m streamlit run app.py
```

Abre en el navegador y elegí la sección en la barra lateral. Los datos de ejemplo
(3 productos: A, B, C) son editables.

## Tests

```bash
.venv/bin/python -m pytest -q
```

## Fórmulas

- LP max: `max c'x` s.a. `Ax <= b`, vía `scipy.optimize.linprog`
- Transporte: min del costo total s.a. oferta y demanda balanceadas
- EOQ: `Q* = sqrt(2*D*S/H)`
- Stock de seguridad: `SS = z * sigma * sqrt(L)`; punto de reorden: `ROP = d*L + SS`
