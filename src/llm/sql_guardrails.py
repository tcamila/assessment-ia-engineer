import sqlparse
import re

class SecurityException(Exception):
    pass

class SQLGuardrails:
    """
    Módulo de seguridad para validar y restringir consultas SQL generadas o manuales.
    - Bloquea consultas destructivas (DML/DDL excepto SELECT)
    - Inyecta o valida filtros obligatorios por organization_id
    - Agrega límites
    """

    FORBIDDEN_KEYWORDS = [
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", 
        "CREATE", "REPLACE", "GRANT", "REVOKE", "COMMIT", "ROLLBACK"
    ]

    @classmethod
    def validate_and_format_query(cls, query: str, organization_id: int, limit: int = 100) -> str:
        """
        1. Parsear y validar que solo exista SELECT.
        2. Validar o inyectar la restricción por id_organizacion.
        3. Aplicar límite.
        Si la query es inválida, levanta SecurityException.
        """
        query = query.strip()
        
        # 1. Validar que comience con SELECT
        if not query.upper().startswith("SELECT"):
            raise SecurityException("Operación no permitida: Solo se permiten consultas SELECT.")

        # 2. Parsear con sqlparse y validar keywords prohibidos
        parsed = sqlparse.parse(query)
        if not parsed:
            raise SecurityException("Consulta SQL inválida.")
        
        stmt = parsed[0]
        tokens_upper = [str(t).upper() for t in stmt.tokens if not t.is_whitespace]
        
        for keyword in cls.FORBIDDEN_KEYWORDS:
            if any(keyword in t_str for t_str in tokens_upper):
                raise SecurityException(f"Operación destructiva bloqueada: {keyword} no está permitido.")
        
        # 3. Forzar filtro por organización y límite
        # Utilizamos una aproximación con regex para verificar si usa un filtro de organizacion básico
        # Aunque el LLM está instruido explícitamente a incluirlo ("WHERE id_organizacion = ?").
        
        # Envolviendo o verificando la existencia del query de proteccion parametrizada
        org_filter_pattern = r"id_organizacion\s*=\s*\?"
        if not re.search(org_filter_pattern, query, re.IGNORECASE):
            # No encontró la restricción estricta en la cadena
            raise SecurityException("Filtro de seguridad faltante: La consulta no parece estar restringida a tu organización con parámetros seguros.")

        # 4. Asegurar el LIMIT
        if not re.search(r"LIMIT\s+\d+", query, re.IGNORECASE):
            query = f"{query} LIMIT {limit}"
        
        return query
