# -*-coding:utf-8 -*

from rmap import Rmap
from rsquare import Rsquare
from robstacles import *

class Rgame:
    """Classe permettant la gestion d'une partie. Elle est définie par une carte et un joueur et garde comme attribut la position du joueur et le statut de la partie (victoire ou non).\n La gestion des obstacles est faite dans cette classe"""

    def __init__(self,carte):
        """Constructeur de la classe Partie"""

        if type(carte)!=Rmap:
            raise TypeError("Erreur ! La carte doit être un objet du type 'Rmap'")

        self.rmapu=carte
        self.victory=False
        self.players_names=dict()
        self.players_positions=dict()

    def __repr__(self):
        """Affichage du statut de la partie"""

        for k in self.players_names.keys():
            print(k,":",self.players_names[k])
        print()

        partiestr=str()
        for j in list(range(self.rmapu.mmax+1)):
            for i in list(range(self.rmapu.nmax+1)):
                # On place les joueurs
                if (i,j) in self.players_positions.values():
                    for k in self.players_positions.keys():
                        if self.players_positions[k]==(i,j):
                            partiestr+=str(k)
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

    def add_player(self,player_name):
        """Methode d'ajout d'un joueur. Elle vient compléter le dictionnaire "players" qui contient les coordonnées de chacun des joueurs"""

        # On complète le dictionnaire des noms de joueurs
        self.players_names[len(self.players_names)+1]=player_name

        # On complète le dictionnaire des positions de joueurs en appelant la méthode randposition de l'object rmap.Rmap
        randomized_position=self.rmapu.randposition(self.players_positions.values())
        self.players_positions[len(self.players_positions)+1]=randomized_position
