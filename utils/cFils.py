
import threading
import importlib

class cFils(threading.Thread):

    def __init__(self, tObj,tMet,jPet,jKerExe):
        threading.Thread.__init__(self)
        self.tObj = tObj
        self.tMet = tMet
        self.jPet = jPet
        self.jKerExe = jKerExe

    def run(self):
        cImp = importlib.import_module('moduls.' + self.tObj + '.' + self.tObj)
        cObj = getattr(cImp,self.tObj)
        cIns = cObj(self.jPet,self.jKerExe)
        fMet = getattr(cIns,self.tMet)
        fMet()
