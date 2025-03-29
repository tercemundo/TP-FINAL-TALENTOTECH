import sqlite3
import os

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    conn = sqlite3.connect('techlab.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con las tablas necesarias."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crear tabla de clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefono TEXT,
        direccion TEXT
    )
    ''')
    
    # Crear tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0
    )
    ''')
    
    # Crear tabla de pedidos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        estado TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
    ''')
    
    # Crear tabla de detalles de pedidos (relación muchos a muchos)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detalles_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
        FOREIGN KEY (producto_id) REFERENCES productos (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Base de datos inicializada correctamente.")