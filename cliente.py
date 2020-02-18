import http.client#usar server3.0.py
import json
#complementos
import sys #para salir del promp, consola
import threading #hilo para ejecutar procesos al mismo tiempo en sugundo plano
import time #para pausar los procesos(esperar un tiempo)
import getIP # para obtener ip (nota: modulo local)
import formatTerminal# mostrar mensajes, usuario en tabla (nota:modulo local)
from  os import system # para limpiar la consola

class Cliente():
	def __init__(self, url='localhost', port=8000, espera=100):
		self.url = url
		self.port = port
		self.espera = espera

		self.miID = 0

		if self.miIPExists() == True:
			#self.conexion = http.client.HTTPConnection(url, port, espera)#tener una sola conexion no funciona (ya k hacen peticiones GET Y POST al mismo tiempo[por el hilo])
			hilo_getDatos = threading.Thread(target=self.hilo_consultarServer, daemon=True)# crear hilo que apunte a la funcion 'obtenerMensajes'
			hilo_updateStatus = threading.Thread(target=self.hilo_actualizarEstado, daemon=True)
			hilo_getDatos.start()
			hilo_updateStatus.start()

			while True:
				msg = input()
				if msg != 'exit':
					self.enviarMensaje(msg)
				else:
					sys.exit()
		else:
			print('Error: Tu IP no se encuentra en el Servidor')

	
	def enviarMensaje(self,msg,user=getIP.getIP()):
		conexion = http.client.HTTPConnection(self.url, self.port, self.espera)
		data = {user:msg}
		json_data = json.dumps(data) # convertir a json

		conexion.request('POST', '/', json_data, headers={'Content-type': 'application/json'})# enviar json
		#response = conexion.getresponse() # esperar respuesta
		#print(response.read())
		self.actualizaMensajes()#actualizar, para visualizar mi mensaje enviado
		conexion.close()

	def actualizaMensajes(self):#AL enviar, actualizar mi terminal -se ejecuta solo una vez al llamarlo
		mensajes = self.obtenerMensajes()#obtener lista de mensages
		usuarios = self.obtenerUsuarios()#obtener lista de usuarios
		system('clear')
		msgFormateada = formatTerminal.getFormatListMSG(mensajes, usuarios)#lista de mensajes, formateada(con colores, estructura)
		usrFormateada = formatTerminal.getFormatListUsers(usuarios)#lista de usuarios, formateada(con colores, estructura)
		print(formatTerminal.pintTableMSG(msgFormateada, usrFormateada))#crear tabla formateada(caracteres que simulan una tabla) e imprimirla

	#nuevos metodos
	def hilo_consultarServer(self):# se mantiene ejecutandose cada 4 segundos
		n_msg = 0 #para obtener numero de mensajes
		n_peticion = 0 #numero de peticiones al servidor(no es vital para el funcionamiento)

		while True:
			time.sleep(8)# esperar n segundos
			n_peticion += 1 # sumar 1 a (numero de peticiones)
			#print('Peticion:', n_peticion) # para saber n peticiones al servidor(no es vital para el funcionamiento)
			mensajes = self.obtenerMensajes()#obtener lista de mensages
			usuarios = self.obtenerUsuarios()#obtener lista de usuarios

			if len(mensajes) > n_msg: # [hay mas msg en server?] - si n. de msg en server (MAYOR A) n. de msg en memoria
				n_msg = len(mensajes)# actualizar n. msg
				system('clear')
				#print('N. peticiones:', n_peticion)#FIXME para saber n peticiones al servidor(no es vital para el funcionamiento)
				#print('Mensajes:', mensajes)
				msgFormateada = formatTerminal.getFormatListMSG(mensajes, usuarios)
				usrFormateada = formatTerminal.getFormatListUsers(usuarios)
				print(formatTerminal.pintTableMSG(msgFormateada, usrFormateada))
	
	def hilo_actualizarEstado(self):
		while True:
			time.sleep(8)# esperar n segundos
			conexion = http.client.HTTPConnection(self.url, self.port, self.espera)
			data = {'ID':self.miID}
			json_data = json.dumps(data) # convertir a json

			conexion.request('PUT', '/', json_data, headers={'Content-type': 'application/json'})# enviar json
			conexion.close()
			self.actualizaMensajes()
	
	def obtenerUsuarios(self):#retorna lista de usuarios
		conexion = http.client.HTTPConnection(self.url, self.port, self.espera)
		conexion.request('GET', '/users')# prepara peticion
		response = conexion.getresponse()# obtiene respuesta
		datos = response.read().decode('utf-8')# leer respuesta y convertir bytes a string
		usuarios = json.loads(datos)# convertir json(en string) a un formato de list
		conexion.close()
		return usuarios
	def obtenerMensajes(self):
		conexion = http.client.HTTPConnection(self.url, self.port, self.espera)
		conexion.request('GET', '/msg')# prepara peticion
		response = conexion.getresponse()# obtiene respuesta
		datos = response.read().decode('utf-8')# leer respuesta y convertir bytes a string
		mensajes = json.loads(datos)# convertir json(en string) a un formato de list
		conexion.close()
		return mensajes

	def miIPExists(self):
		myip = getIP.getIP()
		usuarios = self.obtenerUsuarios()
		for item in usuarios:
			if item[1] == myip:#la posicion 1, corresponde al campo IP
				self.miID = item[0]#la posicion 0, corresponde al campo ID
				return True
		return False

c = Cliente()