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
segmento y costos logísticos por distancia.

### Con fuente pública

Costos de mantenimiento (`H_pct`) — los valores 22 % (Café), 25 % (Arroz) y 55 %
(Plátano) son una construcción bottom-up propia, no un porcentaje publicado. Las
piezas públicas que los sostienen:

- BanRep, tasa de política monetaria 12,25 % EA (oct-2026):
  https://www.banrep.gov.co/es/glosario/tasa-usura — el solo costo de capital ya
  consume el 15 % que la app asumía antes.
- FAO SDG 12.3.1, pérdidas por grupo de commodity (2023):
  https://www.fao.org/sustainable-development-goals-data-portal/data/indicators/1231-global-food-losses/en
  — frutas y vegetales 25,4 % vs. cereales y legumbres 8,4 %, base para separar el
  plátano (perecedero) del café (seco).
- DNP, Encuesta Nacional de Logística:
  https://www.dnp.gov.co/Prensa_/Noticias/Paginas/La-logistica-del-pais-avanza-impulsada-por-regiones-menores-costos-encuesta-nacional-logistica.aspx
  — almacenamiento = 29,0 % del costo logístico del sector agropecuario, el más
  alto de todos los sectores.

Lead times (días) — el modelo es compra doméstica, no importación:

- Café 14 días: IDH/Enveritas documenta intermediarios que retienen el café ~9 días
  y productores que entregan cada 2-3 semanas en cosecha:
  https://idh-prp.files.prepr.io/3yhjieznkva-.pdf
- Arroz 7 días (antes 14): ANDI describe el paddy verde como bien perecedero, vendido
  a molino cercano; molinos del Meta secan 200 t/día, sólo la cola de precio agrega
  días: https://andi.com.co/Uploads/Estudio%20Completo.pdf
- Plátano 2 días (antes 10): el empaque en finca ocurre el mismo día de la cosecha y
  la vida útil del plátano verde es 7-28 días a 12-13 °C, así que 10 días de lead
  time más stock de seguridad modelaba ~25 días de cobertura sobre un techo físico
  de 28: https://repositorio.unal.edu.co/bitstreams/176f336c-3eb3-4733-9229-eb0966dcc184/download

### Sin fuente, declarados como supuesto

- **σ de demanda.** Sin fuente pública. DANE EVA sólo tiene frecuencia anual
  (Café, Plátano) y semestral (Arroz); no hay series mensuales. `σ` se deriva
  directamente de la desviación estándar muestral de la producción histórica
  (`sigma = std(producción)/365`): mide dispersión inter-anual, no variabilidad
  operacional diaria, y mezcla variabilidad climática con operativa. Usar el
  semestral del arroz empeora σ 1,394× porque capta el vaivén entre mitaca y
  cosecha principal: descartado.
- **`S` (costo de pedido).** Sin fuente pública colombiana. Es un supuesto
  administrativo, no un costo logístico medido. Los valores por defecto se
  calibraron para que el ciclo EOQ supere el lead time (≈24, 12 y 3,6 días para
  Café, Arroz y Plátano) y el punto de reorden sea alcanzable dentro del ciclo;
  con los valores anteriores el ciclo era de 0,17-0,38 días y el ROP quedaba por
  encima del inventario máximo.
- **σ_L (variabilidad del lead time).** No modelada. La fórmula estándar sería
  `SS = z*sqrt(L̄*σ_d² + d̄²*σ_L²)`; se deja así mientras σ siga siendo un proxy.

## Fórmulas

- LP max: `max c'x` s.a. `Ax <= b`, vía `scipy.optimize.linprog`
- Transporte: min del costo total s.a. oferta y demanda balanceadas
- EOQ: `Q* = sqrt(2*D*S/H)`
- Stock de seguridad: `SS = z * sigma * sqrt(L)`; punto de reorden: `ROP = d*L + SS`
- `sigma` (desviación estándar diaria) se deriva de la serie histórica:
  `sigma = std(producción anual) / 365`. La sección de Gestión de Inventario
  recalcula todo en cada rerun, así que cualquier cambio en un parámetro se
  refleja de inmediato, sin botón de por medio.
