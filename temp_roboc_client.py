# -*-coding:utf-8 -*

import socket
import select
from rnetwork import *

connection_with_serv=client_init()

recp=""

pname=input("Veuillez entrer votre nom :")
while recp!="name_acquired":
	rsend(connection_with_serv,pname)
	recp=rlisten(connection_with_serv)

while rlisten(connection_with_serv)!="termination":
	msg_to_send=input("intruction ?")
	rsend(connection_with_serv,msg_to_send)

client_term(connection_with_serv)