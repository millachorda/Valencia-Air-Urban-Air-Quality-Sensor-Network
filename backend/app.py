import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

import os
DB_PATH = os.path.join(os.path.dirname(__file__), "readings.db")

@app.route("/")
def home():
    return "The server works"

@app.route("/data", methods=["POST"])
def recieve_data():
    data = request.get_json()
    print("Data recieved:", data)

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO readings (timestamp, node, pm25, temp) VALUES (datetime('now'), ?, ?, ?)",
        (data["node"], data["pm25"], data["temp"])
    )
    conexion.commit()
    conexion.close()

    return jsonify({"status": "ok"})


@app.route("/readings")
def get_readings():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM readings")
    filas = cursor.fetchall()
    conexion.close()
    return jsonify(filas)

@app.route("/latest")
def get_latest():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM readings
        WHERE id IN (
            SELECT MAX(id) FROM readings GROUP BY node
            )
            ORDER BY node
        """)
    filas = cursor.fetchall()
    conexion.close()
    return jsonify(filas)

if __name__ == "__main__":
    app.run(debug=True, port=5000)