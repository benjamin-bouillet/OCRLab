# -*-coding:utf-8 -*

import pickle
import os
from rmap import Rmap
from rgame import Rgame
from rnetwork import serv_listen


def rloadsave():
    """Fonction de chargement des sauvegardes. Si le fichier 'roboc_save_file
    n'existe pas, il est créé vide"""

    try:
        with open('roboc_save_file', 'rb') as saves_file:
            saves_depickler = pickle.Unpickler(saves_file)
            rsave = saves_depickler.load()
    # si le fichier de sauvegarde n'existe pas, on en crée un vide
    except FileNotFoundError:
        with open('roboc_save_file', 'wb') as saves_file:
            saves_pickler = pickle.Pickler(saves_file)
            rsave = dict()
            saves_pickler.dump(rsave)

    return(rsave)


def rdumpsave(par, rsave, cmap):
    """Fonction de vidage de la partie dans un fichier de
    sauvegarde 'roboc_save_file'"""
    if cmap is not None:
        rsave[cmap] = par
    with open("roboc_save_file", "wb") as saves:
        saves_pickler = pickle.Pickler(saves)
        saves_pickler.dump(rsave)


def rchoicemap():
    """Fonction de choix de la carte parmi les cartes présentes dans le
    dossier 'cartes'"""
    list_cartes = dict()
    print("\nVoici la liste des cartes disponibles :")
    nb_map = 0
    for n, m in enumerate([i for i in os.listdir('cartes') if i.endswith(
            '.txt')]):
        print(n+1, m[:-4])
        list_cartes[n+1] = m
    nb_map = input(
               "\nMerci de renseigner le numero correspondant"
               + " à une carte ci-dessus : ")
    while int(nb_map) not in list_cartes:
        print("\nVoici la liste des cartes disponibles :")
        for n, m in enumerate([i for i in os.listdir('cartes') if i.endswith(
                '.txt')]):
            print(n+1, m[:-4])
        nb_map = input("\nMerci de renseigner le numero correspondant à une"
                       " carte ci-dessus : "
                       )

    return list_cartes[int(nb_map)]


def rloadmap(cmap):
    """Fonction de chargement de la map choisie en format texte"""

    with open("cartes/"+cmap, "r") as raw_carte_file:
        raw_carte = raw_carte_file.read()

    return raw_carte


def rchecksave(chosen_map, rsave, roboc_user):
    """Fonction de vérification de la présence d'une sauvegarde sur une map
    donnée et dans un fichier de sauvegarde donnée. Prend comme argument une
    carte (classe 'Rmap') dans un dictionnaire de sauvegarde rsave. La
    fonction renvoie une partie par (class rgame)"""

    # Verification de la présence d'une sauvegarde sur la carte
    if chosen_map in rsave:
        print("\nLe joueur", rsave[chosen_map]._player,
              "a déjà une partie en cours pour la carte", chosen_map, '.')
        answer_existing_map = input("Voulez-vous la charger (O/N) ?")
        while answer_existing_map.upper() not in ('O', 'N'):
            answer_existing_map = input(
                    "\nMerci de répondre par oui (O) ou non (N) :")
        # si le joueur veut reprendre une partie, on charge celle-ci
        if answer_existing_map.upper() == 'O':
            par = rsave[chosen_map]
            par._player = roboc_user
        # sinon, on supprime la sauvegarde et on recommence une nouvelle partie
        else:
            del rsave[chosen_map]
            roboc_carte = Rmap(rloadmap(chosen_map))
            par = Rgame(roboc_user, roboc_carte)
    else:
        roboc_carte = Rmap(rloadmap(chosen_map))
        par = Rgame(roboc_user, roboc_carte)

    return par


def rinputchoice_net(connection_with_client):
    """Fonction de récupération du choix de l'utilisateur en réseau. Renvoie
    un tuple (isend,action,nb). isend est True si le joueur décide de
    s'arrêter. direct contient la direction de déplacement. nb contient
    le nombre de case de déplacement."""

    error_case = str("""Merci de rentrer une action conforme :\n- N/S/E/O pour
                   vous deplacer d\'une case,\n- N/S/E/O+X pour vous
                   deplacer de X cases (ex: N3 ou O2)\n- Q pour quitter\n""")
    isend = False
    action, nb = None, 1
    conform_action = False
    dir_act = None

    while not conform_action:
        try:
            rinput = serv_listen(connection_with_client)
            # Test sur l'action utilisateur : action type "N" ou "NX"
            if len(rinput) == 1:
                # Sortie du jeu
                if rinput.upper() == 'Q':
                    print("""Fin de la partie... Ne vous inquiètez pas, votre
                            progression est sauvegardée !""")
                    isend = True
                elif rinput.upper() in ('N', 'S', 'E', 'O', 'W'):
                    assert type(rinput) == str
                    action = 'D'
                    dir_act = rinput.upper()
                    nb = 1
                else:
                    raise ValueError
                conform_action = True
            elif rinput[0].upper() in ('M', 'P'):
                action = rinput[0].upper()
                dir_act = rinput[1].upper()
                nb = 1
                conform_action = True
            elif rinput[0].upper() in ('N', 'S', 'E', 'O', 'W'):
                action = 'D'
                dir_act = rinput[0].upper()
                nb = int(rinput[1:])
                conform_action = True
            else:
                raise ValueError
        except NameError:
            pass
            print(error_case)
        except ValueError:
            pass
            print(error_case)
        except SyntaxError:
            pass
            print(error_case)
    return (isend, action, nb, dir_act)
