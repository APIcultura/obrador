
# primer input: el nom del projecte
# segon input: el nom de l'usuari
# tercer input: les credencials en el formta entorn-basedades
 ## si treballes en local, posaràs: local-obrador
 ## si ets a l'openshift, posaràs: openshift-obrador
 ## si apuntes a una base de dades diferent, substituiràs obrador pel que sigui: local-un_altre_nom_de_la_base_de_dades

# exemples execucio:
## python3 obrador.py analisiDiputats orpuig local-obrador
## python3 obrador.py processatTfIDF espinacs openshift-obrador
## python3 obrador.py puntualitatAnglesa catbru openshift-obradorProva

from utils.cExecucio import cExecucio
import sys

exe = cExecucio(tProjecte=sys.argv[1],tUsuari=sys.argv[2],tCredencials=sys.argv[3])
exe.pGestorPeticions()
