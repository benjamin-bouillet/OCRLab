# -*-coding:utf-8 -*

from rmap import Rmap
from rgame import Rgame
from rfunctions import rinputchoice_net, rchoicemap, rloadmap
from rnetwork import serv_init, serv_term, serv_listen
clear = "\n" * 100

"""Roboc - v2 - by Bibi"""
# commentaires de correction plus bas

print(clear)
print("Bienvenue dans Roboc !")
print("Le but du jeu est d'amener votre roboc vers la sortie (U)")
print()

# Choix de la carte (dans le dossier "cartes")
chosenmap=rchoicemap()

# Chargement de la carte choisie en format texte
raw_carte=rloadmap(chosenmap)

# Création de la carte
map=Rmap(raw_carte)
par=Rgame(map)

# ajout d'un joueur (temporaire)
par.add_player("Ben")

# Initilisation du serveur
main_connection, connection_with_client , infos_connexion = serv_init()

print(clear)

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
