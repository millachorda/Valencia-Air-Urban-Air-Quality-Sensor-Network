import requests

datos = {"node": 1, "pm25": 12, "temp": 22.5}
respuesta = requests.post("http://127.0.0.1:5000/data", json=datos)
print("Response from the server:", respuesta.json())