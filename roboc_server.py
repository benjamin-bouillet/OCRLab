# -*-coding:utf-8 -*

from rmap import Rmap
from rgame import Rgame
from rfunctions import rinputchoice_net, rchoicemap, rloadmap
from rnetwork import serv_term, serv_listen

import select

clear = "\n" * 100

"""Roboc - v2 - by Bibi"""

# print(clear)
print("Bienvenue dans Roboc")

# Choix de la carte (dans le dossier "cartes")
chosenmap=rchoicemap()

# Chargement de la carte choisie en format texte
raw_carte=rloadmap(chosenmap)

# Création de la carte
map = Rmap(raw_carte)
par = Rgame(map)

# On démarre le serveur réseau et on le met à l'écoute de connexions entrantes
par.init_serveur()

# On accepte les connexions entrantes et on crée les joueurs associés, jusqu'à ce qu'un joueur démarre la partie
par.accept_joueurs()

isend=False
while not par.victory and not isend:
	for client_joueur in par.clients_connectes:
		#while not instr_client:
		client_a_lire = []
		try:
			# On récupère la liste des connexions des joueurs connectés
			liste_socket_connectes = (o.socket_joueur for o in par.clients_connectes)
			# On cherche les messages en attente dans cette liste
			clients_a_lire, wlist, rlist = select.select(liste_socket_connectes, [], [], 0.05)
		except select.error:
			pass
		else:
			# On parcourt la liste des clients à lire
			for client in clients_a_lire:
				# On vérifie si le joueur écouté est le joueur qui doit jouer
				if client == client_joueur.socket_joueur:
					print(par)
					# Si c'est le cas, on fait avancer le jeu avec son action
					isend, action, nb , dir_action = rinputchoice_net(client_joueur.socket_joueur)
				else:
					# Sinon, on écoute pour effacer le message en attente, mais on ne fait rien de cette instruction
					msg_recu = serv_listen(connection_with_client)
					#client_instr
					print("ce n'est pas votre tour !")







 # Boucle permettant de jouer les coups. Elle attend que l'attribut "victory" de la partie (objet Rgame) soit vrai
isend=False
while not par.victory and not isend:
	print(par)
	isend, action, nb , dir_action=rinputchoice_net(connection_with_client)
	if not isend:
		i=0
		while i<nb:
			par.raction(action, dir_action, 1)
			i+=1

# Fermeture de la connexion serveur
serv_term(connection_with_client,main_connection)

# En condition de victoire, on efface la partie de la sauvegarde & on sauvegarde
if par.victory:

	# On affiche et on quitte
	print(par)
	print('')
	print("Victoire !")
	input("Appuyez sur 'Entrée pour quitter...")

# multi-joueur
# avec interface