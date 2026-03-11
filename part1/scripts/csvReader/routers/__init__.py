from .arista import Arista
from .nokia import Nokia
from .mikrotik import MikroTik

ROUTERS = {
    'arista_eos': Arista(),
    'nokia_srl': Nokia(),
    'mikrotik_routeros': MikroTik()
}