# ERP — Programación Lineal (5 productos)

App web (Streamlit) para una empresa con 5 productos que resuelve problemas de
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
(5 segmentos: Galletitas, Chocolates, Golosinas, Alfajores, Cereales) son editables.

## Tests

```bash
.venv/bin/python -m pytest -q
```

## Fuentes y aproximaciones

Los datos por defecto de la app están inspirados en información pública de Arcor.
Sección "Fuentes":

- https://www.arcor.com/ar/informacion-financiera — público: ingresos 2025
  ($4.902.647 millones ARS), resultado operativo ($293.291 millones, ~6 % de margen)
  e inversiones ($208.139 millones).
- https://www.arcor.com/ar/plantas-industriales — público: 49 plantas; se usan como
  orígenes el Complejo Arcor Arroyito (Córdoba), el Complejo Arcor Recreo (Tucumán)
  y Arcor Mar del Plata.
- https://www.arcor.com/ar y https://www.arcor.com/ar/quienes-somos — público: marcas
  presentes en más de 100 países, exportador N°1 de golosinas de Argentina/Chile/Perú,
  líder regional en galletas, alfajores y cereales.
- https://www.arcor.com/ar/nuestros-negocios — público: Agronegocios produce internamente
  azúcar, fructosa, glucosa, almidón y harina de maíz (integración vertical).
- https://www.arcor.com/ar/plantas-industriales — público: 24 plantas en Argentina, entre
  ellas San Luis, Villa Mercedes, Colonia Caroya y La Reducción.
- Alfajores: Bagley (Arcor 51 %, Danone 49 %) lidera el mercado; ver
  https://alfajor.com.ar/marcas.
- Cereales: Arcor lanzó su línea de cereales en 2012 (Grupo Arcor, Wikipedia:
  https://en.wikipedia.org/wiki/Grupo_Arcor).

Estimado (no oficial): precios y costos unitarios por tonelada calibrados para un
margen operativo aproximado del 6 %, capacidades de planta, demandas anuales por
segmento, costos logísticos por distancia y costos de pedido/mantenimiento.

## Fórmulas

- LP max: `max c'x` s.a. `Ax <= b`, vía `scipy.optimize.linprog`
- Transporte: min del costo total s.a. oferta y demanda balanceadas
- EOQ: `Q* = sqrt(2*D*S/H)`
- Stock de seguridad: `SS = z * sigma * sqrt(L)`; punto de reorden: `ROP = d*L + SS`
