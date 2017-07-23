# -*-coding:utf-8 -*

import select
from threading import Thread


class ClientDisplay(Thread):

    """Thread test"""

    def __init__(self, serv_connec):
        self.serv_connec = serv_connec
        Thread.__init__(self)

    def run(self):
        """Code à exécuter dans le thread test"""

        is_running = True
        while is_running:

            try:
                (clients_a_lire,
                 wlist,
                 rlist,
                 ) = select.select([self.serv_connec], [], [], 0.05)
            except select.error:
                pass
            else:
                # On parcourt la liste des clients à lire
                inmsg = self.serv_connec.recv(1024)
                inmsg = inmsg.decode()

                if inmsg in ('end'):
                    is_running = False
                elif inmsg != '':
                    print(inmsg)


class ClientInput(Thread):

    """Thread chargé d'envoyer les instructions client au serveur"""

    def __init__(self, serv_connec):
        self.serv_connec = serv_connec
        Thread.__init__(self)

    def run(self):
        """Code à exécuter dans le thread d'input"""

        is_running = True

        outmsg = ''
        while is_running:
            outmsg = input()
            if outmsg.lower() == "quit":
                is_running = False
            else:
                outmsg = outmsg.encode()
                self.serv_connec.send(outmsg)
