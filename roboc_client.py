# -*-coding:utf-8 -*

from rnetwork import client_init, client_instr, client_term

clear = "\n" * 100
input("Cote client. Initialisation...")

# Initialisation de la connexion avec le serveur
rconnection=client_init()

instruct=""

while instruct.upper()!="Q":
	instruct=input("Instruction :")
	client_instr(rconnection,instruct)

client_term(rconnection)