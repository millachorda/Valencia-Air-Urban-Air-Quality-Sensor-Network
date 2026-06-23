import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "readings.db")

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

cursor.execute( """
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    node INTEGER,
    pm25 REAL
    temp REAL
)
""")

conexion.commit()
conexion.close()