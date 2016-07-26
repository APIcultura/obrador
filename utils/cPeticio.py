
try:
    from utils.cConnexio import cConnexio as cCon
    from time import sleep
    from datetime import datetime as dt
except Exception as e:
    raise e

class cPeticio(object):

    def __init__(self,jPet,jKerExe):

        self.jPet = jPet
        self.jKerExe = jKerExe

        self.nExeId = jKerExe['nExeId']
        self.tProjecte = jKerExe['tProjecte']
        self.tUsuari = jKerExe['tUsuari']
        self.tCredencials = jKerExe['tCredencials']

        self.jParams = self.jPet['jParams']

        self.pIniParams()
        self.pCompDep()


    def pIniParams(self):

        try:

            self.conDb = cCon(self.jKerExe)

            self.jEstats = self.conDb.fConsulta('con',{ 'config': 'estats'},0)[0]['data']
            #self.jProjectes = self.conDb.fConsulta('con',{ 'config': 'projectes'})[0]['data']
            #self.jUsuaris = self.conDb.fConsulta('con',{ 'config': 'usuaris'})[0]['data']
            self.jExeConfig = self.conDb.fConsulta('con',{ 'config': 'exeConfig'},0)[0]['data']
            self.jPetConfig = self.conDb.fConsulta('con',{ 'config': 'petConfig'},0)[0]['data']

        except Exception as e:
            raise e

    def pCompDep(self):
        # de Comprovar Dependencia

        try:
            bPend = 'tDepend' in self.jParams
            while bPend:
                jPetDep = self.conDb.fConsulta('pet',{ '_id': self.jParams['tDepend']},0)
                bPend = jPetDep['nEstat'] == 40
                if not bPend:
                    return True
                sleep(1)

        except Exception as e:
            raise e


    def fInsertarLogExe(self,tPunt,tMissatge):
        try:
            jLog = { 'dData': dt.now(), 'tPunt': tPunt, 'tMissatge': tMissatge }
            jCond = { 'nExeId': self.nExeId }
            jAfegir = { '$push': { 'log': jLog } }
            jResultat = self.conDb.fActualitzar('log',jCond,jAfegir)
            return jResultat
        except Exception as e:
            raise e


    def fInsertarLogPet(self,tPunt,tMissatge):
        try:
            jLog = { 'dData': dt.now(), 'tPunt': tPunt, 'tMissatge': tMissatge }
            jCond = { '_id': self.jPet['_id'] }
            jAfegir = { '$push': { 'log': jLog } }
            jResultat = self.conDb.fActualitzar('pet',jCond,jAfegir)
            return jResultat
        except Exception as e:
            raise e


    def fInsertarErr(self,nCodErr,tPunt,tMissatge):
        try:
            jErr = { 'dData': dt.now(), 'nCodErr': nCodErr, 'tPunt': tPunt, 'tMissatge': tMissatge }
            jCond = { 'nExeId': self.nExeId }
            jAfegir = { '$push': { 'err': jErr } }
            jResultat = self.conDb.fActualitzar('err',jCond,jAfegir)
            return jResultat
        except Exception as e:
            raise e


    def pActExeEstat(self,tExeEstat):
        try:
            self.fInsertarLog('pActExeEstat','Nou estat: ' + str(tExeEstat))
            jCond = { 'nId': self.nExeId }
            jCanvi = { '$set': { 'nEstat': self.jEstats[tExeEstat]['nEstat'] }#, '$currentDate': {'lastModified': { '$type': 'timestamp'}}
            }
            self.conDb.fActualitzar('exe',jCond,jCanvi)
        except Exception as e:
            raise e


    def pActPetEstat(self,jPet,tPetEstat):
        try:
            self.fInsertarLogExe('pActPetEstat','Peticio: ' + str(self.jPet['_id']))
            jCond = { '_id': self.jPet['_id'] }
            jCanvi = { '$set': { 'nEstat': self.jEstats[tPetEstat]['nEstat'] }#, '$currentDate': {'lastModified': { '$type': 'timestamp'}}
            }
            self.conDb.fActualitzar('pet',jCond,jCanvi)
        except Exception as e:
            raise e


    def fJPet(self,tProjecte,tLib,tMet,tData,jParams,nEstat):
        try:
            jPet = { 'tProjecte': tProjecte, 'tLib': tLib, 'tMet': tMet, 'tData': tData, 'jParams': jParams, 'nEstat': nEstat, 'lLog': {} }
            return jPet
        except Exception as e:
            raise e


    def fInsJPet(self,jPet):
        try:
            jResultat = self.conDb.fInsertarUn('pet',jPet)
            return jResultat
        except Exception as e:
            raise e

    def pInsPetSeguent(self):
        if 'jPetSeg' in self.jParams:
            jPetSeg = self.jParams['jPetSeg']
            self.fInsJPet(self.fJPet( self.tProjecte,jPetSeg['tLib'],jPetSeg['tMet'],dt.now(),jPetSeg['jParams'],10))
            