from groq import Groq
from src.utils.config import Config

class LLMClient:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.LLM_MODEL
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
    
    def is_available(self):
        return self.client is not None
        
    def generate_sql(self, system_prompt: str, user_query: str) -> str:
        """Llama al LLM para traducir un prompt de usuario a SQL"""
        if not self.is_available():
            raise ValueError("Groq API key no configurada.")
            
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"PREGUNTA DEL USUARIO: {user_query}. "
                                          f"RECUPERA ÚNICAMENTE EL SQL SIN MARCAS DE CÓDIGO NI EXPLICACIONES."}
            ],
            model=self.model,
            temperature=0.0
        )
        query = response.choices[0].message.content.strip()
        
        # Limpiar si el LLM aún insiste en poner backticks
        if query.startswith("```sql"):
            query = query[6:]
        if query.startswith("```"):
            query = query[3:]
        if query.endswith("```"):
            query = query[:-3]
            
        return query.strip()

    def generate_summary(self, system_prompt: str, data_context: str) -> str:
        """Llama al LLM para resumir los hallazgos de monitoreo o tablas."""
        if not self.is_available():
            raise ValueError("Groq API key no configurada.")
            
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"DATOS DE CONTEXTO:\n{data_context}\n\nGenera un resumen profesional."}
            ],
            model=self.model,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
