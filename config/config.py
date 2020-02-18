import json
import os.path as path


def readJSON():

	file = "conf_conn.json"

	if path.exists(file):
		with open(file, 'r') as f:
			return json.load(f)
	else:
		host = input("Ingresa la dirección IP del servidor: ")
		username = input(
			"Ingresa tu nombre de usuario para la conexión: ")
		password = input("Ingresa tu contraseña: ")
		database = "bootcamp"

		data = {}
		data['conexion'] = []
		data['conexion'].append({
			'host': host,
			'database': database,
			'username': username,
			'password': password
		})

		with open('conf_conn.json', 'w') as f:
			json.dump(data, f, indent=4)