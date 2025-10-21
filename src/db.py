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

    INSERT OR IGNORE INTO usuarios (username, password) VALUES ('admin','admin123');
    """
    with get_connection() as conn:
        conn.executescript(sql)
        conn.commit()
