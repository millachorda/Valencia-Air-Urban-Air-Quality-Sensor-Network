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
    pm1 REAL,
    pm25 REAL,
    pm10 REAL,
    temp REAL,
    humidity REAL,
    pressure REAL,
    co2 REAL,
    voc REAL
)
""")

conexion.commit()
conexion.close()