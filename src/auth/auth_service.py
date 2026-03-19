import hashlib
from src.db.connection import execute_query_raw

def hash_password(password: str) -> str:
    """
    Esta función convierte una contraseña en texto plano en un código seguro (Hash SHA-256).
    Recibe: password (texto de la contraseña)
    Retorna: El texto transformado de 64 caracteres seguros (string).
    """
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str) -> dict:
    """
    Esta función verifica si el usuario y la contraseña existen en la base de datos de SQLite.
    Recibe: username (el nombre de usuario) y password (la clave en texto).
    Retorna: Un diccionario con los datos completos del usuario si es correcto (nombre, organización, etc) o None si falla.
    """
    hashed_pwd = hash_password(password)
    query = """
        SELECT u.id_usuario, u.username, u.nombre_completo, u.id_organizacion, u.rol, o.nombre as org_nombre
        FROM usuarios u
        JOIN organizaciones o ON u.id_organizacion = o.id_organizacion
        WHERE u.username = ? AND u.password_hash = ? AND u.activo = 1
    """
    results = execute_query_raw(query, (username, hashed_pwd))
    if results:
        return results[0]
    return None
