import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "proyecto.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS ordenes_compra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_orden TEXT NOT NULL,
        cliente TEXT NOT NULL,
        direccion TEXT NOT NULL,
        telefono TEXT NOT NULL,
        comuna TEXT NOT NULL,
        region TEXT NOT NULL,
        productos TEXT NOT NULL,
        precios TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'ingresada'
    );

    
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orden_id INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        iva REAL NOT NULL,
        total REAL NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (orden_id) REFERENCES ordenes_compra(id)
    );


    CREATE TABLE IF NOT EXISTS envios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factura_id INTEGER NOT NULL,
        estado_envio TEXT NOT NULL DEFAULT 'pendiente',
        fecha_envio TEXT,
        detalle TEXT,
        FOREIGN KEY (factura_id) REFERENCES facturas(id)
    );

    INSERT OR IGNORE INTO usuarios (username, password)
    VALUES ('admin','admin123');
    """

    with get_connection() as conn:
        conn.executescript(sql)
        conn.commit()
