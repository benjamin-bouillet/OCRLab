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
chosenmap = rchoicemap()

# Chargement de la carte choisie en format texte
raw_carte = rloadmap(chosenmap)

# Création de la carte
map = Rmap(raw_carte)
par = Rgame(map)

# On démarre le serveur réseau et on le met à l'écoute de connexions entrantes
par.init_serveur()

# On accepte les connexions entrantes et on crée les joueurs associés, jusqu'a
# ce qu'un joueur démarre la partie
par.accept_joueurs()

# On envoie a l'ensemble des joueurs l'etat de la partie au debut du jeu
# On precise au premier joueur qu'il est celui qui va jouer en premier
par.avancement_partie(par.clients_connectes[0])

isend = False
while not par.victory and not isend:
    for client_joueur in par.clients_connectes:
        # while not instr_client:
        try:
            # On récupère la liste des connexions des joueurs connectés
            # On cherche les messages en attente dans cette liste
            clients_a_lire, wlist, rlist = select.select(
                    par.liste_sockets_connectes(), [], [], 0.05)
        except select.error:
            pass
        else:
            # On parcourt la liste des clients à lire
            for client in clients_a_lire:
                # On vérifie si le joueur écouté est le joueur qui doit jouer
                if client == client_joueur.socket_joueur:
                    # Si c'est le cas, on recupere l'action du joueur
                    isend, action, nb, dir_action = rinputchoice_net(
                            client_joueur.socket_joueur)
                    # on effectue l'action enregistree
                    par.raction(action, dir_action, client_joueur)
                    # on envoie la mise a jour de la partie l'ensemble des
                    # joueurs
                    par.avancement_partie(client_joueur)
                    par.winner = client_joueur
                else:
                    # Sinon, on écoute pour effacer le message en attente,
                    # mais on ne fait rien de cette instruction.
                    msg_recu = serv_listen(client_joueur.socket_joueur)
                    # client_instr
                    print("ce n'est pas votre tour !")

# On previent les joueurs que la partie est terminee
msg_fin = "{} a gagne. Fin de la partie...".format(par.winner.nom_joueur)
par.msg_all_client(msg_fin)

# Fermeture des connexions avec l'ensemble des sockets (clients) connectes
# On recupere la liste des sockets des clients connectes
# et on ferme l'ensemble des connexions liees a ces sockets
for socket_connecte in par.liste_sockets_connectes():
    serv_term(socket_connecte, par.connexion_principale)
