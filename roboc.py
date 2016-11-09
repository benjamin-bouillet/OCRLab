# -*-coding:utf-8 -*

import os
from rmap import Rmap
from rgame import Rgame
from rfunctions import rinputchoice, rloadsave, rdumpsave, rchoicemap, rloadmap, rchecksave
import pickle
clear = "\n" * 100

"""Roboc - v1.1 - by Bibi"""
# commentaires de correction plus bas

print(clear)
print("Bienvenue dans Roboc !")
print("Le but du jeu est d'amener votre roboc vers la sortie (U)")
print()
roboc_user=input("Merci de renseigner votre nom : ")

# Récupération des sauvegardes existantes
# si le fichier de sauvegarde n'existe pas, on en crée un vide
rsave=rloadsave()

# Choix de la carte (dans le dossier "cartes")
chosenmap=rchoicemap()

# Chargement de la carte choisie en format texte
raw_carte=rloadmap(chosenmap)

# Verification de la présence d'une sauvegarde sur la carte
par=rchecksave(chosenmap, rsave, roboc_user)

print(clear)

 # Boucle permettant de jouer les coups. Elle attend que l'attribut "victory" de la partie (objet Rgame) soit vrai
isend=False
while not par.victory and not isend:
	print(par)
	isend, action, nb , dir_action=rinputchoice()
	if not isend:
		i=0
		while i<nb:
			par.raction(action, dir_action)
			i+=1

	# Sauvegarde après chaque coup
	rdumpsave(par,rsave,chosenmap)

# En condition de victoire, on efface la partie de la sauvegarde & on sauvegarde
if par.victory:
	del rsave[chosenmap]

	rdumpsave(par,rsave,None)

	# On affiche et on quitte
	print(par)
	print('')
	print("Victoire !")
	input("Appuyez sur 'Entrée pour quitter...")

#Le travail est bien réalisé et correspond aux consignes de l'exercice. Globalement on sent une bonne maitrise du cours jusque là. Seul bémol: la modularité. En effet, on a bien un découpage en classes et modules mais là c'est vraiment minime et cela aurait nécéssité d'étendre un peu plus le modèle objet (une classe carte, une classe pour les sauvegardes par exemple...)

#Très bien, j'ai bien aimé le fait que l'utilisateur entre son nom et que la sauvegarde se fasse par rapport à lui. J'aurais aimé un peu plus de documentation mais c'est déjà pas mal. Et je n'ai pas compris pourquoi tu lèves une erreur quand le joueur décide de quitter.

# Le code fonctionne. Des actions de robustesse ont été prévues pour les actions non conformes ou erronées ou la saisie non valide de nom de labyrinthe. Le code est propre et bien commenté. Personnellement, je n’aurai pas mis deux classes dans le même module rclasses. Je préfère associer un module à chaque classe, pour rester au plus près de la notion d’objet (un objet « partie » associé à un module, et un objet « map » associé à un autre module.) Deux modules différents permettent de faire évoluer les objets indépendamment. Pourquoi avoir mélanger anglais et français, en utilisant le mot rmap ? L’introduction des deux classes est cependant judicieuse. Je trouve maladroit l’utilisation de par._statut ou _player dans le module roboc. Les attributs commençant par « _ » sont par convention considérés privés ; on évite de les utiliser hors du module. (revoir la notion de propriétés ou supprimer ‘_’. ) (je cite le cours : "La convention veut qu'on n'accède pas, depuis l'extérieur de la classe, à un attribut commençant par un souligné _. C'est une convention, rien ne vous l'interdit… s") De même, il est préférable que les noms de classe commencent par une majuscule (PEEP 8 de Python). 