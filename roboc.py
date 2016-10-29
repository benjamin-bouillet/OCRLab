# -*-coding:utf-8 -*

import os
from rclasses import rmap,partie
import pickle
clear = "\n" * 100

"""Roboc - v0.1 - by Bibi"""
# commentaires de correction plus bas

print(clear)
print("Bienvenue dans Roboc !")
print("Le but du jeu est d'amener votre roboc vers la sortie (U)")
print()
roboc_user=input("Merci de renseigner votre nom : ")

# Récupération des sauvegardes existantes
try:
	with open('roboc_save_file','rb') as saves_file:
		saves_depickler=pickle.Unpickler(saves_file)
		rsave=saves_depickler.load()
# si le fichier de sauvegarde n'existe pas, on en crée un vide
except FileNotFoundError:
	with open('roboc_save_file','wb') as saves_file:
		saves_pickler=pickle.Pickler(saves_file)
		rsave=dict()
		saves_pickler.dump(rsave)

# Choix de la carte (dans le dossier "cartes")
liste_cartes=dict()
print("\nVoici la liste des cartes disponibles :")
nb_map=0
for n,m in enumerate([i for i in os.listdir('cartes') if i.endswith('.txt')]):
	print(n+1,m[:-4])
	liste_cartes[n+1]=m
nb_map=input("\nMerci de renseigner le numero correspondant à une carte ci-dessus : ")
while int(nb_map) not in liste_cartes:
	print(clear)
	print("\nVoici la liste des cartes disponibles :")
	for n,m in enumerate([i for i in os.listdir('cartes') if i.endswith('.txt')]):
		print(n+1,m[:-4])
	nb_map=input("\nMerci de renseigner le numero correspondant à une carte ci-dessus : ")

with open("cartes/"+liste_cartes[int(nb_map)],"r") as raw_carte_file:
	raw_carte=raw_carte_file.read()

# Verification de la présence d'une sauvegarde sur la carte
if liste_cartes[int(nb_map)] in rsave:
	print("\nLe joueur",rsave[liste_cartes[int(nb_map)]]._player,"a déjà une partie en cours pour la carte",liste_cartes[int(nb_map)],'.')
	answer_existing_map=input("Voulez-vous la charger (O/N) ?")
	while answer_existing_map.upper() not in ('O','N'):
		answer_existing_map=input("\nMerci de répondre par oui (O) ou non (N) :")
	# si le joueur veut reprendre une partie, on charge celle-ci
	if answer_existing_map.upper()=='O':
		par=rsave[liste_cartes[int(nb_map)]]
		par._player=roboc_user
	# sinon, on supprime la sauvegarde et on recommence une nouvelle partie
	else:
		del rsave[liste_cartes[int(nb_map)]]
		roboc_carte=rmap(raw_carte)
		par=partie(roboc_user,roboc_carte)
else:
	roboc_carte=rmap(raw_carte)
	par=partie(roboc_user,roboc_carte)

print(clear)

# Boucle permettant de jouer les coups. Elle attend que l'instance de la classe partie lui renvoie un _statut=True
while not par._statut:
	print(par)
	action_conforme=False
	while not action_conforme:
		rinput=input("Action ? ")
		print(clear)
		# Test sur l'action utilisateur : action type "N" ou "NX"
		if len(rinput)==1:
			# Sortie du jeu
			if rinput.upper()=='Q':
				print('')
				raise UserWarning("Fin de la partie... Ne vous inquiètez pas, votre progression est sauvegardée !")
			# On déplace le roboc d'une case
			action_conforme=True
			par.mouv(rinput.upper())
		else:
			try:
				int(rinput[1:])
			except ValueError:
				print("Merci de rentrer une action conforme :\n- N/S/E/O pour vous déplacer d\'une case,\n- N/S/E/O+X pour vous déplacer de X cases (ex: N3 ou O2)\n- Q pour quitter\n")
				break
			#On déplace le roboc de X cases
			i=0
			while i!=int(rinput[1:]):
				par.mouv(rinput[0].upper())
				i+=1
			action_conforme=True

	# Sauvegarde après chaque coup
	rsave[liste_cartes[int(nb_map)]]=par
	with open("roboc_save_file","wb") as saves:
		saves_pickler=pickle.Pickler(saves)
		saves_pickler.dump(rsave)

# En condition de victoire, on efface la partie de la sauvegarde & on sauvegarde
del rsave[liste_cartes[int(nb_map)]]

with open("roboc_save_file","wb") as saves:
	saves_pickler=pickle.Pickler(saves)
	saves_pickler.dump(rsave)

# On affiche et on quitte
print(par)
print('')
print("Victoire !")
input("Appuyez sur 'Entrée pour quitter...")

#Le travail est bien réalisé et correspond aux consignes de l'exercice. Globalement on sent une bonne maitrise du cours jusque là. Seul bémol: la modularité. En effet, on a bien un découpage en classes et modules mais là c'est vraiment minime et cela aurait nécéssité d'étendre un peu plus le modèle objet (une classe carte, une classe pour les sauvegardes par exemple...)

#Très bien, j'ai bien aimé le fait que l'utilisateur entre son nom et que la sauvegarde se fasse par rapport à lui. J'aurais aimé un peu plus de documentation mais c'est déjà pas mal. Et je n'ai pas compris pourquoi tu lèves une erreur quand le joueur décide de quitter.

# Le code fonctionne. Des actions de robustesse ont été prévues pour les actions non conformes ou erronées ou la saisie non valide de nom de labyrinthe. Le code est propre et bien commenté. Personnellement, je n’aurai pas mis deux classes dans le même module rclasses. Je préfère associer un module à chaque classe, pour rester au plus près de la notion d’objet (un objet « partie » associé à un module, et un objet « map » associé à un autre module.) Deux modules différents permettent de faire évoluer les objets indépendamment. Pourquoi avoir mélanger anglais et français, en utilisant le mot rmap ? L’introduction des deux classes est cependant judicieuse. Je trouve maladroit l’utilisation de par._statut ou _player dans le module roboc. Les attributs commençant par « _ » sont par convention considérés privés ; on évite de les utiliser hors du module. (revoir la notion de propriétés ou supprimer ‘_’. ) (je cite le cours : "La convention veut qu'on n'accède pas, depuis l'extérieur de la classe, à un attribut commençant par un souligné _. C'est une convention, rien ne vous l'interdit… s") De même, il est préférable que les noms de classe commencent par une majuscule (PEEP 8 de Python). 