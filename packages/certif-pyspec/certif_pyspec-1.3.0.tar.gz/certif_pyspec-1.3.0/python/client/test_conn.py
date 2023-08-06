
from pyspec.client.SpecConnection import SpecConnection, QSpecConnection
from pyspec.css_logger import log
from pyspec.client.spec_updater import spec_updater
from pyspec.utils import async_loop
import time

from pyspec.client import spec
spec = spec("toto")

updater = spec_updater()
updater.start()

while True:
   spec.run_cmd("testcnt 1;")
   time.sleep(0.1)

"""
global s

def run_mac():
    global s
    answ = s.run_cmd("graph toto;")
    log.log(2, "got answer %s" % answ)

def update_conn():
    global s
    async_loop() 
    if not s.is_connected():
        log.log(2, "not connected")
    s.update_events()

s = QSpecConnection("toto")

time.sleep(2)

while True:
   run_mac()
   time.sleep(1)



"""
