
try:
    import os
    import pymongo
except Exception as e:
    raise e

class cConnexio(object):

    def __init__(self,jKerExe):

        self.tExeId = jKerExe['nExeId']
        self.tProjecte = jKerExe['tProjecte']
        self.tUsuari = jKerExe['tUsuari']

        self.tCredencials = jKerExe['tCredencials']
        self.tEntorn = self.tCredencials.split('-')[0]
        self.tDb = self.tCredencials.split('-')[1]

        self.pConnectar()


    def pConnectar(self):
        if self.tEntorn == 'local':
            self.conClient = pymongo.MongoClient()
            self.conDb = self.conClient[self.tDb]
        elif self.tEntorn == 'openshift':
            self.conClient = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST'],int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))
            self.conDb = self.conClient[os.environ['OPENSHIFT_APP_NAME']]
            self.conDb.authenticate(os.environ['OPENSHIFT_MONGODB_DB_USERNAME'],os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'])

    def pDesconnectar(self):
        del self.conClient

    def fInsertarUn(self,tColec,jDoc):
        jResultat = self.conDb[tColec].insert(jDoc)
        return jResultat

    def fInsertarVaris(self,tColec,jDocs):
        jResultat = self.conDb[tColec].insert_many(jDocs)
        return jResultat

    def fEliminarUn(self,tColec,jCond):
        jResultat = self.conDb[tColec].delete_one(jCond)
        return jResultat

    def fActualitzar(self,tColec,jCond,jCanvi):
        jResultat = self.conDb[tColec].update(jCond,jCanvi)
        return jResultat

    def fSusbstituir(self,tColec,jCond,jNou):
        jResultat = self.conDb[tColec].replace(jCond,jNou)
        return jResultat

    def fConsulta(self,tColec,jCond,nLim):
        if nLim < 1 or nLim is None:
            nLim = 0
        jResultat = self.conDb[tColec].find(jCond).limit(nLim)
        return jResultat

    def fConsultaLim(self,tColec,jCond,jLim):
        jResultat = self.conDb[tColec].find(jCond,jLim)
        return jResultat

    def fConsIAct(self,tColec,jCond,jCanvi):
        jResultat = self.conDb[tColec].find_one_and_update(jCond,jCanvi,projection=None,sort=None)#,return_document=ReturnDocument.AFTER)
        return jResultat

    def fConsCount(self,tColec,jCond):
        jResultat = self.conDb[tColec].find(jCond).count()
        return jResultat

    def fCollections(self):
        jResultat = self.conDb.collection_names(include_system_collections=False)
        return jResultat

    def fEliminarCollection(self,tColec):
        jResultat = self.conDb[tColec].drop()
        return jResultat
