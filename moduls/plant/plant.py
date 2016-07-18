
from time import sleep
from utils.cPeticio import cPeticio as cPet

class plant(cPet):
    def __init__(self, jPet, jKerExe):
        print('iniciada la prova')
        self.p = 2
        self.num = '2'

    def plant(self):
        print('mes!' + self.num)
        sleep(self.p)
        print('mes2!' + self.num)
        sleep(self.p)
        print('mes3!' + self.num)
        sleep(2)
        print('mes4!' + self.num)
