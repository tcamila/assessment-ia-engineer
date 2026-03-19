"""
============================================================
  ASSESSMENT TECNICO - INGENIERO DE INTELIGENCIA ARTIFICIAL
  Script de generacion de base de datos
============================================================

Este script genera una base de datos SQLite con datos sinteticos
para el ejercicio del assessment.

Instrucciones:
  1. Ejecute este script con Python 3.8+
  2. No se requieren dependencias externas (usa solo libreria estandar)
  3. Al finalizar se creara el archivo "assessment_ia.db" en el
     directorio actual

Uso:
  python generar_base_datos.py

"""

import sqlite3
import random
import os
import hashlib
from datetime import datetime, timedelta

# ------------------------------------------
# Configuracion
# ------------------------------------------
DB_NAME = "assessment_ia.db"
SEED = 42

random.seed(SEED)

# ------------------------------------------
# Datos base para generacion sintetica
# ------------------------------------------
NOMBRES = [
    "Carlos", "Maria", "Juan", "Ana", "Pedro", "Laura", "Andres", "Sofia",
    "Diego", "Camila", "Felipe", "Valentina", "Santiago", "Isabella", "Mateo",
    "Daniela", "Sebastian", "Mariana", "Nicolas", "Gabriela", "Alejandro",
    "Paula", "David", "Carolina", "Tomas", "Natalia", "Julian", "Catalina",
    "Emilio", "Lucia",
]

APELLIDOS = [
    "Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Hernandez",
    "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez",
    "Diaz", "Cruz", "Morales", "Reyes", "Gutierrez", "Ortiz", "Ramos",
    "Vargas", "Castro", "Romero", "Jimenez", "Ruiz", "Mendoza", "Medina",
    "Aguilar", "Herrera", "Guerrero",
]

CIUDADES = [
    "Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena",
    "Bucaramanga", "Pereira", "Manizales", "Santa Marta", "Ibague",
]

SEGMENTOS = ["Persona Natural", "Persona Juridica"]

TIPOS_CUENTA = ["Ahorros", "Corriente", "Nomina", "Inversion"]
ESTADOS_CUENTA = ["Activa", "Inactiva", "Bloqueada"]
MONEDAS = ["COP", "USD"]

TIPOS_TRANSACCION = [
    "Transferencia Enviada",
    "Transferencia Recibida",
    "Pago de Servicios",
    "Retiro ATM",
    "Compra en Comercio",
    "Deposito",
    "Pago de Nomina",
    "Pago de Impuestos",
]
CANALES = ["App Movil", "Sucursal", "Portal Web", "ATM", "Corresponsal"]
ESTADOS_TRANSACCION = ["Completada", "Pendiente", "Rechazada", "Reversada"]

TIPOS_ALERTA = [
    "Transaccion inusual",
    "Monto elevado",
    "Multiples transacciones en corto tiempo",
    "Transaccion internacional",
    "Cuenta nueva con alto volumen",
    "Cambio de datos de contacto",
]
NIVELES_SEVERIDAD = ["Baja", "Media", "Alta", "Critica"]
ESTADOS_ALERTA = ["Abierta", "En revision", "Cerrada", "Escalada"]

ESPECIALIDADES_ANALISTA = [
    "Monitoreo Transaccional",
    "Analisis de Riesgo",
    "Prevencion de Fraude",
    "Cumplimiento Normativo",
    "Analisis de Datos",
]

# Organizaciones (cooperativas)
ORGANIZACIONES = [
    {
        "nombre": "Cooperativa del Valle",
        "nit": "900.123.456-1",
        "ciudad_sede": "Cali",
        "fecha_constitucion": "2005-03-15",
    },
    {
        "nombre": "Cooperativa Antioquena",
        "nit": "900.789.012-3",
        "ciudad_sede": "Medellin",
        "fecha_constitucion": "1998-07-22",
    },
    {
        "nombre": "Cooperativa del Caribe",
        "nit": "900.345.678-5",
        "ciudad_sede": "Barranquilla",
        "fecha_constitucion": "2010-11-05",
    },
]


# ------------------------------------------
# Funciones auxiliares
# ------------------------------------------
def fecha_aleatoria(inicio: datetime, fin: datetime) -> str:
    delta = fin - inicio
    dias = random.randint(0, delta.days)
    segundos = random.randint(0, 86399)
    fecha = inicio + timedelta(days=dias, seconds=segundos)
    return fecha.strftime("%Y-%m-%d %H:%M:%S")


def generar_email(nombre: str, apellido: str) -> str:
    dominio = random.choice(["correo.com", "mail.co", "empresa.com.co", "email.com"])
    sufijo = random.randint(1, 999)
    return f"{nombre.lower()}.{apellido.lower()}{sufijo}@{dominio}"


def generar_telefono() -> str:
    return f"+57 3{random.randint(10, 29)} {random.randint(100, 999)} {random.randint(1000, 9999)}"


def generar_numero_cuenta() -> str:
    return f"{random.randint(1000, 9999)}-{random.randint(100000, 999999)}-{random.randint(10, 99)}"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ------------------------------------------
# Creacion de la base de datos
# ------------------------------------------
def crear_base_datos():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"  Base de datos anterior '{DB_NAME}' eliminada.")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # -- Tabla: organizaciones --
    cursor.execute("""
        CREATE TABLE organizaciones (
            id_organizacion     INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre              TEXT NOT NULL,
            nit                 TEXT NOT NULL UNIQUE,
            ciudad_sede         TEXT NOT NULL,
            fecha_constitucion  TEXT NOT NULL,
            activa              INTEGER NOT NULL DEFAULT 1
        );
    """)

    # -- Tabla: usuarios (login) --
    cursor.execute("""
        CREATE TABLE usuarios (
            id_usuario          INTEGER PRIMARY KEY AUTOINCREMENT,
            username            TEXT NOT NULL UNIQUE,
            password_hash       TEXT NOT NULL,
            nombre_completo     TEXT NOT NULL,
            id_organizacion     INTEGER NOT NULL,
            rol                 TEXT NOT NULL DEFAULT 'consulta',
            activo              INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (id_organizacion) REFERENCES organizaciones(id_organizacion)
        );
    """)

    # -- Tabla: analistas --
    cursor.execute("""
        CREATE TABLE analistas (
            id_analista     INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre          TEXT NOT NULL,
            apellido        TEXT NOT NULL,
            email           TEXT NOT NULL,
            especialidad    TEXT NOT NULL,
            fecha_ingreso   TEXT NOT NULL,
            activo          INTEGER NOT NULL DEFAULT 1,
            id_organizacion INTEGER NOT NULL,
            FOREIGN KEY (id_organizacion) REFERENCES organizaciones(id_organizacion)
        );
    """)

    # -- Tabla: asociados (antes clientes) --
    cursor.execute("""
        CREATE TABLE asociados (
            id_asociado         INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre              TEXT NOT NULL,
            apellido            TEXT NOT NULL,
            tipo_documento      TEXT NOT NULL,
            numero_documento    TEXT NOT NULL UNIQUE,
            email               TEXT,
            telefono            TEXT,
            ciudad              TEXT NOT NULL,
            segmento            TEXT NOT NULL,
            fecha_registro      TEXT NOT NULL,
            id_analista_asignado INTEGER,
            id_organizacion     INTEGER NOT NULL,
            FOREIGN KEY (id_analista_asignado) REFERENCES analistas(id_analista),
            FOREIGN KEY (id_organizacion) REFERENCES organizaciones(id_organizacion)
        );
    """)

    # -- Tabla: cuentas --
    cursor.execute("""
        CREATE TABLE cuentas (
            id_cuenta       INTEGER PRIMARY KEY AUTOINCREMENT,
            id_asociado     INTEGER NOT NULL,
            numero_cuenta   TEXT NOT NULL UNIQUE,
            tipo_cuenta     TEXT NOT NULL,
            saldo           REAL NOT NULL DEFAULT 0,
            moneda          TEXT NOT NULL DEFAULT 'COP',
            estado          TEXT NOT NULL DEFAULT 'Activa',
            fecha_apertura  TEXT NOT NULL,
            FOREIGN KEY (id_asociado) REFERENCES asociados(id_asociado)
        );
    """)

    # -- Tabla: transacciones --
    cursor.execute("""
        CREATE TABLE transacciones (
            id_transaccion      INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cuenta           INTEGER NOT NULL,
            tipo_transaccion    TEXT NOT NULL,
            monto               REAL NOT NULL,
            fecha_transaccion   TEXT NOT NULL,
            canal               TEXT NOT NULL,
            estado              TEXT NOT NULL DEFAULT 'Completada',
            descripcion         TEXT,
            FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta)
        );
    """)

    # -- Tabla: alertas --
    cursor.execute("""
        CREATE TABLE alertas (
            id_alerta           INTEGER PRIMARY KEY AUTOINCREMENT,
            id_transaccion      INTEGER,
            id_asociado         INTEGER NOT NULL,
            id_analista_asignado INTEGER,
            tipo_alerta         TEXT NOT NULL,
            severidad           TEXT NOT NULL,
            estado              TEXT NOT NULL DEFAULT 'Abierta',
            descripcion         TEXT,
            fecha_creacion      TEXT NOT NULL,
            fecha_cierre        TEXT,
            FOREIGN KEY (id_transaccion) REFERENCES transacciones(id_transaccion),
            FOREIGN KEY (id_asociado) REFERENCES asociados(id_asociado),
            FOREIGN KEY (id_analista_asignado) REFERENCES analistas(id_analista)
        );
    """)

    conn.commit()
    return conn, cursor


# ------------------------------------------
# Insercion de datos sinteticos
# ------------------------------------------
def insertar_organizaciones(cursor):
    ids = []
    for org in ORGANIZACIONES:
        cursor.execute(
            "INSERT INTO organizaciones (nombre, nit, ciudad_sede, fecha_constitucion, activa) "
            "VALUES (?, ?, ?, ?, 1)",
            (org["nombre"], org["nit"], org["ciudad_sede"], org["fecha_constitucion"]),
        )
        ids.append(cursor.lastrowid)
    return ids


def insertar_usuarios(cursor, org_ids):
    """Crea usuarios de prueba para cada organizacion."""
    usuarios = []
    datos = [
        # org 1 - Cooperativa del Valle
        ("admin_valle", "admin123", "Administrador Valle", org_ids[0], "admin"),
        ("analista_valle", "analista123", "Analista Valle", org_ids[0], "analista"),
        ("consulta_valle", "consulta123", "Consultor Valle", org_ids[0], "consulta"),
        # org 2 - Cooperativa Antioquena
        ("admin_antioquia", "admin123", "Administrador Antioquia", org_ids[1], "admin"),
        ("analista_antioquia", "analista123", "Analista Antioquia", org_ids[1], "analista"),
        ("consulta_antioquia", "consulta123", "Consultor Antioquia", org_ids[1], "consulta"),
        # org 3 - Cooperativa del Caribe
        ("admin_caribe", "admin123", "Administrador Caribe", org_ids[2], "admin"),
        ("analista_caribe", "analista123", "Analista Caribe", org_ids[2], "analista"),
        ("consulta_caribe", "consulta123", "Consultor Caribe", org_ids[2], "consulta"),
    ]
    for username, password, nombre, id_org, rol in datos:
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, nombre_completo, id_organizacion, rol, activo) "
            "VALUES (?, ?, ?, ?, ?, 1)",
            (username, hash_password(password), nombre, id_org, rol),
        )
        usuarios.append(cursor.lastrowid)
    return usuarios


def insertar_analistas(cursor, org_ids, cantidad_por_org=8):
    analistas = []  # lista de (id_analista, id_organizacion)
    nombres_usados = set()
    for id_org in org_ids:
        for _ in range(cantidad_por_org):
            while True:
                nombre = random.choice(NOMBRES)
                apellido = random.choice(APELLIDOS)
                if (nombre, apellido) not in nombres_usados:
                    nombres_usados.add((nombre, apellido))
                    break
            email = generar_email(nombre, apellido)
            especialidad = random.choice(ESPECIALIDADES_ANALISTA)
            fecha_ingreso = fecha_aleatoria(datetime(2020, 1, 1), datetime(2024, 12, 31))
            activo = 1 if random.random() > 0.15 else 0

            cursor.execute(
                "INSERT INTO analistas (nombre, apellido, email, especialidad, fecha_ingreso, activo, id_organizacion) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nombre, apellido, email, especialidad, fecha_ingreso, activo, id_org),
            )
            analistas.append((cursor.lastrowid, id_org))
    return analistas


def insertar_asociados(cursor, analistas, org_ids, cantidad_por_org=170):
    asociados = []  # lista de (id_asociado, id_organizacion)
    docs_usados = set()
    for id_org in org_ids:
        analistas_org = [a[0] for a in analistas if a[1] == id_org]
        for _ in range(cantidad_por_org):
            nombre = random.choice(NOMBRES)
            apellido = random.choice(APELLIDOS)
            tipo_doc = random.choice(["CC", "CE", "NIT", "Pasaporte"])
            while True:
                num_doc = str(random.randint(10000000, 9999999999))
                if num_doc not in docs_usados:
                    docs_usados.add(num_doc)
                    break
            email = generar_email(nombre, apellido)
            telefono = generar_telefono()
            ciudad = random.choice(CIUDADES)
            segmento = random.choices(SEGMENTOS, weights=[75, 25])[0]
            fecha_registro = fecha_aleatoria(datetime(2019, 1, 1), datetime(2025, 12, 31))
            id_analista = random.choice(analistas_org) if random.random() > 0.3 else None

            cursor.execute(
                "INSERT INTO asociados "
                "(nombre, apellido, tipo_documento, numero_documento, email, telefono, "
                "ciudad, segmento, fecha_registro, id_analista_asignado, id_organizacion) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (nombre, apellido, tipo_doc, num_doc, email, telefono,
                 ciudad, segmento, fecha_registro, id_analista, id_org),
            )
            asociados.append((cursor.lastrowid, id_org))
    return asociados


def insertar_cuentas(cursor, asociados):
    cuentas = []  # lista de (id_cuenta, id_organizacion)
    for id_asociado, id_org in asociados:
        num_cuentas = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
        for _ in range(num_cuentas):
            numero = generar_numero_cuenta()
            tipo = random.choice(TIPOS_CUENTA)
            moneda = random.choices(MONEDAS, weights=[90, 10])[0]
            saldo = round(
                random.uniform(50000, 150000000) if moneda == "COP" else random.uniform(100, 50000), 2
            )
            estado = random.choices(ESTADOS_CUENTA, weights=[80, 12, 8])[0]
            fecha_apertura = fecha_aleatoria(datetime(2019, 1, 1), datetime(2025, 12, 31))

            cursor.execute(
                "INSERT INTO cuentas "
                "(id_asociado, numero_cuenta, tipo_cuenta, saldo, moneda, estado, fecha_apertura) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (id_asociado, numero, tipo, saldo, moneda, estado, fecha_apertura),
            )
            cuentas.append((cursor.lastrowid, id_org))
    return cuentas


def insertar_transacciones(cursor, cuentas, objetivo_minimo=20000):
    transacciones = []  # lista de (id_transaccion, id_organizacion)
    base_por_cuenta = max(5, objetivo_minimo // len(cuentas))
    for id_cuenta, id_org in cuentas:
        num_transacciones = random.randint(base_por_cuenta, base_por_cuenta + 15)
        for _ in range(num_transacciones):
            tipo = random.choice(TIPOS_TRANSACCION)
            monto = round(random.uniform(10000, 25000000), 2)
            fecha = fecha_aleatoria(datetime(2024, 1, 1), datetime(2026, 2, 28))
            canal = random.choice(CANALES)
            estado = random.choices(ESTADOS_TRANSACCION, weights=[80, 10, 7, 3])[0]
            descripcion = f"{tipo} por ${monto:,.2f} via {canal}"

            cursor.execute(
                "INSERT INTO transacciones "
                "(id_cuenta, tipo_transaccion, monto, fecha_transaccion, canal, estado, descripcion) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (id_cuenta, tipo, monto, fecha, canal, estado, descripcion),
            )
            transacciones.append((cursor.lastrowid, id_org))
    return transacciones


def insertar_alertas(cursor, transacciones, asociados, analistas, cantidad_por_org=270):
    cursor.execute("SELECT id_transaccion, id_cuenta FROM transacciones")
    trans_cuenta = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT id_cuenta, id_asociado FROM cuentas")
    cuenta_asociado = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT id_asociado, id_organizacion FROM asociados")
    asociado_org = {row[0]: row[1] for row in cursor.fetchall()}

    org_ids = list(set(a[1] for a in asociados))

    for id_org in org_ids:
        trans_org = [t[0] for t in transacciones if t[1] == id_org]
        asoc_org = [a[0] for a in asociados if a[1] == id_org]
        anal_org = [a[0] for a in analistas if a[1] == id_org]

        for _ in range(cantidad_por_org):
            id_transaccion = random.choice(trans_org) if random.random() > 0.2 else None

            if id_transaccion and id_transaccion in trans_cuenta:
                id_cuenta = trans_cuenta[id_transaccion]
                id_asociado = cuenta_asociado.get(id_cuenta, random.choice(asoc_org))
            else:
                id_asociado = random.choice(asoc_org)

            id_analista = random.choice(anal_org) if random.random() > 0.25 else None
            tipo_alerta = random.choice(TIPOS_ALERTA)
            severidad = random.choices(NIVELES_SEVERIDAD, weights=[30, 35, 25, 10])[0]
            estado = random.choices(ESTADOS_ALERTA, weights=[30, 25, 35, 10])[0]
            descripcion = f"Alerta: {tipo_alerta} - Severidad {severidad}"
            fecha_creacion = fecha_aleatoria(datetime(2024, 6, 1), datetime(2026, 2, 28))
            fecha_cierre = (
                fecha_aleatoria(
                    datetime.strptime(fecha_creacion, "%Y-%m-%d %H:%M:%S"),
                    datetime(2026, 3, 5),
                )
                if estado == "Cerrada"
                else None
            )

            cursor.execute(
                "INSERT INTO alertas "
                "(id_transaccion, id_asociado, id_analista_asignado, tipo_alerta, "
                "severidad, estado, descripcion, fecha_creacion, fecha_cierre) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (id_transaccion, id_asociado, id_analista, tipo_alerta,
                 severidad, estado, descripcion, fecha_creacion, fecha_cierre),
            )


# ------------------------------------------
# Ejecucion principal
# ------------------------------------------
def main():
    print("=" * 60)
    print("  GENERADOR DE BASE DE DATOS - ASSESSMENT IA")
    print("=" * 60)
    print()

    print("[1/8] Creando base de datos y tablas...")
    conn, cursor = crear_base_datos()

    print("[2/8] Insertando organizaciones...")
    org_ids = insertar_organizaciones(cursor)

    print("[3/8] Insertando usuarios...")
    insertar_usuarios(cursor, org_ids)

    print("[4/8] Insertando analistas...")
    analistas = insertar_analistas(cursor, org_ids, cantidad_por_org=8)

    print("[5/8] Insertando asociados...")
    asociados = insertar_asociados(cursor, analistas, org_ids, cantidad_por_org=170)

    print("[6/8] Insertando cuentas...")
    cuentas = insertar_cuentas(cursor, asociados)

    print("[7/8] Insertando transacciones...")
    transacciones = insertar_transacciones(cursor, cuentas)

    print("[8/8] Insertando alertas...")
    insertar_alertas(cursor, transacciones, asociados, analistas, cantidad_por_org=270)

    conn.commit()

    # -- Resumen --
    print()
    print("-" * 60)
    print("  RESUMEN DE DATOS GENERADOS")
    print("-" * 60)

    tablas = ["organizaciones", "usuarios", "analistas", "asociados", "cuentas", "transacciones", "alertas"]
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        print(f"  {tabla:<20} {count:>6} registros")

    print("-" * 60)
    print()

    # -- Datos por organizacion --
    print("  DATOS POR ORGANIZACION:")
    for id_org, org in zip(org_ids, ORGANIZACIONES):
        cursor.execute("SELECT COUNT(*) FROM asociados WHERE id_organizacion = ?", (id_org,))
        n_asoc = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM transacciones t "
            "JOIN cuentas c ON t.id_cuenta = c.id_cuenta "
            "JOIN asociados a ON c.id_asociado = a.id_asociado "
            "WHERE a.id_organizacion = ?", (id_org,)
        )
        n_trans = cursor.fetchone()[0]
        print(f"  {org['nombre']:<30} {n_asoc:>4} asociados, {n_trans:>6} transacciones")

    print()
    print("  ESQUEMA DE RELACIONES:")
    print()
    print("  organizaciones ---+--> usuarios")
    print("                    +--> analistas ---+")
    print("                    |                 |")
    print("                    +--> asociados <--+")
    print("                         |")
    print("                         +--> cuentas --> transacciones")
    print("                         |                      |")
    print("                         +---- alertas <--------+")
    print()

    # -- Credenciales --
    print("  USUARIOS DE PRUEBA:")
    print("  " + "-" * 50)
    print(f"  {'Usuario':<25} {'Clave':<15} {'Org'}")
    print("  " + "-" * 50)
    cursor.execute(
        "SELECT u.username, u.rol, o.nombre "
        "FROM usuarios u JOIN organizaciones o ON u.id_organizacion = o.id_organizacion "
        "ORDER BY u.id_organizacion, u.rol"
    )
    passwords = {"admin": "admin123", "analista": "analista123", "consulta": "consulta123"}
    for row in cursor.fetchall():
        pwd = passwords.get(row[1], "???")
        print(f"  {row[0]:<25} {pwd:<15} {row[2]}")
    print("  " + "-" * 50)
    print()

    print(f"  Base de datos generada: {os.path.abspath(DB_NAME)}")
    print()
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    main()
