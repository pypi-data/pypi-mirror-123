
from pyspec.client import SpecConnection
from pyspec.client.SpecCommand import SpecCommandA
import time

sp = SpecConnection('toto')
cmd = SpecCommandA(sp,'testcnt')

def titi(value):
    cmd(value)
