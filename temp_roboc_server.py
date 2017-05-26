# -*-coding:utf-8 -*

import socket
import select
from rnetwork import *


hote=""
port=12800

connection_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection_server.bind((hote,port))
connection_server.listen(5)
print("Le serveur écoute désormais sur le port {}".format(port))
print("En attente de connexion des joueurs")

rec_msg=""
in_game=True
connected_clients=[]
players_name=dict()
game_started=False
while in_game:
	while not game_started:
		# On vérifie que des clients ne chercent pas à se connecter
		# on écoute pour cela la connexion principale
		# Attente max : 50ms
		awaiting_connections, wlist, xlist = select.select([connection_server],[],[],0.05)

		# On se connecte à chacun des clients en attente de connexion
		for connection in awaiting_connections:
			connection_to_client, connection_infos=connection.accept()

			# On ajoute l'ensemble de ces connexions à une liste qui nous permettra d'écouter par la suite
			connected_clients.append(connection_to_client)

		# Maintenant, on récupère le nom de tous les clients
		# On fait un "try" pour éviter de se retrouver avec une liste de clients à lire vide qui léverai une exception
		clients_to_read=[]
		try:
			clients_to_read, wlist, xlist = select.select(connected_clients,[],[],0.05)
		except select.error:
			pass
		else:
			for client in clients_to_read:
				if client not in players_name.keys():
					client_name=""
					while client_name=="":
						client_name=rlisten(client)
					print("Le joueur {} vient de se connecter".format(client_name))
					rsend(client,"name_acquired")
					players_name[client]=client_name
				else:
					if rlisten(client)=="c":
						game_started=True

	answer=""
	while answer.upper()!="q":
		print("Voici la liste des joueurs connectés :")
		for p in players_table.keys():
			print(p,":",players_table[p])
		answer=input("quitter? (q)")
	in_game=False

print("Fermeture des connexions...")
for client in connected_clients:
	client.send(b"termination")
	client.close()

connection_server.close()
input('Toutes connexions fermés ! Arrêt du programme...')