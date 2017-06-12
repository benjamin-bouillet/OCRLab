# -*-coding:utf-8 -*

from rnetwork import client_init, client_instr, client_term
from threading import Thread
from rclient import ClientDisplay, ClientInput

clear = "\n" * 100

input("Initialisation du client. Appuyez sur 'Entrée' pour continuer")

# Initialisation de la connexion avec le serveur
rconnection=client_init()

# Renseignement du nom du joueur
nom_joueur=input("Veuillez renseigner votre nom : ")
client_instr(rconnection,nom_joueur)

# Renseignement du nom du joueur
demarrage=''
while demarrage.upper()!="C":
	demarrage=input("Tapez 'c' pour démarrer la partie :")
	client_instr(rconnection,demarrage)

thread1 = ClientDisplay(rconnection)
thread2 = ClientInput(rconnection)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

client_term(rconnection)