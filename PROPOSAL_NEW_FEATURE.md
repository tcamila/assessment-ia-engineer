# Propuesta de Nueva Funcionalidad: Insight-Driven Conversational Drill-down

## 1. Descripción de la Funcionalidad
Esta funcionalidad transforma el asistente de un motor de búsqueda pasivo a uno **proactivo**. Actualmente, el sistema entrega tablas de datos y el monitoreo corre por separado. Con esta mejora, al realizar una consulta NL2SQL, el sistema analiza automáticamente el resultado mediante el LLM y, cruzando la información con las reglas de `monitoring/rules.py`, ofrece:
1.  **Resumen de Hallazgos**: Interpretación en lenguaje natural de los datos obtenidos (ej. *"Se observa un incremento del 20% en transacciones de alto riesgo en este periodo"*).
2.  **Sugerencias de Seguimiento**: Botones o preguntas sugeridas para profundizar en anomalías detectadas (ej. *"He detectado 3 asociados que disparan la Regla #1, ¿deseas ver sus perfiles?"*).

## 2. Justificación (Basada en el problema actual)
*   **Limitación actual del NL2SQL**: Es reactivo. El usuario recibe una tabla, pero si no tiene conocimientos técnicos o de riesgo, puede no saber qué buscar a continuación o ignorar anomalías invisibles a simple vista.
*   **Limitación del Monitoreo**: Está aislado en otra pestaña. El analista debe ir activamente a buscar riesgos en lugar de que el sistema se los señale durante su flujo de trabajo normal.
*   **Valor**: Une el poder del **Análisis de Datos** con el **Monitoreo de Riesgos** en una sola experiencia conversacional, guiando al analista hacia los problemas que realmente requieren atención.

## 3. Componentes Afectados
*   **`src/nl_query/nl2sql.py`**: Se actualiza `process_query` para que invoque el nuevo motor de interpretación.
*   **`src/nl_query/insights.py` (Nuevo)**: Módulo encargado de generar resúmenes estadísticos y sugerencias de seguimiento usando el LLM.
*   **`src/monitoring/rules.py`**: Se deben exponer las funciones de reglas para que el motor de insights pueda verificar hallazgos sobre DataFrames en memoria.
*   **`app.py`**: Modificación de la UI para mostrar "Sugerencias de Seguimiento" (botones rápidos) debajo de los resultados de la consulta.

## 4. Integración con el Flujo Actual
El flujo pasaría de ser lineal a **interactivo**:
1.  **Usuario** → Pregunta NL → **nl2sql.py** genera SQL.
2.  **SQL** → **db/connection.py** recupera DataFrame.
3.  **DataFrame** → **insights.py** (Analiza los datos + consulta a **rules.py**).
4.  **Sistema** → Devuelve al usuario: **Tabla** + **Resumen de Hallazgos** + **Preguntas de Seguimiento Sugeridas** (vía botones de Streamlit).

## 5. Plan de Implementación
1.  **Fase 1 (Lógica de Insights)**: Crear `src/nl_query/insights.py`. Diseñar un prompt que reciba un resumen estadístico del DataFrame y genere frases de interpretación profesional.
2.  **Fase 2 (Conexión con Monitoreo)**: Refactorizar `rules.py` para permitir verificaciones sobre DataFrames existentes sin re-consultar la base de datos.
3.  **Fase 3 (Interfaz Dinámica)**: Actualizar `app.py` para renderizar sugerencias dinámicas que alimenten el área de texto de la consulta al hacer clic.
4.  **Fase 4 (Aislamiento Multi-Tenant)**: Asegurar que las sugerencias hereden el contexto de la organización actual para evitar cruces de datos.
