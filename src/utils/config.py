import os
from dotenv import load_dotenv
import sqlite3
import sys

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class Config:
    """Configuración centralizada para la aplicación."""
    
    # Path a la base de datos SQLite
    DB_PATH = os.getenv("DB_PATH", "assessment_ia.db")
    
    # Proveedor LLM (Groq)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Límite global para consultas NLP
    QUERY_LIMIT = int(os.getenv("QUERY_LIMIT", "100"))
    
    # Modelo a usar en Groq
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3-70b-8192")

    @classmethod
    def check_db_exists(cls):
        """Verifica si la base de datos existe, si no, intenta generarla."""
        if not os.path.exists(cls.DB_PATH):
            print(f"Base de datos {cls.DB_PATH} no encontrada. Intentando crearla...")
            try:
                # Importamos el script original de generacion local
                import generar_base_datos
                generar_base_datos.main()
                print("Base de datos generada exitosamente.")
            except ImportError:
                print("Error: No se encontró el script 'generar_base_datos.py'.")
                sys.exit(1)
            except Exception as e:
                print(f"Error generando la BD: {e}")
                sys.exit(1)

# Asegurar existencia de BD al inicializar configuración
Config.check_db_exists()
