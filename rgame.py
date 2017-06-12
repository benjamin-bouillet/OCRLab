# -*-coding:utf-8 -*

import socket
import select
from rmap import Rmap
from rsquare import Rsquare
from rjoueur import Rjoueur
from robstacles import *

class Rgame:
	"""Classe permettant la gestion d'une partie. Elle est définie par une carte et un joueur et garde comme attribut la position du joueur et le statut de la partie (victoire ou non).\n La gestion des obstacles est faite dans cette classe"""

	def __init__(self,carte):
		"""Constructeur de la classe Partie"""

		if type(carte)!=Rmap:
			raise TypeError("Erreur ! La carte doit être un objet du type 'Rmap'")

		# Attributs liés au jeu lui-même
		self.rmapu=carte
		self.victory=False
		# self.players_names=dict()
		# self.players_positions=dict()

		# Attributs liés au réseau
		self._hote = ''
		self._port = 12800
		# self.nom_joueurs = dict()
		self.compteur_joueurs = 0
		self.clients_connectes = list()
		self.connexion_principale = socket.socket()

	def __repr__(self):
		"""Affichage du statut de la partie"""

		for k in self.clients_connectes:
			print("#{0} : {1} - {2}".format(k.numero_joueur, k.nom_joueur, k.position_joueur))

		partiestr=str()
		for j in list(range(self.rmapu.mmax+1)):
			for i in list(range(self.rmapu.nmax+1)):
				##################################################################################################
				# On crée une liste temporaire regroupant les positions des joueurs
				positions_joueurs = list()
				for joueur in self.clients_connectes:
					positions_joueurs.append(joueur.position_joueur)
				# On place les joueurs
				if (i,j) in positions_joueurs:
					for joueur in self.clients_connectes:
						if joueur.position_joueur == (i,j):
							partiestr+=str(joueur.numero_joueur)
				# if (i,j) in self.players_positions.values():
				# 	for k in self.players_positions.keys():
				# 		if self.players_positions[k]==(i,j):
				# 			partiestr+=str(k)
				##################################################################################################
				# On supprime le marquage de la position de départ
				elif self.rmapu[i,j]=='X':
					partiestr+=' '
				else:
					partiestr+=str(self.rmapu[i,j])
			partiestr+='\n'

		return partiestr

	def raction(self, action, direction, joueur):
		"""Methode de deplacement unitaire du robot"""

		if action not in ('D','M','P'):
			print("Merci de rentrer une action conforme :\n- N/S/E/O pour vous déplacer d\'une case,\n- N/S/E/O+X pour vous déplacer de X cases (ex: N3 ou O2)\n- M pour murer une porte\n- P pour percer une porte\n- Q pour quitter")
		else:
			pos_dir=tuple()
			virtual_opp=Rplayer()
			pposition=self.players_positions[joueur]

			# Determination de la position cible
			if direction=='N':
				pos_dir=(pposition[0],pposition[1]-1)
			elif direction=='S':
				pos_dir=(pposition[0],pposition[1]+1)
			elif direction=='E':
				pos_dir=(pposition[0]+1,pposition[1])
			elif direction in ('W','O'):
				pos_dir=(pposition[0]-1,pposition[1])

			if action=='D':
				action=direction

			#Validation de la position cible
			if pos_dir[0]<0 or pos_dir[1]<0 or pos_dir[0]>self.rmapu.nmax or pos_dir[1]>self.rmapu.mmax:
				print('Votre robot est déjà aux frontières du réel...\n')
			else:
				# On vérifie si la destination (pos_dir) est occupée par un joueur
				if pos_dir in self.players_positions.values():
					(self.victory, confaction, self.players_positions[joueur], mmessage)=virtual_opp.access(pposition,action)
					print(mmessage)
				else:
					(self.victory, confaction, self.players_positions[joueur], mmessage)=self.rmapu[pos_dir].access(pposition,action)
					print(mmessage)

	def add_player(self,numero_joueur, nom_joueur, socket_joueur):
		"""Methode d'ajout d'un joueur. Elle vient compléter le dictionnaire "players" qui contient les coordonnées de chacun des joueurs"""

		# On détermine une position vide en appelant la méthode randposition de l'object rmap.
		randomized_position=self.rmapu.randposition(self.clients_connectes)

		# On crée l'objet Rjoueur associé
		nouveau_joueur = Rjoueur(numero_joueur, nom_joueur, socket_joueur, randomized_position)
		
		# On ajoute le joueur à la liste des joueurs connectés
		self.clients_connectes.append(nouveau_joueur)

	def init_serveur(self):

		""" Méthode d'initilisation du serveur de la partie. Cette méthode se termine sur l'écoute par le serveur de connection entrante sur le port associée en attribut à l'init """

		self.connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connexion_principale.bind((self._hote, self._port))
		self.connexion_principale.listen(5)
		print("Le serveur écoute à présent sur le port {}".format(self._port))

	def accept_joueurs(self):

		""" Méthode acceptant les connexions entrantes, jusqu'à ce qu'un joueur lance la partie """

		print('En attente de connexions entrantes...')

		partie_demarree = False
		while not partie_demarree:
			# On va vérifier que de nouveaux clients ne demandent pas à se connecter
			connexions_demandees, wlist, xlist = select.select([self.connexion_principale], [], [], 0.05)

			for connexion in connexions_demandees:
				# On accepte la connexion entrante
				connexion_avec_client, infos_connexion = connexion.accept()
				# On récupère le nom du client
				nom_joueur = ''
				while nom_joueur == '':
					nom_joueur = connexion_avec_client.recv(1024)
					nom_joueur = nom_joueur.decode()
				# On ajoute le joueur entrant à la liste des clients connectés
				self.compteur_joueurs += 1
				self.add_player(self.compteur_joueurs, nom_joueur, connexion_avec_client)

				print("Le joueur numéro {0} nommé {1} s'est connecté".format(self.compteur_joueurs, nom_joueur))

			# Maintenant, on écoute la liste des clients connectés pour récupèrer un éventuel go de la part d'un des joueurs

			client_a_lire = []
			try:
				# On récupère la liste des connexions des joueurs connectés
				liste_socket_connectes = (o.socket_joueur for o in self.clients_connectes)
				# On cherche les messages en attente dans cette liste
				clients_a_lire, wlist, rlist = select.select(liste_socket_connectes, [], [], 0.05)
			except select.error:
				pass
			else:
				# On parcourt la liste des clients à lire
				for client in clients_a_lire:
					# Client est de classe socket
					msg_recu = client.recv(1024)
					# Peut planter si le message contient des caractères spéciaux
					msg_recu = msg_recu.decode()

					if msg_recu.lower() == 'c':
						partie_demarree = True

		print()
