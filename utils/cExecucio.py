
try:
    from time import sleep
    from datetime import datetime as dt
    from utils.cConnexio import cConnexio as cCon
    from utils.cFils import cFils as cF
except Exception as e:
    raise e

class cExecucio(object):
    def __init__(self,**jKerExe):
        # guardem el kernel de l'execucio, que la identifica unicament
        self.jKerExe = jKerExe
        self.tProjecte = jKerExe['tProjecte']
        self.tUsuari = jKerExe['tUsuari']
        self.tCredencials = jKerExe['tCredencials']

        self.filPet = {}

        self.pIniParams()
        self.pInsExecucio()

    def pIniParams(self):

        try:

            self.nId = int(dt.now().strftime('%Y%m%d%H%M%S'))
            self.jKerExe['nExeId'] = self.nId
            self.conDb = cCon(self.jKerExe)

            self.jEstats = self.conDb.fConsulta('con',{ 'config': 'estats'},0)[0]['data']
            self.jProjectes = self.conDb.fConsulta('con',{ 'config': 'projectes'},0)[0]['data']
            self.jUsuaris = self.conDb.fConsulta('con',{ 'config': 'usuaris'},0)[0]['data']
            self.jExeConfig = self.conDb.fConsulta('con',{ 'config': 'exeConfig'},0)[0]['data']
            self.jPetConfig = self.conDb.fConsulta('con',{ 'config': 'petConfig'},0)[0]['data']

            self.nEstat = self.jEstats['ExeIniciat']['nEstat']

            self.dInici = dt.now()
            self.dFi = dt.now()

            self.nVoltesBuides = 0
            self.nPetAgafar = self.jPetConfig['nPetAgafar']
            self.nPetSleep = self.jPetConfig['nPetSleep']
            self.bSeguirBuscant = True
            self.bSeguirExecutant = True

            # data_inici, data_final esperada, us_recursos, sleeps!
            # agafar config de: BD - obrador, colec - config

        except Exception as e:
            raise e

    def pInsExecucio(self):
        try:
            jExe = self.fJExe()
            jLog = self.fJLog()
            jErr = self.fJErr()
            jResultat1 = self.conDb.fInsertarUn('exe',jExe)
            jResultat2 = self.conDb.fInsertarUn('log',jLog)
            jResultat3 = self.conDb.fInsertarUn('err',jErr)
        except Exception as e:
            raise e

    def fJExe(self):
        try:
            jExe = { 'nId': self.nId, 'dInici': self.dInici, 'dFi': self.dFi, 'nEstat': self.nEstat, 'tProjecte': self.tProjecte }
            return jExe
        except Exception as e:
            raise e

    def fJLog(self):
        try:
            jLog = { 'nExeId': self.nId, 'log': [], 'tProjecte': self.tProjecte }
            return jLog
        except Exception as e:
            raise e

    def fJErr(self):
        try:
            jErr = { 'nExeId': self.nId, 'err': [], 'tProjecte': self.tProjecte }
            return jErr
        except Exception as e:
            raise e

    def fInsertarLogExe(self,tPunt,tMissatge):
        try:
            jLog = { 'dData': dt.now(), 'tPunt': tPunt, 'tMissatge': tMissatge }
            jCond = { 'nExeId': self.nId }
            jAfegir = { '$push': { 'log': jLog } }
            jResultat = self.conDb.fActualitzar('log',jCond,jAfegir)
            return jResultat
        except Exception as e:
            raise e

    def fInsertarErr(self,nCodErr,tPunt,tMissatge):
        try:
            jErr = { 'dData': dt.now(), 'nCodErr': nCodErr, 'tPunt': tPunt, 'tMissatge': tMissatge }
            jCond = { 'nExeId': self.nId }
            jAfegir = { '$push': { 'err': jErr } }
            jResultat = self.conDb.fActualitzar('err',jCond,jAfegir)
            return jResultat
        except Exception as e:
            raise e

    def pGestorExecucio(self):
        try:
            self.fInsertarLogExe('pGestorExecucio.inici','Iniciat gestor execucions.')
            self.nVoltesGestorExe = 0
            while bSeguirExecutant:
                self.nVoltesGestorExe += 1
                self.pRecursos()
                self.pAjustarGestorExe()
                sleep(self.jExeConfig['nExeSleep'])
                self.fInsertarLogExe('pGestorExecucio.volta','Volta: ' + str(self.nVoltesGestorExe))

            self.fInsertarLogExe('pGestorExecucio.final','Finalitzat gestor execucions.')
        except Exception as e:
            raise e

    def pGestorPeticions(self):

        try:

            self.fInsertarLogExe('pGestorPeticions.inici','Iniciat gestor peticions.')

            self.nVoltesGestorPet = 0
            while self.bSeguirBuscant:

                self.nVoltesGestorPet += 1
                lPet = self.fPetPend()
                self.nPetsAgafades = lPet.count()
                self.fInsertarLogExe('pGestorPeticions.pendents','Volta: ' + str(self.nVoltesGestorPet) + ', Pendents: ' + str(lPet.count()))

                for p in lPet:
                    self.pActPetEstat(p,'PetAgafada')
                    self.pExePet(p)

                self.pAjustarGestorPet()
                sleep(self.nPetSleep)
                self.fInsertarLogExe('pGestorPeticions.volta','Volta: ' + str(self.nVoltesGestorPet) + ' acabada')

            self.fInsertarLogExe('pGestorPeticions.final','Finalitzat gestor peticions.')

        except Exception as e:
            raise e

    def pAjustarGestorExe(self):
        # decidir si seguim amb l'execucio
        #  si fa estona que no fa res
        #  si no ens queden recursos...
        # ajustar altres vars-config
        try:
            self.fInsertarLogExe('pAjustarGestorExe.inici','Inici ajustament gestor execucions a volta ' + str(self.nVoltesGestorExe) + '.')
            if self.nVoltesGestorExe > 5:
                self.bSeguirExecutant = False
                self.fInsertarLogExe('pAjustarGestorExe.final','Finalitzat ajustament gestor execucions, queda ' + str(self.bSeguirExecutant) + '.')
        except Exception as e:
            raise e

    def pAjustarGestorPet(self):
        try:
            self.fInsertarLogExe('pAjustarGestorPet.inici','Inici ajustament gestor peticions a volta ' + str(self.nVoltesGestorPet) + '.')
            self.jPetConfig = self.conDb.fConsulta('con',{ 'config': 'petConfig'},0)[0]['data']

            if self.jPetConfig['bApagar']: # or dt.now() = self.jPetConfig['dApagar']:
                self.bSeguirBuscant = False
                return

            if self.nPetsAgafades == 0:
                self.nVoltesBuides += 1
                self.nPetSleep += 1
            elif self.nPetsAgafades > 0:
                self.nVoltesBuides = 0

            if self.nVoltesBuides > self.jPetConfig['nMaxVoltesBuidesPet']:
                self.bSeguirBuscant = False
                return

            if self.nVoltesGestorPet > self.jPetConfig['nMaxVoltesPet']:
                self.bSeguirBuscant = False
                return

            self.fInsertarLogExe('pAjustarGestorPet.final','Finalitzat ajustament gestor peticions, queda ' + str(self.bSeguirBuscant) + '.')

        except Exception as e:
            raise e

    def pActExeEstat(self,tExeEstat):
        try:
            self.fInsertarLogExe('pActExeEstat','Nou estat: ' + str(tExeEstat))
            jCond = { 'nId': self.nId }
            jCanvi = { '$set': { 'nEstat': self.jEstats[tExeEstat]['nEstat'] }#, '$currentDate': {'lastModified': { '$type': 'timestamp'}}
            }
            self.conDb.fActualitzar('exe',jCond,jCanvi)
        except Exception as e:
            raise e

    def pActPetEstat(self,jPet,tPetEstat):
        try:
            self.fInsertarLogExe('pActPetEstat','Peticio: ' + str(jPet['_id']))
            jCond = { '_id': jPet['_id'] }
            jCanvi = { '$set': { 'nEstat': self.jEstats[tPetEstat]['nEstat'] }#, '$currentDate': {'lastModified': { '$type': 'timestamp'}}
                }
            self.conDb.fActualitzar('pet',jCond,jCanvi)
        except Exception as e:
            raise e

    def pExePet(self,jPet):
        try:
            self.fInsertarLogExe('pExePet','Peticio: ' + str(jPet['_id']))
            self.filPet[str(jPet['_id'])] = cF( jPet['tLib'], jPet['tMet'], jPet, self.jKerExe )
            self.filPet[str(jPet['_id'])].start()
        except Exception as e:
            raise e

    def fPetPend(self):
        try:
            if self.tProjecte == 'obrador':
                jCond = { 'nEstat': 10 }
            else:
                jCond = { 'nEstat': 10, 'tProjecte': self.tProjecte }
            lPet = self.conDb.fConsulta('pet',jCond,self.jPetConfig['nPetAgafar'])
            return lPet
        except Exception as e:
            raise e

    def fJPet(self,tProjecte,tLib,tMet,tData,jParams,nEstat):
        try:
            jPet = { 'tProjecte': tProjecte, 'tLib': tLib, 'tMet': tMet, 'tData': tData, 'jParams': jParams, 'nEstat': nEstat, 'lLog': [] }
            return jPet
        except Exception as e:
            raise e

    def fInsJPet(self,jPet):
        try:
            jResultat = self.conDb.fInsertarUn('pet',jPet)
            return jResultat
        except Exception as e:
            raise e

    def fNetejaDb(self):
        try:
            self.conDb.fEliminarCollection('pet')
            self.conDb.fEliminarCollection('exe')
            self.conDb.fEliminarCollection('log')
        except Exception as e:
            raise e
