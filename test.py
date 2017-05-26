# -*-coding:utf-8 -*

import random
import time
import sys
from threading import Thread

class afficheur(Thread):

	def __init__(self, lettre):
		Thread.__init__(self)
		self.lettre = lettre

	def run(self):

		i = 0
		while i<20:
			sys.stdout.write(self.lettre)
			sys.stdout.flush()
			att = 0.2
			att += random.randint(1,60) /100
			time.sleep(att)
			i+=1

thread_1 = afficheur("1")

thread_2 = afficheur("2")


# Lancement des threads

thread_1.start()

thread_2.start()


# Attend que les threads se terminent

thread_1.join()

thread_2.join()