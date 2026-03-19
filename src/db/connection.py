import sqlite3
import pandas as pd
from src.utils.config import Config

def get_db_connection():
    """
    Esta función abre un túnel (conexión) hacia nuestra base de datos local SQLite.
    No recibe parámetros.
    Retorna: Un objeto de conexión de sqlite3 (conn).
    """
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """
    Esta función ejecuta una consulta SQL y convierte el resultado en una tabla fácil de leer usando Pandas.
    Recibe: query (texto de tu consulta) y params (tupla con variables seguras, es opcional).
    Retorna: Un DataFrame de pandas (tabla de datos).
    """
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        raise Exception(f"Se produjo un error ejecutando la consulta: {e}")

def execute_query_raw(query: str, params: tuple = ()) -> list:
    """
    Esta función ejecuta una consulta SQL pero, en lugar de una tabla de pandas, devuelve una lista común de Python.
    Recibe: query (texto de tu consulta) y params (tupla opcional).
    Retorna: Una lista donde cada fila es un diccionario con el nombre de la columna y el valor.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description] if cursor.description else []
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    except Exception as e:
        raise Exception(f"Query error: {e}")
    finally:
        conn.close()
