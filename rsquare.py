# -*-coding:utf-8 -*

class Rsquare:
    """ Classe permettant la gestion des cases (obstacles et vides) du roboc. Le comportement de cette classe est celui d'une case vide."""

    def __init__(self):
        """Constructeur du Rsquare"""
        
        self.isvictory=False

    def __repr__(self):
        """Methode de representation graphique de la carte"""

        rsquarerepr=' '

        return rsquarerepr

    def access(self, coord, action):
        """Methode définissant le comportement de l'obstacle lorsque le joueur essaie de se déplacer sur sa position"""

        confaction=False
        destpos=coord
        mmessage=""
        # Si l'action est un mouvement
        if action.upper() in ('N','S','E','W','O'):
            (confaction,destpos,mmessage)=self.mouv(coord,action.upper())
        # Si l'action est un "murage" de porte
        elif action.upper()=='M':
            (confaction,mmessage)=self.wall()
        # Si l'action est un 'perçage' de porte
        elif action.upper()=='P':
            (confaction,mmessage)=self.destroy()

        return(self.isvictory, confaction, destpos, mmessage)

    def mouv(self, coord, action):
        """ Méthode de comportement en cas de déplacement vers le rsquare"""

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

    def wall(self):
        """ Méthode de comportement en cas de 'murage' vers le rsquare"""

        return (False, "Votre destination ne se mure pas !")

    def destroy(self):
        """ Méthode de comportement en cas de 'perçage' vers le rsquare"""

        return (False, "Votre destination ne se perce pas !")