from src.llm.groq_client import LLMClient

class MonitoringSummarizer:
    def __init__(self):
        self.llm = LLMClient()
    
    def generate_report(self, rules_results: dict, org_name: str) -> str:
        findings = rules_results.get("findings", [])
        metrics = rules_results.get("metrics", {})
        
        if not findings:
            return f"**Monitoreo completado.** No se encontraron anomalías o riesgos de alta prioridad en {org_name} durante esta ejecución."
            
        context = f"Organizacion: {org_name}\nHallazgos:\n"
        for f in findings:
            context += f"- {f}\n"
            
        if self.llm.is_available():
            system_prompt = """Eres un Oficial de Riesgo Financiero analizando operaciones o riesgos.
            Se te darán hallazgos crudos de un sistema. Construye un párrafo de resumen ejecutivo conciso destacando las conclusiones principales.
            No agregues introducciones largas, va directo al punto.
            """
            try:
                summary = self.llm.generate_summary(system_prompt, context)
                return summary
            except Exception as e:
                return self._fallback_summary(context)
        else:
            return self._fallback_summary(context)
            
    def _fallback_summary(self, context: str) -> str:
        return f"**Resumen Automatizado (Fallback sin IA):** Se han detectado irregularidades en el monitoreo actual que requieren revisión manual inmediata. Por favor revise los hallazgos detallados a continuación.\n\nContexto crudo procesado:\n{context}"
