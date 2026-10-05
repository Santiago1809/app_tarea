# UI premium (feature ui-premium)

## Objetivo
Elevar la UI de la app Streamlit con la skill high-end-visual-design, sin cambiar lógica.

## Alcance
- CSS en `app.py`: doble bisel en tarjetas, sombras sin negro duro, transiciones con cubic-bezier, grano fijo, mobile <768px.
- Navegación del sidebar como pills (selectores `stRadioOption`).
- `.streamlit/config.toml`: tema oscuro nativo para tablas y widgets.

## Adaptaciones a Streamlit
- Sin blur en animaciones de entrada (checklist: solo transform y opacity).
- Doble bisel aproximado con `box-shadow` (no hay wrapper propio en Streamlit).
- Sin botones con flecha: no aplica el patrón button-in-button.

## Tareas
- [x] t1 — CSS premium + sidebar pills + tema oscuro + mobile

## Verificación
- pytest: 8 passed.
- Capturas Playwright (Chromium del sistema): desktop, sección Minimizar costos, mobile 390px sin overflow horizontal.

## Estado: COMPLETO
