
from utils.cConnexio import cConnexio as cCo
import sys
import json

jKerExe = {}
jKerExe['nExeId'] = 0
jKerExe['tProjecte'] = sys.argv[1]
jKerExe['tUsuari'] = sys.argv[2]
jKerExe['tCredencials'] = sys.argv[3]

conDB = cCo(jKerExe)

conDB.fEliminarCollection('con')
conDB.fEliminarCollection('exe')
conDB.fEliminarCollection('pet')
conDB.fEliminarCollection('log')
conDB.fEliminarCollection('err')
conDB.fEliminarCollection('dest')

with open('conf/errors.json') as errors:
    jErrors = json.load(errors)

with open('conf/estats.json') as estats:
    jEstats = json.load(estats)

with open('conf/projectes.json') as projectes:
    jProjectes = json.load(projectes)

with open('conf/usuaris.json') as usuaris:
    jUsuaris = json.load(usuaris)

with open('conf/fonts.json') as fonts:
    jFonts = json.load(fonts)

with open('conf/exeConfig.json') as exeConfig:
    jExeConfig = json.load(exeConfig)

with open('conf/petConfig.json') as petConfig:
    jPetConfig = json.load(petConfig)

conDB.fInsertarUn('con',jErrors)
conDB.fInsertarUn('con',jEstats)
conDB.fInsertarUn('con',jProjectes)
conDB.fInsertarUn('con',jUsuaris)
conDB.fInsertarUn('con',jFonts)
conDB.fInsertarUn('con',jExeConfig)
conDB.fInsertarUn('con',jPetConfig)
