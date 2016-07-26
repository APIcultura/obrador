
try:
	from birdy.twitter import UserClient
	from birdy.twitter import AppClient
	from datetime import datetime as dt
	from datetime import timedelta as td

	from utils.cPeticio import cPeticio as cPet
	from time import sleep
	import json, ast

except Exception as e:
	print(e)
	#TODO: posar al log del sistema...

class cCapTwi(cPet):

	def pExecuta(self):

		self.pActPetEstat(self.jPet,'PetProcess')

		self.fInsertarLogPet('pExecuta.inici','Iniciem la execucio de la captura')

		# tenir el codi peticio en una variable
		tPetId = str(self.jPet['_id'])

		if 'tRecur' in self.jParams:
			if self.jParams['tRecur'] == None:
				jResultat = self.pCapSimple()
			else:
				jResultat = self.pCapRecursiva()
		else:
			jResultat = self.pCapSimple()

		# actualitzar l'estat de la peticio abans d'acabar
		if jResultat['estat'] == 'ok':
			self.pActPetEstat(self.jPet,'PetFinExit')
		else:
			self.pActPetEstat(self.jPet,'PetFinFrac')

		#TODO: traslladar aixo a cPeticio, self.pInsPetSeguent()
		if 'jPetSeg' in self.jParams:
			jPetSeg = self.jParams['jPetSeg']
			self.fInsJPet(self.fJPet( self.tProjecte,jPetSeg['tLib'],jPetSeg['tMet'],dt.now(),jPetSeg['jParams'],10))


	def pCapSimple(self):

		tRest = self.jParams['tRest']
		jClaus = self.pCrearClient(tRest,'app')

		oPreg = self.cClient.api
		for r in self.fSeparaPunt(tRest):
			oPreg = oPreg[r]
		oResposta = oPreg.get(**self.jParams['jArgs']) # aqui entrem self.jParams['jArgs']


		if oResposta.headers['status'] != '200 OK':
			print('Aha! Algun error!')
			#TODO: insertar el error a db

		self.fActClaus(tRest,jClaus['tId'],oResposta.headers['x-rate-limit-remaining'])

		# guardem a Db
		jGuardar = { 'nExeId': self.nExeId, 'jPet': self.jPet, 'jHeaders': oResposta.headers, 'jData': oResposta.data }
		self.pGuardarData(jGuardar,self.jParams['tDesti'])

		oResposta.jResposta = {}
		oResposta.jResposta['tEstat'] = 'ok'

		# no hi ha una resposta estandar per la recursiva!
		# per exemple, amb statuses/user_timeline el oResposta.data es una llista de tuits
		# en canvi, amb search/tweets el oResposta.data es un json que te un camp 'statuses' que es un a llista de tuits
		# no sabem com es friends/ids o friends/list per exemple...

		bTeTuits = tRest in ['search/tweets','statuses/home_timeline','statuses/user_timeline']

		'''
		if tRest == 'search/tweets':

		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		elif tRest == '':
		else:
		print('ERROR: REST no reconeguda!')
		'''

		if 'previous_cursor' in oResposta.data:
			oResposta.jResposta['previous_cursor'] = oResposta.data['previous_cursor']
			oResposta.jResposta['previous_cursor_str'] = oResposta.data['previous_cursor_str']
			oResposta.jResposta['next_cursor'] = oResposta.data['next_cursor']
			oResposta.jResposta['next_cursor_str'] = oResposta.data['next_cursor_str']
			oResposta.jResposta[self.jParams['tRecur']] = oResposta.jResposta['next_cursor']
			oResposta.jResposta['nElemCap'] = len(oResposta.data['ids'])
		elif bTeTuits:
			# COMPTE, aquests max i min no crec que ho facin be...

			if ( 'statuses' in oResposta.data ) and ( len(oResposta.data['statuses']) > 0 ):
				oResposta.jResposta['max_id'] = oResposta.data['statuses'][-1]['id'] - 1
				oResposta.jResposta['since_id'] = oResposta.data['statuses'][0]['id'] + 1
				oResposta.jResposta['nElemCap'] = len(oResposta.data['statuses'])
			elif len(oResposta.data) > 0:
				oResposta.jResposta['max_id'] = oResposta.data[-1]['id'] - 1
				oResposta.jResposta['since_id'] = oResposta.data[0]['id'] + 1
				oResposta.jResposta['nElemCap'] = len(oResposta.data)
				# max([t['id_str'] for t in oResposta.data])
		else:
			oResposta.jResposta[self.jParams['tRecur']] = ''
			oResposta.jResposta['nElemCap'] = 0

		# que pot passar?
		# arriben dades, tot ok
		# arriben dades, buides
		# arriba error claus
		# arriba error no de claus
		# que s'ha de fer?
		# actualitzar estat/log peticio
		# actualitzar CapTwiSit
		#

		# a.Actualitzar estat peticio
		self.nEstat = 70

		# b.Actualitzar situacio claus
		# nQuedenUsr/App posar el min( oResposta.headers['remainingwhatever'] , 'el que hi ha a DB' )

		return oResposta.jResposta


	def pCapRecursiva(self):

		dAra = dt.now()

		bSeguir = True
		tRecur = self.jParams['tRecur']
		jResultat = {}

		while bSeguir:

			jResposta = self.pCapSimple()

			if tRecur in self.jParams['jArgs']:
				# ajustem el valor del cursor per a la seguent captura
				self.jParams['jArgs'][tRecur] = jResposta[tRecur]
			else:
				# si es el primer cop, posem el camp tRecur per seguir la recursiva
				self.jParams['jArgs'][tRecur] = jResposta[tRecur] # entenend .append(index,element)

			if jResposta['tEstat'] == 'ok':
				jResultat['estat'] = 'ok'
			else:
				jResultat['estat'] = 'ko'
				return jResultat

			# aixo hauria de estar molt mes treballat!!!
			if jResposta['nElemCap'] == 0 or jResposta[tRecur] == '' or jResposta[tRecur] == 0:
				bSeguir = False
			else:
				bSeguir = True


		nTempsTardat = dt.now()-dAra
		#TODO: instertar-ho a algun lloc bonic

		return jResultat

	def pCapStream(self):
		print('Procediment per capturar amb streaming')
		self.pActPetEstat(self.jPet,'PetFinExit')


	def pCrearClient(self,tRest,tTipus):

		jClaus = self.fClaus(tRest)

		if tTipus == 'user':
			self.cClient = UserClient(jClaus['ConsumerKey'],jClaus['ConsumerSecret'], jClaus['AccessToken'], jClaus['AccessTokenSecret'] )
		elif tTipus == 'app':
			self.cClient = AppClient(jClaus['ConsumerKey'],jClaus['ConsumerSecret'] )
			tAccessToken = self.cClient.get_access_token()
			self.cClient = AppClient(jClaus['ConsumerKey'],jClaus['ConsumerSecret'], tAccessToken )

		return jClaus


	def pGuardarData(self,jGuardar,tDesti):
		self.conDb.fInsertarUn(tDesti,jGuardar)


	def fSeparaPunt(self,tRest):
		#return re.sub(r'([a-z]*)([A-Z])',r'\1 \2',s)
		#return re.findall('[A-Z][^A-Z]*', s)
		return tRest.split('/')

	def fClaus(self,tRest):
		bTrobat = True
		while bTrobat:
			jCond = { 'tRest': tRest, '$or': [ {'nQuedenApp': { '$gt': 0 }}, {'dUltima': { '$lt': dt.now() - td(minutes=15) }} ] }
			jCanvi = { '$inc': { 'nQuedenApp': -1 }, '$set': { 'dUltima': dt.now() } }

			jResultat = self.conDb.fConsIAct('CapTwiSit',jCond,jCanvi)

			if jResultat is not None:
				bTrobat = False

		jCond2 = { 'config' : 'claus' }
		jLim = { 'data.'+jResultat['tClau']: 1}
		jResultat2 = self.conDb.fConsultaLim('CapTwiCon',jCond2,jLim)

		return jResultat2[0]['data'][jResultat['tClau']]

	def fActClaus(self,tRest,tClau,nLimitRemaining):
		jCond = { 'tRest': tRest, 'tClau': tClau}
		jCanvi = { '$min': { 'nQuedenApp': nLimitRemaining }, '$set': {'dUltima': dt.now()} }
		self.conDb.fActualitzar('CapTwiSit',jCond,jCanvi)

	def pOrdenar(self,jPet,jSistema):

		if jPet['jParams']['tRest'] == 'statuses/user_timeline':

			if jSistema['statuses/user_timeline'] == 'cru':
				jPet = self.conDb.fConsulta(jPet['jParams']['tDesti'],{ 'jPet' : { '_id': jPet['_id']} } )
				self.conDB.fInsertarVaris(jSistema['tuits'],jPet['jData'])

			if jSistema['bBorrar']:
				self.conDB.fEliminarUn(jPet['jParams']['tDesti'],{ 'jPet' : { '_id': jPet['_id']} } )

		elif jPet['jParams']['tRest'] == 'friends/ids':
			if jSistema['friends/ids'] == 'cru':
				jPet = self.conDb.fConsulta(jPet['jParams']['tDesti'],{ 'jPet' : { '_id': jPet['_id']} } )

		elif jPet['jParams']['tRest'] == 'followers/ids':
			jPet = self.conDb.fConsulta(jPet['jParams']['tDesti'],{ 'jPet' : { '_id': jPet['_id']} } )
