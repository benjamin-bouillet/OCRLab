# -*-coding:utf-8 -*

from rsquare import Rsquare

class Rwall(Rsquare):
    """Classe définissant le comportement d'un mur"""

    def __repr__(self):
        """Methode de representation graphique d'un mur"""

        rsquarerepr='O'

        return rsquarerepr

    def mouv(self, coord, action):
        """ Méthode de comportement en cas de déplacement vers le Rwall"""

        # Renvoie une validation d'action conforme, les nouvelles coordonnées du joueur ainsi qu'une absence de message (un déplacement sur une case vide ne génère aucun message d'alerte au joueur)
        return (False, coord, "Vous ne traversez pas les murs")

class Rdoor(Rsquare):
    """Classe définissant le comportement d'une porte"""

    def __init__(self):
        """Constructeur de la classe ; permet la gestion du murage et les cas de représentation graphique"""

        self._iswalled=False
        Rsquare.__init__(self)

    def __repr__(self):
        """Methode de representation graphique d'une porte"""

        if self._iswalled:
            rsquarerepr='0'
        else:
            rsquarerepr='.'

        return rsquarerepr

    def mouv(self, coord, action):
        """ Méthode de comportement en cas de déplacement vers le Rwall"""

        if self._iswalled:
            confaction=False
            retcoord=coord
            message="Il vous faut percer ce mur avant de pouvoir le traverser"
        else:
            confaction=True
            (i,j)=coord
            if action=='N':
                j-=1
            elif action=='S':
                j+=1
            elif action=='E':
                i+=1
            elif action in ('W','O'):
                i-=1
            retcoord=(i,j)
            message=""

        return (confaction,retcoord,message)

    def wall(self):
        """ Méthode de comportement en cas de 'murage' vers le rsquare"""

        if self._iswalled:
            confaction=False
            message="Cette porte est déjà murée, pourquoi ne pas essayer de la percer ?"
        else:
            self._iswalled=True
            confaction=True
            message=""

        return (confaction, message)

    def destroy(self):
        """ Méthode de comportement en cas de 'perçage' vers le rsquare"""
        
        if self._iswalled:
            confaction=True
            message=''
            self._iswalled=False
        else:
            confaction=False
            message="Rien à percer ici..."

        return (confaction, message)

class Rplayer(Rsquare):
    """Classe définissant le comportement d'un joueur"""

    def __repr__(self):
        """Methode de representation graphique d'un joueur"""

        rsquarerepr='P'

        return rsquarerepr

    def mouv(self, coord, action):
        """ Méthode de comportement en cas de déplacement vers le Rplayer"""

        return (False, coord, "Ne marchez pas sur les pieds de votre adversaire !")

class Rexit(Rsquare):
    """Classe définissant le comportement d'une sortie"""

    def __repr__(self):
        """Methode de representation graphique d'une sortie"""

        rsquarerepr='U'

        return rsquarerepr

    def mouv(self, coord, action):
        """Méthode de comportement en cas de déplacement vers la sortie"""

        self.isvictory=True
        (i,j)=coord
        if action=='N':
            j-=1
        elif action=='S':
            j+=1
        elif action=='E':
            i+=1
        elif action in ('W','O'):
            i-=1

        # Renvoie une validation d'action conforme, les nouvelles coordonnées du joueur ainsi qu'une absence de message (un déplacement sur une case vide ne génère aucun message d'alerte au joueur)
        return (True, (i,j), "")
