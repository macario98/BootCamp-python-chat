def getFormatListMSG(listmsg, listUser):#devuelve una lista de mensajes (con formato)
	
	formatoListaMsg = []#para guardar los msg
	# for diccionario in listmsg:
	# 	for key in diccionario:
	# 		formatoListaMsg.append( '(\x1b[7;30;42m{}\x1b[0m): {}'.format(key, diccionario[key]) )
	# return formatoListaMsg
	for msg in listmsg:
		for key in msg:
			for user in listUser:
				if key == user[1]:
					formatoListaMsg.append( '({}-\x1b[7;30;42m{}\x1b[0m): {}'.format(user[2], user[1], msg[key]) )
	return formatoListaMsg

#-------------------------------------------------------------------------------------------------------------------------------------------------------
def getFormatListUsers(listUser, miTiempo = None):#recibo tiempo (desde la funcion TestUsers() ), solo para hacer pruebas locales
	from datetime import date, datetime, timedelta

	if miTiempo == None:#Si no recibo miTiempo(Ultima conexion)
		miTiempo = datetime.now()#Crear variable


	filas = [] #donde se guardaran las filas para la tabla
	for item in listUser: #recorrer items de la lista de usuarios (nota: un item devuelve una TUPLA)
		idu,ip,user,stringTiempo = item #es posible que de erro, esto depende del numero de columnas de la bd
		contactoDatetime = datetime.strptime(stringTiempo, '%Y-%m-%d %H:%M:%S.%f') # convertir la fecha(string) a una fecha de tipo(datetime), el segundo parametro es el formato de fecha (YEARM-MONTH-DAY Hour:Minute:Seconds.etc..)
		diferencia = miTiempo - contactoDatetime

		#Info para colores en terminal: https://www.pythond.com/20055/imprimir-en-terminal-con-colores.html
		if diferencia.total_seconds() > 10:#cuando el tiempo del contacto esta muy adelantado, puede ser por que su reloj esta adelantado
			filas.append("\x1b[0;37;41m{:<18} {:<28}  OFFLINE                \x1b[0m".format(user, stringTiempo) )#Ese item o tupla(formado for dos elementos'ip,fecha') se pasa como argumento a las dos columnas (18 espacios, 26 espacios) -Este metodo es DESEMPAQUETADO DE ARGUMENTOS
		else:
			if diferencia.total_seconds() < -10:
				filas.append("\x1b[0;30;43m{:<18} {:<28}  ERROR DE SINCRONIZACION\x1b[0m".format(user, stringTiempo) )#Ese item o tupla(formado for dos elementos'ip,fecha') se pasa como argumento a las dos columnas (18 espacios, 26 espacios) -Este metodo es DESEMPAQUETADO DE ARGUMENTOS
			else:
				filas.append("\x1b[0;37;44m{:<18} {:<28}  ONLINE                 \x1b[0m".format(user, stringTiempo) )#Ese item o tupla(formado for dos elementos'ip,fecha') se pasa como argumento a las dos columnas (18 espacios, 26 espacios) -Este metodo es DESEMPAQUETADO DE ARGUMENTOS

	return filas
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def pintTableMSG(listmsg = [], listUser = []):
	mayor = 0
	lenListMSG = len(listmsg)
	lenListUsers = len(listUser)

	formato = """\
+----------------------------------------------------------------------------------------+--------------------------------------------------------------------------+
|                                 MESSAGES                                               |    IP ADDRESS    .       Last Seen             .        Status           |
|----------------------------------------------------------------------------------------+--------------------------------------------------------------------------|
{}
+----------------------------------------------------------------------------------------+--------------------------------------------------------------------------+\
"""
	filas = []


	if lenListMSG <= lenListUsers:#saber si hay mas mensajes o mas lista de usuario
		mayor = lenListUsers
	else:
		mayor = lenListMSG

	for i in range(0,mayor):
		fila = ''
		if(lenListMSG > i):
			#print('MSG:', listmsg[i])
			fila = '| {:<100} '.format(listmsg[i])
		else:
			fila = '|. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . '
		if(lenListUsers > i):
			#print('USERS:', listUser[i])
			fila += '| {:<84} |'.format(listUser[i])
		else:
			fila += '| . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|'
		#print('Estor en i:',i)
		filas.append(fila)
	#print('Filas')

	tabla  = formato.format('\n'.join(filas))
	return tabla


#TESTs
def testGetListMSG():
	listmsg = [{'192.168.0.137': 'hello'}, {'192.168.0.151': 'Hellodsfsdgfdsgdf'}, {'192.168.0.205': 'HELLO'}, {'192.168.0.213': 'estoy en el bootcamp eleveminds'}, {'192.168.0.146': 'HELLO'}]
	r = getFormatListMSG(listmsg)
	print( r )
	return r
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def testGetListUsers():
	from datetime import date, datetime, timedelta #timedelta sirve para hacer operaciones(sumar, restar, etc.) con sugundos, minutos, etc a un datetime

	#listUser = [(45, '192.168.0.137', 'Macario', '2020, 2, 11, 16, 41, 3, 640753'), (46, '192.168.0.139', 'Carlos Daniel', '2020, 2, 10, 17, 13, 34, 458843')] #este formato es el mismo que devuelva una consulta hecha a la BD
	listUser = []
	
	miTiempo = datetime.now() #obtener la fecha y hora de mi conexion

	#Nota: La tolerancia es de 8 segundos, un usuario que este dentro del rango (-8 a 8 segundos) se tomara como ONLINE
	#Mi tiempo es mayor - mi contacto es menor:
	listUser.append( ('02','192,168.123.220','Lulu', str( miTiempo - timedelta(seconds=10.0) ))) # crear usuario con 10 segundos menos que yo - OFFLINE
	listUser.append( ('03','192,168.123.205','Bod', str( miTiempo - timedelta(seconds=8.0) ))) # crear usuario con 8 segundos menos que yo - ONLINE
	listUser.append( ('04','192,168.123.117','Ros', str( miTiempo - timedelta(seconds=5.0) ))) # crear usuario con 5 segundos menos que yo - ONLINE
	#Mi tiempo y contacto igual:
	listUser.append( ('05','192,168.123.106','Patric', str( miTiempo ))) # crear usuario con mismo tiempo que yo - ONLINE
	#Mi tiempo es Menor - Mi contacto es Mayor:
	listUser.append( ('06','192,168.123.186','john', str( miTiempo + timedelta(seconds=5.0) ))) # crear usuario con 5 segundos mas que yo - ONLINE
	listUser.append( ('07','192,168.123.238','fredy', str( miTiempo + timedelta(seconds=8.0) ))) # crear usuario con 8 segundos mas que yo - ONLINE
	listUser.append( ('08','192,168.123.212','jason', str( miTiempo + timedelta(seconds=10.0) ))) # crear usuario con 10 segundos mas que yo - Error de tiempo [Puede que el otro contacto no se este actualizando con el mismo intervalo de tiempo]
	listUser.append( ('09','192,168.123.253','alien', str( miTiempo + timedelta(minutes=1.0) ))) # crear usuario con 1 minuto(60 segundos) mas que yo - ERROR de tiempo [esto se presenta cuando el reloj del otro esta adelantado], ya que actualizan status a la BD con el mismo intervalo de tiempo, por lo tanto no debe haber mas diferencia

	r = getFormatListUsers(listUser, miTiempo)
	print( r )
	return r
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def testPintTableChat():
	print('Test - Tabla MSG:')
	listMSG = testGetListMSG()
	print('\nTest - Tabla Users:')
	listUSERS = testGetListUsers()
	print('\nTest - Pint Tabla Chat')
	print(pintTableMSG(listMSG, listUSERS))

if __name__ == "__main__": #Si ejecutas el script, ejecuta los test
	testPintTableChat()