# -*-coding:utf-8 -*

from rmap import Rmap

class Rgame:
    """Classe permettant la gestion d'une partie. Elle est définie par une carte et un joueur et garde comme attribut la position du joueur et le statut de la partie (victoire ou non).\n La gestion des obstacles est faite dans cette classe"""

    def __init__(self,joueur,carte):
        """Constructeur de la classe Partie"""

        if type(joueur)!=str:
            raise TypeError("Erreur ! Le nom du joueur doit être une chaine de charactère")

        if type(carte)!=Rmap:
            raise TypeError("Erreur ! La carte doit être un objet du type 'Rmap'")

        self._position=carte.pos_depart
        self.rmapu=carte
        self.victory=False
        self._player=joueur

    def __repr__(self):
        """Affichage du statut de la partie"""

        partiestr=str()
        for j in list(range(self.rmapu.mmax+1)):
            for i in list(range(self.rmapu.nmax+1)):
                # On place le joueur
                if (i,j)==self._position:
                    partiestr+='R'
                # On supprime le marquage de la position de départ
                elif self.rmapu[i,j]=='X':
                    partiestr+=' '
                else:
                    partiestr+=str(self.rmapu[i,j])
            partiestr+='\n'

        return partiestr

    def raction(self, action, direction):
        """Methode de deplacement unitaire du robot"""

        if action not in ('D','M','P'):
            print("Merci de rentrer une action conforme :\n- N/S/E/O pour vous déplacer d\'une case,\n- N/S/E/O+X pour vous déplacer de X cases (ex: N3 ou O2)\n- M pour murer une porte\n- P pour percer une porte\n- Q pour quitter")
        else:
            pos_dir=tuple()

            # Determination de la position cible
            if direction=='N':
                pos_dir=(self._position[0],self._position[1]-1)
            elif direction=='S':
                pos_dir=(self._position[0],self._position[1]+1)
            elif direction=='E':
                pos_dir=(self._position[0]+1,self._position[1])
            elif direction in ('W','O'):
                pos_dir=(self._position[0]-1,self._position[1])

            if action=='D':
                action=direction

            #Validation de la position cible
            if pos_dir[0]<0 or pos_dir[1]<0 or pos_dir[0]>self.rmapu.nmax or pos_dir[1]>self.rmapu.mmax:
                print('Votre robot est déjà aux frontières du réel...\n')
            else:
                (self.victory, confaction, self._position, mmessage)=self.rmapu[pos_dir].access(self._position,action)
                print(mmessage)