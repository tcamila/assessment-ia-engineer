import pandas as pd
from src.db.connection import execute_query

def get_kpis_dashboard(org_id: int) -> dict:
    """Retorna los KPIs principales para el dashboard."""
    query = """
    SELECT 
        (SELECT COUNT(*) FROM asociados WHERE id_organizacion = ?) as total_asociados,
        (SELECT COUNT(*) 
         FROM transacciones t 
         JOIN cuentas c ON t.id_cuenta = c.id_cuenta
         JOIN asociados a ON c.id_asociado = a.id_asociado
         WHERE a.id_organizacion = ?) as total_transacciones,
        (SELECT COUNT(*)
         FROM alertas a2
         JOIN asociados asoc2 ON a2.id_asociado = asoc2.id_asociado
         WHERE asoc2.id_organizacion = ? AND a2.estado != 'Cerrada') as total_alertas
    """
    df = execute_query(query, params=(org_id, org_id, org_id))
    if not df.empty:
        return df.iloc[0].to_dict()
    return {"total_asociados": 0, "total_transacciones": 0, "total_alertas": 0}

def get_transacciones_recientes(org_id: int, limit: int = 50) -> pd.DataFrame:
    """Retorna las transacciones más recientes."""
    query = """
        SELECT t.id_transaccion, t.fecha_transaccion, t.tipo_transaccion, t.monto, t.estado, 
               a.nombre || ' ' || a.apellido as asociado
        FROM transacciones t
        JOIN cuentas c ON t.id_cuenta = c.id_cuenta
        JOIN asociados a ON c.id_asociado = a.id_asociado
        WHERE a.id_organizacion = ?
        ORDER BY t.fecha_transaccion DESC
        LIMIT ?
    """
    return execute_query(query, params=(org_id, limit))

def get_resumen_alertas(org_id: int) -> pd.DataFrame:
    """Retorna un conteo de alertas activas agrupadas por severidad."""
    query = """
        SELECT a.severidad, COUNT(*) as cantidad
        FROM alertas a
        JOIN asociados asoc ON a.id_asociado = asoc.id_asociado
        WHERE asoc.id_organizacion = ? AND a.estado IN ('Abierta', 'En revision')
        GROUP BY a.severidad
    """
    return execute_query(query, params=(org_id,))

def get_transacciones_por_tipo(org_id: int) -> pd.DataFrame:
    """Retorna la suma de transacciones agrupadas por tipo."""
    query = """
        SELECT t.tipo_transaccion, SUM(t.monto) as monto_total
        FROM transacciones t
        JOIN cuentas c ON t.id_cuenta = c.id_cuenta
        JOIN asociados a ON c.id_asociado = a.id_asociado
        WHERE a.id_organizacion = ?
        GROUP BY t.tipo_transaccion
    """
    return execute_query(query, params=(org_id,))

def get_ranking_asociados(org_id: int, limit: int = 10) -> pd.DataFrame:
    """Retorna los asociados con mayor volumen transaccional."""
    query = """
        SELECT asoc.nombre || ' ' || asoc.apellido as asociado,
               COUNT(t.id_transaccion) as cantidad_tx,
               SUM(t.monto) as volumen_total
        FROM asociados asoc
        JOIN cuentas c ON asoc.id_asociado = c.id_asociado
        JOIN transacciones t ON c.id_cuenta = t.id_cuenta
        WHERE asoc.id_organizacion = ?
        GROUP BY asoc.id_asociado
        ORDER BY volumen_total DESC
        LIMIT ?
    """
    return execute_query(query, params=(org_id, limit))
