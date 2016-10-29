# -*-coding:utf-8 -*

class rmap:
    """Classe permettant la gestion des cartes du Roboc Game"""

    def __init__(self, bmap):
        """Constructeur de la classe. Une instance est appelée avec une carte (en chaine de charactères)"""

        self._obj=dict()

        if type(bmap)!=str:
            raise TypeError("Erreur de création d'instance : la carte doit être une string")

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
                self._obj[n,m]=j
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

    def __repr__(self):
        """Methode de representation graphique de la carte"""

        rmapstr=str()
        for j in list(range(self.mmax+1)):
            for i in list(range(self.nmax+1)):
                rmapstr+=str(self[i,j])
            rmapstr+='\n'

        return rmapstr

class partie:
    """Classe permettant la gestion d'une partie. Elle est définie par une carte et un joueur et garde comme attribut la position du joueur et le statut de la partie (victoire ou non).\n La gestion des obstacles est faite dans cette classe"""

    def __init__(self,joueur,carte):
        """Constructeur de la classe Partie"""

        if type(joueur)!=str:
            raise TypeError("Erreur ! Le nom du joueur doit être une chaine de charactère")

        if type(carte)!=rmap:
            raise TypeError("Erreur ! La carte doit être un objet du type 'rmap'")

        self._position=carte.pos_depart
        self._rmapu=carte
        self._statut=False
        self._player=joueur

    def __repr__(self):
        """Affichage du statut de la partie"""

        partiestr=str()
        for j in list(range(self._rmapu.mmax+1)):
            for i in list(range(self._rmapu.nmax+1)):
                if (i,j)==self._position:
                    partiestr+='R'
                elif self._rmapu[i,j]=='X':
                    partiestr+=' '
                else:
                    partiestr+=str(self._rmapu[i,j])
            partiestr+='\n'

        return partiestr

    def mouv(self, direct):
        """Methode de deplacement unitaire du robot"""

        if direct not in ('N','E','W','O','S'):
            print("Merci de rentrer une action conforme :\n- N/S/E/O pour vous déplacer d\'une case,\n- N/S/E/O+X pour vous déplacer de X cases (ex: N3 ou O2)\n- Q pour quitter")
        else:
            pos_dir=tuple()
            
            # Determination de la position cible
            if direct=='N':
                pos_dir=(self._position[0],self._position[1]-1)
            elif direct=='S':
                pos_dir=(self._position[0],self._position[1]+1)
            elif direct=='E':
                pos_dir=(self._position[0]+1,self._position[1])
            elif direct=='W' or direct=='O':
                pos_dir=(self._position[0]-1,self._position[1])

            #Validation de la position cible
            if self._rmapu[pos_dir]=='O':
                print('Vous ne traversez pas les murs.\n')
            elif pos_dir[0]<0 or pos_dir[1]<0 or pos_dir[0]>self._rmapu.nmax or pos_dir[1]>self._rmapu.mmax:
                print('Votre robot est déjà aux frontières du réel...\n')
            elif self._rmapu[pos_dir]=='U':
                self._position=pos_dir
                self._statut=True
            else:
                self._position=pos_dir

