# -*-coding:utf-8 -*

from rsquare import Rsquare
from robstacles import Rwall, Rdoor, Rplayer, Rexit
import random

class Rmap:
    """Classe permettant la gestion des cartes du Roboc Game"""

    def __init__(self, bmap):
        """Constructeur de la classe. Une instance est appelée avec une carte (en chaine de charactères)"""

        self._obj=dict()

        if type(bmap)!=str:
            raise TypeError("Erreur de création d'instance : la carte doit être une string")

        obs_corresp=dict()
        obs_corresp['O']= Rwall()
        obs_corresp[' ']= Rsquare()   
        obs_corresp['U']= Rexit()
        # obs_corresp['P']= Rplayer() \\\ Non fonctionnel depuis le fonctionnement multi-joueurs
        obs_corresp['.']= Rdoor()        

        # Construction de la map dans un dictionnaire
        self.pos_depart=tuple()
        self.pos_sortie=list()
        u=1
        (n,m)=(0,0)
        for (i,j) in enumerate(bmap):
            if j=='\n':
                m+=1
                n=0
            else:
                try:
                    self._obj[n,m]=obs_corresp[j]
                except KeyError:
                    self._obj[n,m]=Rsquare()
                if j=='X':
                    self.pos_depart=(n,m)
                if j=='U':
                    self.pos_sortie.append((n,m))
                # print(n,m,self._obj[n,m])
                n+=1
        # print('La position de depart est : ',self.pos_depart)
        # print('Les positions de sortie sont :',self.pos_sortie)

        # Definition de la dimension de la carte
        (self.nmax,self.mmax)=(1,1)
        for (i,j) in self._obj.keys():
            if i>self.nmax:
                self.nmax=i
            if j>self.mmax:
                self.mmax=j
        # print("Les dimensions de la carte sont de",self.nmax+1,"colonnes et",self.mmax+1,"lignes")

    def __getitem__(self,coord):
        """Methode speciale permettant l\'acces aux elements de la carte"""

        if (type(coord)!=tuple or len(coord)!=2):
            raise TypeError("Merci de renseigner deux coordonnees")

        try:
            return self._obj[coord]
        except KeyError:
            print("Ces coordonnees ('[colonnes,lignes]') sont en dehors de la carte ! La carte fait",self.nmax+1,"colonnes et",self.mmax+1,"lignes. Attention, les coordonnees commencent à 0.")

    def __setitem__(self,coord,rtype):
        """ Méthode spéciale permettant la modification d'une case de la carte"""

        self._obj[coord]=rtype

    def __repr__(self):
        """Methode de representation graphique de la carte"""

        rmapstr=str()
        for j in list(range(self.mmax+1)):
            for i in list(range(self.nmax+1)):
                rmapstr+=str(self[i,j])
            rmapstr+='\n'

        return rmapstr

    def randposition(self , *players_position):
        """Méthode renvoyant des coordonnées vides faisant partie de la partie, excluant les positions des joueurs déjà présents"""

        (coord1,coord2)=(0,0)

        if players_position==():
            players_position=((-1,-1),)

        while (type(self[coord1,coord2])!=Rsquare) or ((coord1,coord2) in players_position):
            coord1=random.randint(0,self.nmax)
            coord2=random.randint(0,self.mmax)

        return (coord1,coord2)
