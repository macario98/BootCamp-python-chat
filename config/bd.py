import psycopg2
from .config import readJSON #se usa FIXME punto para llamar un mudulo que se utilizara en este otro mudulo

host = ''
bd = ''
user = ''
pasw = ''

def leerConfiguracion():
	global host, bd, user, pasw
	try:
		str_conn = readJSON()
		host=str_conn['conexion'][0]['host']
		bd=str_conn['conexion'][0]['database']
		user=str_conn['conexion'][0]['username']
		pasw=str_conn['conexion'][0]['password']
		return True

	except (Exception, psycopg2.DatabaseError) as error:
		print("Error: ", error)
		return False

def selectUsers():
	if checkVariables() == False:
		leerConfiguracion()
	global host, bd, user, pasw
	sql = 'SELECT *  FROM cat.users'
	try:
		conexion = psycopg2.connect(host=host, database=bd, user=user, password=pasw)
		cur = conexion.cursor()
		cur.execute(sql)

		lista =  cur.fetchall()
		cur.close()

		return lista
		#print('Lista:', lista)

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		return []
	finally:
		conexion.close()

def updateLastSeen(id):
	if checkVariables() == False:
		leerConfiguracion()

	global host, bd, user, pasw
	from datetime import datetime
	hoy = datetime.now()
	sql = 'UPDATE cat.users SET last_seen = %s WHERE user_id = %s;'

	try:
		conexion = psycopg2.connect(host=host, database=bd, user=user, password=pasw)
		cur = conexion.cursor()
		cur.execute(sql, (hoy, id))
		conexion.commit()

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		conexion.close()

def checkVariables():#(validaVariablesDeConexion)verifica que las variables esten asignadas
	global host, bd, user, pasw
	if host == '' or bd == '' or user == '' or pasw == '':
		return False
	else:
		return True

	
if __name__ == "__main__":
	print('Test - Consulta Users - BD')
	print(selectUsers())