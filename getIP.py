from socket import socket, AF_INET, SOCK_DGRAM #se especifican las importaciones para liberar memoria

def getIP():
	s = socket(AF_INET, SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return str(s.getsockname()[0])