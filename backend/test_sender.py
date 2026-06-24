import requests
import random

nodos = [
    {"node": 1, "pm_base": 18, "hum": 55},   
    {"node": 2, "pm_base": 32, "hum": 50},   
    {"node": 3, "pm_base": 7,  "hum": 75},  
]

for n in nodos:
    pm25 = round(random.uniform(n["pm_base"] - 5, n["pm_base"] + 5), 1)
    datos = {
        "node": n["node"],
        "pm1": round(pm25 * 0.7, 1),
        "pm25": pm25,
        "pm10": round(pm25 * 1.4, 1),
        "temp": round(random.uniform(18, 30), 1),
        "humidity": round(random.uniform(n["hum"] - 5, n["hum"] + 5), 1),
        "pressure": round(random.uniform(1010, 1020), 1),
        "co2": round(random.uniform(400, 800), 0),
        "voc": round(random.uniform(0, 200), 0)
    }
    respuesta = requests.post("http://127.0.0.1:5000/data", json=datos)
    print(f"Nodo {n['node']} -> PM2.5 {datos['pm25']}, Hum {datos['humidity']}% -> {respuesta.json()}")