# 🤖 Data Tools | AI Engineer Assessment

## 1. Descripción del Proyecto
Esta plataforma es una herramienta integral de análisis de datos y monitoreo diseñada para instituciones financieras y cooperativas. Su objetivo principal es **democratizar el acceso a la información** permitiendo que perfiles no técnicos realicen consultas complejas mediante lenguaje natural, transformándolas automáticamente en código SQL (NL2SQL).

El valor central del sistema radica en su arquitectura **Multi-Tenant**, que garantiza un aislamiento estricto de los datos. Cada usuario interactúa exclusivamente con la información de su propia organización, integrando capas avanzadas de seguridad y auditoría automática para prevenir fugas de información o ejecuciones malintencionadas.

---

## 2. Arquitectura del Sistema
El proyecto sigue una estructura modular y escalable dentro del directorio `src/`:

- **`auth/`**: Gestiona la autenticación de usuarios y el control de acceso basado en organizaciones. Utiliza hashing SHA-256 para las credenciales.
- **`db/`**: Centraliza la lógica de conexión a la base de datos SQLite y la ejecución de consultas, retornando resultados en formatos optimizados (Pandas DataFrames).
- **`llm/`**: Orquestador de la Inteligencia Artificial. Contiene el constructor de prompts dinámicos y los **Guardrails** de seguridad SQL.
- **`monitoring/`**: Motor de auditoría que ejecuta reglas de negocio programadas para detectar anomalías (ej. montos inusuales o acumulación de alertas).
- **`nl_query/`**: Motor de traducción de lenguaje natural a SQL. Implementa una lógica dual: procesamiento vía IA (Groq/Llama 3) y un motor de **Fallback** local basado en heurísticas.
- **`reports/`**: Define las consultas estáticas para los tableros de control y la lógica de visualización interactiva.
- **`utils/`**: Configuraciones globales y utilidades transversales del sistema.

---

## 3. Funcionalidades Principales

### 🧠 Asistente NL2SQL (Natural Language to SQL)
Permite a los analistas realizar preguntas como *"¿Cuántos asociados tengo?"* o *"Lista las transacciones de más de 10 millones"*. El sistema traduce la intención a SQL puro, lo valida y lo ejecuta al instante.

### 🛡️ Guardrails de Seguridad
Cada consulta generada pasa por un riguroso proceso de validación:
- **Solo Lectura**: Bloqueo absoluto de sentencias `INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.
- **Inyección Automática de Contexto**: El sistema fuerza la cláusula `WHERE id_organizacion = ?` en todas las consultas para garantizar que los datos nunca se crucen entre inquilinos.

### 🚩 Monitoreo de Riesgos
Un panel dedicado a la detección automática de comportamientos sospechosos, como asociados con múltiples alertas abiertas o transacciones que superan umbrales críticos de riesgo financiero.

### 📊 Tableros Interactivos
Dashboard general con KPIs en tiempo real (Asociados, Transacciones, Alertas) y gráficos dinámicos (Plotly) para entender la distribución y severidad de la operación.

---

## 4. Stack Tecnológico
- **Python 3.10+**: Núcleo del backend y lógica de negocio.
- **Streamlit**: Framework para la interfaz de usuario reactiva y moderna.
- **SQLite**: Base de datos relacional ligera y autocontenida.
- **Pandas**: Procesamiento y manipulación de estructuras de datos.
- **Plotly**: Generación de visualizaciones interactivas y profesionales.
- **Groq API (Llama 3)**: Motor de inferencia ultra rápido para el procesamiento de lenguaje natural.
- **python-dotenv**: Gestión segura de variables de entorno.

---

## 5. Modelo de Datos
La base de datos se compone de las siguientes entidades principales:

1.  **`organizaciones`**: Cooperativas o entidades financieras inquilinas.
2.  **`usuarios`**: Personal administrativo con acceso a la plataforma.
3.  **`analistas`**: Responsables de la gestión de riesgos y asociados.
4.  **`asociados`**: Clientes finales de las organizaciones.
5.  **`cuentas`**: Productos financieros vinculados a los asociados.
6.  **`transacciones`**: Movimientos financieros (depósitos, retiros, transferencias).
7.  **`alertas`**: Registros de actividad sospechosa generados por el sistema.

---

## 6. Instalación y Configuración

### Requisitos Previos
- Python 3.10 o superior instalado.
- Una API Key de Groq (Opcional, para activar la funcionalidad completa de IA).

### Pasos
1. **Clonar el repositorio** y acceder a la carpeta raíz.
2. **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Configurar variables de entorno**:
    Crea un archivo `.env` basado en `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Edita `.env` y añade tu `GROQ_API_KEY`. Si no tienes una, la aplicación funcionará en modo **Resiliencia (Fallback)**.
4. **Inicializar la Base de Datos**:
    Ejecuta el script de hidratación para crear datos sintéticos:
    ```bash
    python generar_base_datos.py
    ```

---

## 7. Guía de Uso

### Ejecución de la App
Inicia el servidor de Streamlit:
```bash
streamlit run app.py
```

### Usuarios de Prueba (Demo)
El sistema cuenta con aislamiento total. Puedes probar el acceso con las siguientes credenciales:

| Organización | Usuario | Contraseña |
| :--- | :--- | :--- |
| **Cooperativa del Valle** | `admin_valle` | `admin123` |
| **Cooperativa Antioqueña** | `admin_antioquia` | `admin123` |
| **Cooperativa del Caribe** | `admin_caribe` | `admin123` |

### Ejemplos de Consultas NLP
Prueba las siguientes preguntas en la pestaña de **Consulta Inteligente**:
- *"¿Cuántos asociados tiene mi organización?"*
- *"Muéstrame las transacciones del último mes."*
- *"Lista todos mis analistas activos."*
- *"Dame un resumen de las alertas abiertas."*

---

## 8. Diseño de Seguridad y Multi-Tenant
La seguridad se ha implementado en múltiples capas:
1. **Sesión Segura**: El `organization_id` se vincula permanentemente a la sesión del usuario tras el login.
2. **Validación de Token de Consulta**: El motor NL2SQL verifica la existencia del filtro de organización antes de permitir la ejecución.
3. **Parámetros Seguros**: Se utilizan consultas parametrizadas (`?`) para evitar cualquier intento de inyección SQL manual.

---

## 9. Roadmap y Mejoras Futuras
- [ ] Implementación de autenticación vía **JWT** con un backend en FastAPI.
- [ ] Integración de **SQLAlchemy** para soportar motores como PostgreSQL o SQL Server.
- [ ] Módulo de **RAG (Retrieval-Augmented Generation)** para consultar manuales internos y normativas en PDF.
- [ ] Exportación avanzada de reportes en PDF y Excel con firmas digitales.
