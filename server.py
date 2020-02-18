from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import json
#
from config import bd#este paquete es local, sirve para conexion a la BD
import time #para usar el sleep (detener el proceso por un tiempo)
import threading #hilo para ejecutar procesos al mismo tiempo en sugundo plano(actualizar la lista de usuarios)
import datetime#necesario para la conversion de datetime.datetime (de la BD) a string

mensajes = []#lista para guardar los mensajes
usuarios = []#lista para guardar los usuarios de la BD

def actualizaLista():
	global usuarios#se usa global para referenciar a la variable que esta fuera de esta funcion
	while True:
		time.sleep(8)#cada 8 segundos,consultar a la BD
		usuarios = bd.selectUsers()#funcion de la BD(retorna lista a partir de la consulta)
		print(usuarios)

def myconverter(o):#Un convertidor, para  que el datetime.datetime pueda parsearse a JSON
    if isinstance(o, datetime.datetime):
        return o.__str__()#se retorna el datetime en formato de string

#---------------------------------------------------------------------
class HandleRequests(BaseHTTPRequestHandler):
	def _set_headers(self, tipo = 'text/plain'):
		self.send_response(200)
		self.send_header('Content-type', tipo)
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', 'http://localhost:8000')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
		self.end_headers()

	def _set_response(self, response):
		if isinstance(response, bytes):#si el parametro es binario
			self.wfile.write(response)
		else:#si no se convierte a bytes
			self.wfile.write(bytes(response, 'utf-8'))

	def do_GET(self):
		if self.path == '/':
			self._set_headers('text/html')
			f = open('html/index.html')
			self._set_response(f.read())
			f.close()

		if self.path.endswith(".js"):
			self._set_headers('application/javascript')
			print('curdir:{}, sep{}'.format(curdir, sep))
			f = open('html'+self.path)
			self.wfile.write(f.read().encode('utf-8'))
			f.close()
		if self.path == '/msg':
			self._set_headers()
			mensajes_binario = str(json.dumps(mensajes, default=myconverter)).encode('utf-8')#convertir list-msg a bytes
			self.wfile.write(mensajes_binario)#respuesta para el cliente - retorna mensajes
		if self.path == '/users':
			self._set_headers()
			usuarios_binario = str(json.dumps(usuarios, default=myconverter)).encode('utf-8')#convertir list-msg a bytes, pero antes las fechas datetime se convierten a string
			self.wfile.write(usuarios_binario)#respuesta para el cliente - retorna usuarios
		
	def do_POST(self):
		self._set_headers()
		content_len = int(self.headers['Content-Length'])#obtener longitud de dato recibido
		datos = self.rfile.read(content_len)#leer datos, los datos recibidos son binarios
		datos_string = datos.decode('utf-8')#convertir datos binarios a 
		diccMSG = json.loads(datos_string)#el dato recibido es un diccionario: {'ip':'mensaje'}
		diccMSG['tiempo'] = datetime.datetime.now()#crear un nuevo item al diccionario de msg, el tiempo, {'ip':'mensaje', 'timpo':'fecha y hora'}
		mensajes.append(diccMSG)#agregar dato recibido a la list

		print('Datos[POST]:', datos_string)#--para comprobar (no es necesario)
		print('Mensajes[]:', str(mensajes))#--para comprobar (no es necesario)

		respuesta_binaria = "Datos[POST] recibido:{}".format(datos_string).encode('utf-8')
		self.wfile.write(respuesta_binaria)#respuesta para el cliente

	def do_PUT(self):
		self._set_headers()
		content_len = int(self.headers['Content-Length'])#obtener longitud de dato recibido
		datosBin = self.rfile.read(content_len)#leer datos, los datos recibidos son binarios
		datos_string = datosBin.decode('utf-8')#convertir datos binarios a string
		data = json.loads(datos_string)#el dato recibido del cliente fue un diccionario {clave:valor}

		miID = data['ID']
		
		bd.updateLastSeen(miID)

#---------------------------------------------------------------------
hilo_getUsers = threading.Thread(target=actualizaLista)#preparar hilo para actualizar la lista de usuarios(consultar a la BD cada 8 segundos)
hilo_getUsers.daemon = True
hilo_getUsers.start()#Ejecutar hilo(proceso en segundo plano)


host = '0.0.0.0'# Si se pone 127.0.0.1, funciona solo en local, 0.0.0.0 para ser accedido desde otro cliente remoto(ip diferente)
port = 8000
HTTPServer((host, port), HandleRequests).serve_forever()




#"0.0.0.0" means it is listening on all available interfaces.
#INFO encontrado en : https://stackoverflow.com/questions/55820681/how-do-i-access-a-python-http-server-from-a-remote-connection
#MAS INFO:localhost or 127.0.0.1, you could only connect to it from the local machine, because 127.0.0.1 belongs to the loopback device. But with 0.0.0.0, the server's binding to lo, eth0 and any other network devices you might have. de : https://askubuntu.com/questions/620459/python-simplehttpserver-woking-only-with-local-machine