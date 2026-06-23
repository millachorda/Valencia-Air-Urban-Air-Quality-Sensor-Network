import sqlite3

conexion = sqlite3.connect("readings.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    node INTEGER,
    pm25 REAL,
    temp REAL
)
""")

conexion.commit()
conexion.close()
print("Database created")