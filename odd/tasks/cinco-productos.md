# ERP — 5 productos (feature cinco-productos)

## Objetivo
Ampliar el ERP de 3 a 5 productos, incorporando datos públicos de Arcor obtenidos de la web.

## Problema
Los módulos LP y abastecimiento y la UI están fijos a 3 segmentos (Galletitas, Chocolates, Golosinas).

## Por qué
Pedido del usuario: más productos para el ejercicio de optimización y sustento de datos desde fuentes públicas.

## Alcance autorizado
- Dos productos nuevos: **Alfajores** y **Cereales** (elegidos por ser segmentos de Arcor con marca y línea productiva pública).
- Actualizar listas de productos, recursos y datos por defecto en `app.py`.
- Actualizar textos de UI/README que dicen "tres".
- Tests del módulo LP con 5 productos.
- Registro de fuentes web en README.

## Fuera de alcance
- Cambiar transporte (plantas/destinos) o la sección de insumos de "Minimizar costos".
- Scripts de scraping persistentes; la extracción fue manual con WebFetch/WebSearch.

## Restricciones
- Costos unitarios, precios, demandas y capacidades por producto **no son públicos**: quedan como estimaciones calibradas a ~6 % de margen (igual criterio que el proyecto).
- Balance transporte: oferta 125 = demanda 125 (sin cambios).

## Fuentes (evidencia web)
- https://www.arcor.com/ar/nuestros-negocios — segmentos: chocolates, golosinas, galletas, helados, suplementos; Agronegocios; Packaging.
- https://www.arcor.com/ar/plantas-industriales — 24 plantas en Argentina (incluye Arroyito, Recreo, Mar del Plata, San Luis, Villa Mercedes, Colonia Caroya, Río Seco, La Reducción).
- https://www.arcor.com/ar/informacion-financiera — ingresos 2025 $4.902.647 M, resultado operativo $293.291 M.
- https://alfajor.com.ar/marcas — mercado de alfajores; Bagley (Arcor 51 %, Danone 49 %) lidera.
- https://en.wikipedia.org/wiki/Grupo_Arcor — Arcor lanzó cereales en 2012 (dato de búsqueda, no verificado en la página primaria).

## Tareas

- [ ] t1 — `.gitignore`: ignorar `.codegraph/` — commit `5cf6378`
- [x] t2 — `app.py`: 5 productos en LP (precios, costos, usos por recurso), abastecimiento e índices
- [x] t3 — `test_lp_core.py`: caso de 5 productos verificable a mano (44 = 4·5 + 6·4)
- [x] t4 — `README.md`: 5 productos, fuentes nuevas, sin "tres"

## Ruta por tarea
- t1: inline (ya hecho).
- t2–t4: inline. Motivo: edición mecánica y ya entendida en el mismo contexto; 3 archivos pero sin investigación previa pendiente. Declarado para trazabilidad.

## Verificación
- Por tarea: `.venv/bin/python -m pytest -q` (base: 7 passed).
- Final: `streamlit` arranca y `healthz` responde 200.

## Progreso
- t1 done (`5cf6378`).
- t2–t4 done. Pytest: 8 passed. Streamlit smoke: healthz 200.
- Nota: con los datos por defecto, el óptimo de "Maximizar ganancias" produce solo Cereales (55,6 t). Es consecuencia de las estimaciones, no un bug; conviene recalibrar si se quiere un mix.

## Estado: COMPLETO (pendiente commit de t2–t4)
