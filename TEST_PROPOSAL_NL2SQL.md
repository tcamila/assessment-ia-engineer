# Propuesta de Prueba Funcional: Agregación Financiera por Segmento (NL2SQL)

## 1. Nueva Consulta de Ejemplo
**Pregunta Natural:** *"¿Cuál es el saldo total acumulado de mis asociados por cada segmento?"*
**Valor:** Permite al analista evaluar la distribución de liquidez y el peso financiero de cada tipo de cliente (Persona Natural vs. Jurídica) sin realizar cálculos manuales.

## 2. Resultado Esperado
Una tabla (DataFrame) con dos columnas:
*   **segmento**: El nombre del segmento (ej. 'Persona Natural').
*   **saldo_total**: La suma de los saldos de todas las cuentas pertenecientes a los asociados de dicho segmento.

## 3. Módulos Involucrados
*   **`src/nl_query/nl2sql.py`**: Intercepta la pregunta e invoca la generación/validación.
*   **`src/llm/prompt_builder.py`**: Provee el esquema de las tablas `asociados` y `cuentas` al LLM.
*   **`src/llm/sql_guardrails.py`**: Valida la sintaxis, el filtrado por organización y bloquea comandos DML/DDL.
*   **`src/db/connection.py`**: Ejecuta la consulta final parametrizada en SQLite.

## 4. Validaciones Técnicas
Para que la prueba sea exitosa, el sistema debe garantizar:
1.  **Aislamiento Multi-Tenant**: El SQL generado debe realizar un `JOIN` entre `asociados` y `cuentas` e incluir estrictamente la cláusula `WHERE asociados.id_organizacion = ?`. No debe haber exposición de saldos de otras cooperativas.
2.  **Uso Exclusivo de SELECT**: `SQLGuardrails` debe rechazar la consulta si el LLM intenta inyectar comandos de escritura o borrado.
3.  **Compatibilidad Parametrizada**: La ejecución debe realizarse pasando el `st.session_state["organization_id"]` como una tupla de parámetros, evitando inyección SQL por concatenación de strings.

## 5. Plan de Pruebas (Rama Nueva)
**Nombre de rama sugerido:** `feature/test-segment-aggregation`

1.  **Aislamiento de Lógica**: Crear un script de test unitario que instancie `NLPQueryEngine` con un `organization_id` específico.
2.  **Simulación de Respuesta (Mocking)**: Configurar el cliente de LLM para devolver el SQL esperado:
    `SELECT a.segmento, SUM(c.saldo) FROM asociados a JOIN cuentas c ON a.id_asociado = c.id_asociado WHERE a.id_organizacion = ? GROUP BY a.segmento`.
3.  **Verificación de Guardrails**: Llamar a `SQLGuardrails.validate_and_format_query` y asegurar que no lance `SecurityException`.
4.  **Ejecución y Assertions**: Comprobar que los datos devueltos coincidan con la sumatoria real de la base de datos para esa organización específica.
