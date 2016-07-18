
from utils.cConnexio import cConnexio as cCo
import sys
import json
from datetime import datetime as dt
from datetime import timedelta as td

jKerExe = {}
jKerExe['nExeId'] = 0
jKerExe['tProjecte'] = sys.argv[1]
jKerExe['tUsuari'] = sys.argv[2]
jKerExe['tCredencials'] = sys.argv[3]

conDB = cCo(jKerExe)

conDB.fEliminarCollection('CapTwiCon')
conDB.fEliminarCollection('CapTwiSit')


with open('moduls/cCapTwi/conf/config.json') as config:
	jConfig = json.load(config)

with open('moduls/cCapTwi/conf/claus.json') as claus:
    jClaus = json.load(claus)

with open('moduls/cCapTwi/conf/getRests.json') as getRests:
    jGetRests = json.load(getRests)

with open('moduls/cCapTwi/conf/postRests.json') as postRests:
    jPostRests = json.load(postRests)


conDB.fInsertarUn('CapTwiCon',jGetRests)
conDB.fInsertarUn('CapTwiCon',jPostRests)
conDB.fInsertarUn('CapTwiCon',jClaus)


jSituacions = {}
i = 0
for r in jGetRests['data']:
	for c in jClaus['data']:
		jSituacions[str(i)] = {
			'tRest': r, 'tClau': c,
			'nQuedenUsr': jGetRests['data'][r]['nLimUsr'],
			'nQuedenApp': jGetRests['data'][r]['nLimApp'],
			'dUltima': dt.now() - td(minutes=15)
		}
		i += 1

for s in jSituacions:
	conDB.fInsertarUn('CapTwiSit',jSituacions[s])
