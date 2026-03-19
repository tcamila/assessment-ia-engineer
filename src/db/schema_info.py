# Textual representation of the database schema for the LLM prompt.

SCHEMA_INFO = """
Esquema de Base de Datos Relacional (SQLite):

1. Tabla `organizaciones`
   - id_organizacion (INTEGER PRIMARY KEY)
   - nombre (TEXT)
   - nit (TEXT)
   - ciudad_sede (TEXT)
   - fecha_constitucion (TEXT)
   - activa (INTEGER)

2. Tabla `usuarios`
   - id_usuario (INTEGER PRIMARY KEY)
   - username (TEXT)
   - password_hash (TEXT)
   - nombre_completo (TEXT)
   - id_organizacion (INTEGER, FOREIGN KEY a organizaciones.id_organizacion)
   - rol (TEXT)
   - activo (INTEGER)

3. Tabla `analistas`
   - id_analista (INTEGER PRIMARY KEY)
   - nombre (TEXT)
   - apellido (TEXT)
   - email (TEXT)
   - especialidad (TEXT)
   - fecha_ingreso (TEXT)
   - activo (INTEGER)
   - id_organizacion (INTEGER, FOREIGN KEY a organizaciones.id_organizacion)

4. Tabla `asociados`
   - id_asociado (INTEGER PRIMARY KEY)
   - nombre (TEXT)
   - apellido (TEXT)
   - tipo_documento (TEXT)
   - numero_documento (TEXT)
   - email (TEXT)
   - telefono (TEXT)
   - ciudad (TEXT)
   - segmento (TEXT)
   - fecha_registro (TEXT)
   - id_analista_asignado (INTEGER, FOREIGN KEY a analistas.id_analista)
   - id_organizacion (INTEGER, FOREIGN KEY a organizaciones.id_organizacion)

5. Tabla `cuentas`
   - id_cuenta (INTEGER PRIMARY KEY)
   - id_asociado (INTEGER, FOREIGN KEY a asociados.id_asociado)
   - numero_cuenta (TEXT)
   - tipo_cuenta (TEXT)
   - saldo (REAL)
   - moneda (TEXT)
   - estado (TEXT)
   - fecha_apertura (TEXT)

6. Tabla `transacciones`
   - id_transaccion (INTEGER PRIMARY KEY)
   - id_cuenta (INTEGER, FOREIGN KEY a cuentas.id_cuenta)
   - tipo_transaccion (TEXT)
   - monto (REAL)
   - fecha_transaccion (TEXT)
   - canal (TEXT)
   - estado (TEXT)
   - descripcion (TEXT)

7. Tabla `alertas`
   - id_alerta (INTEGER PRIMARY KEY)
   - id_transaccion (INTEGER, FOREIGN KEY a transacciones.id_transaccion, nullable)
   - id_asociado (INTEGER, FOREIGN KEY a asociados.id_asociado)
   - id_analista_asignado (INTEGER, FOREIGN KEY a analistas.id_analista, nullable)
   - tipo_alerta (TEXT)
   - severidad (TEXT)
   - estado (TEXT)
   - descripcion (TEXT)
   - fecha_creacion (TEXT)
   - fecha_cierre (TEXT, nullable)

Relaciones clave:
- Un asociado pertenece a una sola organización (`id_organizacion`).
- Una cuenta pertenece a un solo asociado (`id_asociado`).
- Una transacción pertenece a una sola cuenta (`id_cuenta`) -> asociado -> organización.
- Una alerta pertenece a un asociado (`id_asociado`) -> organización.
"""
