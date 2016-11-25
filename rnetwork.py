# -*-coding:utf-8 -*

import socket

hote=''
port = 12800

def serv_init():
	""" Methode de génération du serveur Roboc"""

	hote=''
	port = 12800

	main_connection=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
	main_connection.bind((hote, port))
	main_connection.listen(5)

	print("Le serveur écoute à présent sur le port {}".format(port))
	connection_with_client , infos_connexion=main_connection.accept()

	return main_connection, connection_with_client , infos_connexion

def serv_listen(connection_with_client):
	"""Methode d'écoute du serveur"""

	client_instruction = b""
	client_instruction = connection_with_client.recv(1024)
	# L'instruction ci-dessous peut lever une exception si le message\
	# Réceptionné comporte des accents
	
	rcv_msg = client_instruction.decode()

	return rcv_msg
	# connection_with_client.send(b"Instruction recue")

def serv_term(connection_with_client,main_connection):
	"""Méthode de fermeture de la connexion côté serveur"""

	print("Fermeture de la connexion") 
	connection_with_client.close()
	main_connection.close()


def client_init():
	"""Méthode de génération de la connexion côté client"""

	connection_with_serveur=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
	connection_with_serveur.connect((hote, port))
	print("Connexion etablie avec le serveur sur le port {}".format(port))	

	return connection_with_serveur

def client_instr(connection_with_serveur,instruct):
	"""Methode d'envoi d'instruction au serveur par le client"""

	send_msg = instruct
	# Peut planter si vous tapez des caractères spéciaux
	send_msg = send_msg.encode()
	# On envoie le message
	connection_with_serveur.send(send_msg)

def client_term(connection_with_serveur):
	"""Méthode de fermeture de la connexion côté client"""

	print("Fermeture de la connexion")
	connection_with_serveur.close()



