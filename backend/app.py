import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

import os
DB_PATH = os.path.join(os.path.dirname(__file__), "readings.db")

@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

@app.route("/data", methods=["POST"])
def recieve_data():
    data = request.get_json()
    print("Data recieved:", data)

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO readings (timestamp, node, pm1, pm25, pm10, temp, humidity, pressure, co2, voc) VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (data["node"], data["pm1"], data["pm25"], data["pm10"], data["temp"], data["humidity"], data["pressure"], data["co2"], data["voc"])
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

@app.route("/readings/<int:node>")
def get_readings_by_node(node):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM readings WHERE node = ? ORDER BY id", (node,))
    filas = cursor.fetchall()
    conexion.close()
    return jsonify(filas)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
