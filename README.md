# 🤖 Data Tools | AI Engineer Assessment

## 1. Descripción del Proyecto

Esta aplicación es una plataforma integral de análisis de datos y monitoreo diseñada para instituciones financieras o cooperativas con una arquitectura **Multi-Tenant** (Múltiples inquilinos u organizaciones). Resuelve el problema de democratizar el acceso a la información mediante un asistente de **Inteligencia Artificial (NL2SQL)** que permite a los usuarios hacer preguntas en lenguaje natural para obtener consultas de bases de datos seguras y reportes al instante.

El valor central de esta herramienta radica en la **privacidad y aislamiento de datos**: un analista solo puede consultar e interactuar matemáticamente con la información que pertenece estrictamente a su propia organización, previniendo fugas de información.

---

## 2. Arquitectura del Sistema

El proyecto tiene una estructura modular clara para facilitar su escalabilidad:

- **`auth`**: Gestiona las credenciales de los usuarios usando hashes seguros. Controla a qué organización pertenece la persona que inicia sesión.
- **`db`**: Centraliza la conexión y recuperación de datos directamente con la base de datos local SQLite, devolviendo DataFrames listos para su uso.
- **`llm`**: Construye las instrucciones (Prompts) para la inteligencia artificial y aplica los *Guardrails* (reglas de bloqueo) de seguridad en todo el código generado.
- **`nl_query`**: Traductor principal. Intercepta la pregunta escrita por la persona, se la pasa a la IA (o al módulo de respuestas pre-grabadas offline) y devuelve la consulta limpia.
- **`reports`**: Almacena las consultas estáticas frecuentemente utilizadas para los tableros generales, y dibuja los gráficos interactivos.
- **`monitoring`**: Audita todos los datos buscando comportamientos sospechosos basándose en reglas duras (ej. montos excesivos) y emite un veredicto de auditoría.

El flujo es unidireccional: **Usuario -> Interfaz (Streamlit) -> Guardrails/Auth -> Base de Datos -> Interfaz**.

---

## 3. Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje núcleo de todo el backend y frontend gracias a Streamlit.
- **Streamlit**: Framework que permite crear la interfaz gráfica visual (UI) moderna, componentes interactivos y control de estado reactivo.
- **SQLite**: Base de datos relacional ligera y local que no requiere configuración central ni servidores externos.
- **Pandas**: Motor de estructura de datos que procesa las tablas SQL rápidamente para mostrarlas y exportarlas.
- **Plotly**: Creador de gráficos interactivos, limpios y minimalistas listos para explorar en pantalla.
- **Groq (API)**: Proveedor de modelos de lenguaje (LLM) extremadamente rápidos como Llama 3 para orquestar la comprensión de lenguaje natural. *(Es opcional en esta app)*
- **python-dotenv**: Gestor de credenciales de entorno para asegurar que las variables sensibles no queden expuestas directamente en el código base.

---

## 4. Instalación

Para preparar el ambiente, solo debes clonar o copiar este código y correr los siguientes comandos en tu terminal.

1. Instalar dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
2. (Opcional) Renombrar el archivo de variables:
   ```bash
   mv .env.example .env
   ```
   Agrega tu clave de Groq en `.env` si quieres activar la IA, o déjalo sin clave para probar el modo nativo (Fallback offline).

---

## 5. Ejecución

Para iniciar el servidor local de la interfaz gráfica, corre:

```bash
streamlit run app.py
```
*Si la base de datos SQLite no existe, el sistema la creará e hidratará automáticamente en el primer inicio con datos sintéticos de muestra.*

---

## 6. Usuarios de Prueba (Demo)

Puedes iniciar sesión utilizando cualquiera de estos dos perfiles aislados. Cada uno verá **únicamente** los datos de su propia empresa:

| Organización | Usuario | Contraseña |
| --- | --- | --- |
| **Cooperativa del Valle** | `admin_valle` | `admin123` |
| **Cooperativa Antioqueña** | `admin_antioquia` | `admin123` |

---

## 7. Ejemplos de Consultas (NL2SQL)

Una vez logueado, dirígete a la pestaña **Consulta Inteligente** y experimenta introduciendo preguntas naturales como estas:

- *"¿Cuántos asociados tiene mi organización actualmente?"*
- *"Muéstrame las transacciones del último mes."*
- *"Dame un resumen del total de alertas abiertas."*
- *"¿Cuáles son los asociados con mayor actividad por monto?"*
- *"Lista todos mis usuarios inactivos."*

El LLM entenderá la métrica buscada y generará automáticamente el SQL necesario.

---

## 8. Funcionamiento del Sistema

- **Login Mantenido**: El estado de sesión (`st.session_state`) envuelve todo el uso del usuario protegiendo si está conectado o no en cada clic que haga.
- **Filtro `organization_id`**: Cada vez que se ejecuta una petición, el sistema inyecta nativamente un `WHERE asoc.id_organizacion = X` amarrándolo a la sesión actual del usuario ingresado. El usuario final **no puede hackear o cambiar este valor** desde la interfaz.
- **NL2SQL Activo**: Toma el input, se pasa junto al esquema de variables a Groq (IA), la IA devuelve texto SQL, pasa por el módulo de seguridad, se extraen los datos y se plasman en un DataFrame en UI.
- **Fallback Activo (Módulo sin IA)**: Si la API no responde, no hay internet, o no hay token en `.env`, el sistema no se rompe. Emplea Regex interno (Expresiones regulares) para capturar la "intención" del usuario (ej. si lee "transacciones mes") y envía un código SQL ya compilado seguro offline. 
- **Monitoreo Cíclico**: Analiza en bloque mediante SQLs en `rules.py` y dispara advertencias si un cliente tiene demasiadas alertas activadas o transacciones desorbitadas.

---

## 9. Seguridad Profunda

La seguridad fue construida pensando en mitigar ataques de inyección y sobreescrituras:
- **Solo Lectura Estricta**: El `sql_guardrails.py` bloquea por completo sentencias tipo `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`. Solo deja pasar `SELECT`.
- **Aislamiento Multi-Tenant Garantizado**: El Guardrail lee el texto del SQL y si no detecta explícitamente el fragmento que liga la búsqueda al `id_organizacion` correspondiente de la persona, trata de inyectarlo por fuerza y si no puede acoplarlo estructuradamente, anula y detiene toda la ejecución de consulta arrojando una excepción defensiva. Nada se ejecuta si no está acotado.

---

## 10. Decisiones de Diseño Principal

- **Por qué Streamlit**: Fomenta el rápido desarrollo (prototipado) en Python puro sin tener que perder tiempo valioso conectando React/Vue vía APIs. Soporta estado nativo y recude los puntos de falla técnicos.
- **Por qué SQLite**: No ocupa puertos, no exige a los directivos o jurados técnicos instalar motores de datos pasados como Postgres o MySQL para calificar este proyecto. Viene pre-compilado en el OS y en Python.
- **Por qué Groq API**: Ofrece tiempos de Inferencia (TTFT) excesivamente rápidos en modelos de Meta Llama, haciendo que la sensación de chat sea instantánea sin latencia dolorosa.
- **Por qué el Fallback**: En los entornos corporativos se puede perder conectividad saliente fácilmente. Una app "IA" que crashea si se cae la red externa no es resiliente. El "Fallback offline" avala la resiliencia productiva.

---

## 11. Futuras Escalabilidades y Mejoras (Roadmap)
- **Autenticación con JWT**: Desacoplar la vista en frontend conectándola vía Tokens JWT usando FastAPI por detrás, admitiendo autenticaciones corporativas reales mediante SSO u Oauth2.
- **Motor Multi-BD**: Expandir el conector `connection.py` utilizando herramientas potentes como SQLAlchemy para interactuar dinámicamente tanto con Postgres, SQL Server u Oracle BD.
- **Visualización Geométrica**: Integrar gráficos automáticos más nutridos para la pestaña del NL2SQL como diagramas de serie de tiempo dinámicos al instante.
- **RAG Extendido**: Que el sistema no solo hable con la BD SQL, sino que además indexe los contratos o los PDFs de alertas en base vectorial.
