import re
import pandas as pd
from src.llm.groq_client import LLMClient
from src.llm.prompt_builder import build_system_prompt
from src.llm.sql_guardrails import SQLGuardrails, SecurityException
from src.db.connection import execute_query
from src.utils.config import Config

class NLPQueryEngine:
    def __init__(self, organization_id: int):
        self.org_id = organization_id
        self.llm = LLMClient()
    
    def process_query(self, user_question: str) -> dict:
        """
        Esta función principal toma la pregunta natural del usuario, decide si responde usando Inteligencia Artificial o lógica fija offline local, valida la seguridad usando Guardrails, ejecuta la consulta y retorna una tabla de datos.
        Recibe: user_question (texto natural, ej. ¿Cuántos asociados existen?).
        Retorna: Un diccionario que contiene el estado de éxito, la tabla de resultados (data) y la consulta (sql).
        """
        try:
            if self.llm.is_available():
                sql_query = self._generate_with_ai(user_question)
            else:
                sql_query = self._fallback_query_generator(user_question)

            # Validar e inyectar limite con los Guardrails
            # Como el prompt ya instruye añadir id_organizacion = ?, validamos fuertemente:
            if "id_organizacion = ?" not in sql_query and "id_organizacion=?" not in sql_query.replace(" ",""):
                 raise SecurityException("La consulta generada no incluyó explícitamente el filtro `id_organizacion = ?`.")

            safe_sql = SQLGuardrails.validate_and_format_query(
                sql_query, 
                self.org_id, 
                limit=Config.QUERY_LIMIT
            )

            # Pasamos org_id como parametro estrico (tupla)
            results_df = execute_query(safe_sql, params=(self.org_id,))
            
            return {
                "status": "success",
                "sql": safe_sql,
                "data": results_df,
                "message": "Consulta ejecutada correctamente (Aislada a tu organización)."
            }

        except SecurityException as se:
            return {"status": "error", "message": f"Error de Seguridad: {str(se)}"}
        except Exception as e:
            return {"status": "error", "message": f"Error Procesando Consulta: {str(e)}"}

    def _generate_with_ai(self, question: str) -> str:
        prompt = build_system_prompt(self.org_id)
        return self.llm.generate_sql(prompt, question)

    def _fallback_query_generator(self, question: str) -> str:
        """
        Fallback basado en heurísticas paramétricas.
        """
        q = question.lower()
        if "asociados" in q and "cuantos" in q:
            return "SELECT count(*) as total_asociados FROM asociados WHERE id_organizacion = ?"
        elif "asociados" in q:
            return "SELECT nombre, apellido, segmento, ciudad FROM asociados WHERE id_organizacion = ? ORDER BY fecha_registro DESC LIMIT 10"
        elif "transacciones" in q and "ultimo mes" in q:
            return """
            SELECT t.tipo_transaccion, t.monto, t.fecha_transaccion, t.estado 
            FROM transacciones t
            JOIN cuentas c ON t.id_cuenta = c.id_cuenta
            JOIN asociados a ON c.id_asociado = a.id_asociado
            WHERE a.id_organizacion = ?
            ORDER BY t.fecha_transaccion DESC LIMIT 50
            """
        elif "alertas" in q:
            return """
            SELECT a.tipo_alerta, a.severidad, a.estado, a.fecha_creacion, asocia.nombre
            FROM alertas a
            JOIN asociados asocia ON a.id_asociado = asocia.id_asociado
            WHERE asocia.id_organizacion = ?
            """
        elif "analistas" in q:
            return "SELECT nombre, apellido, especialidad FROM analistas WHERE id_organizacion = ?"
            
        raise ValueError("No puedo interpretar esta intención sin el uso de IA. Intenta con preguntas sobre 'asociados', 'alertas' o 'las transacciones del ultimo mes'.")
