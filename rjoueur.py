# -*-coding:utf-8 -*

class Rjoueur():
	""" Classe (très simple) de gestion des joueurs connectés sur le serveur """

	def __init__(self, jnumero, jnom, jsocket, jposition):
		""" Constructeur de la classe joueur """

		self.numero_joueur = jnumero
		self.socket_joueur = jsocket
		self.nom_joueur = jnom
		self.position_joueur = jposition

	def __repr__(self):
		"""Affichage du des informations joueurs"""

		return "Joueur #{0} : {1} - {2}".format(self.numero_joueur, self.nom_joueur, self.position_joueur)