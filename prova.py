
from utils.cConnexio import cConnexio as cCo
from datetime import datetime as dt
import sys

jKerExe = {}
jKerExe['nExeId'] = 0
jKerExe['tProjecte'] = sys.argv[1]
jKerExe['tUsuari'] = sys.argv[2]
jKerExe['tCredencials'] = sys.argv[3]

conDB = cCo(jKerExe)

jEstats = conDB.fConsulta('con',{ 'config': 'estats'},0)[0]

jParams1 = {
	'tTipus': 'captura twitter',
	'tRest': 'statuses/user_timeline',
	'nSleep': 1,
	'jArgs': { 'screen_name': 'quimmonzo', 'count': 50 },
	'tDesti': 'dest_monzo'
	}

jPet = { 'tProjecte': 'prova', 'tLib': 'cCapTwi', 'tMet': 'pExecuta', 'tData': dt.now(), 'jParams': jParams1, 'nEstat': jEstats['data']['PetPendent']['nEstat'], 'lLog': [] }

conDB.fInsertarUn('pet',jPet)
