import pandas as pd
from src.db.connection import execute_query

def execute_monitoring_rules(org_id: int) -> dict:
    """
    Esta función ejecuta scripts automáticos (reglas) para buscar problemas o comportamientos extraños en todos los asociados al mismo tiempo. Siempre protegiendo los parámetros con `?` contra inyección SQL.
    Recibe: org_id (el identificador de la organización del analista logueado, ej. 1).
    Retorna: Un diccionario agrupando todos los hallazgos en texto (findings) y las métricas numéricas asociadas.
    """
    findings = []
    metrics = {}
    
    # Regla 1: Asociados con múltiples alertas abiertas o en revisión
    query_alertas = """
        SELECT asoc.nombre || ' ' || asoc.apellido as asociado, COUNT(a.id_alerta) as num_alertas
        FROM asociados asoc
        JOIN alertas a ON asoc.id_asociado = a.id_asociado
        WHERE asoc.id_organizacion = ? AND a.estado IN ('Abierta', 'En revision', 'Escalada')
        GROUP BY asoc.id_asociado
        HAVING num_alertas >= 3
    """
    df_alertas = execute_query(query_alertas, params=(org_id,))
    if not df_alertas.empty:
        for idx, row in df_alertas.iterrows():
            findings.append(f"El asociado {row['asociado']} tiene {row['num_alertas']} alertas activas.")
            
    metrics["asociados_multialertas"] = len(df_alertas)

    # Regla 2: Transacciones inusualmente altas (más de 20M por ejemplo, limitadas a 5)
    query_altas = """
        SELECT t.id_transaccion, t.monto, asoc.nombre || ' ' || asoc.apellido as asociado
        FROM transacciones t
        JOIN cuentas c ON t.id_cuenta = c.id_cuenta
        JOIN asociados asoc ON c.id_asociado = asoc.id_asociado
        WHERE asoc.id_organizacion = ? AND t.monto > 20000000
        ORDER BY t.monto DESC
        LIMIT 5
    """
    df_altas = execute_query(query_altas, params=(org_id,))
    if not df_altas.empty:
        for idx, row in df_altas.iterrows():
            findings.append(f"Transacción de riesgo excesivo (Monto detectado: ${row['monto']:,.2f}) detectada para asociado {row['asociado']}.")
            
    metrics["transacciones_altas"] = len(df_altas)
    
    return {
        "findings": findings,
        "metrics": metrics
    }
