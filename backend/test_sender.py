import requests
import random

nodos = [
    {"node": 1, "pm25_min": 10, "pm25_max":25, "temp_min": 20, "temp_max": 28},
    {"node": 2, "pm25_min": 20, "pm25_max":45, "temp_min": 21, "temp_max": 30},
    {"node": 3, "pm25_min": 3, "pm25_max": 12, "temp_min": 18, "temp_max": 25},
]

for n in nodos:
    datos = {
        "node": n["node"],
        "pm25": round(random.uniform(n["pm25_min"], n ["pm25_max"]), 1),
        "temp": round(random.uniform(n["temp_min"], n["temp_max"]), 1)
    }

    respuesta = requests.post("http://127.0.0.1:5000/data", json=datos)
    print(f"Nodo {n['node']} -> {datos} -> {respuesta.json()}")