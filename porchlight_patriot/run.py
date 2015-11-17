import time
import signal, os, sys
import logging
from phue import Bridge
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

b = Bridge('192.168.1.111')
b.connect()

transtime = 30
bright = 80

def change_white():
  lightargs = {'transitiontime':transtime, 'on': True, 'bri': bright, 'ct': 175}
  b.set_light(5, lightargs)

def change_red():
  lightargs = {'transitiontime':transtime, 'on': True, 'bri': bright, 'hue': 0, 'sat': 254}
  b.set_light(5, lightargs)

def change_blue():
  lightargs = {'transitiontime':transtime, 'on': True, 'bri': bright, 'hue': 46920, 'sat': 254}
  b.set_light(5, lightargs)

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    logger.info(time.strftime('%x %X %Z')+': Going down for a nap...')
    b.set_light(5, 'on', False)
    self.kill_now = True

if __name__ == '__main__':
  logger.info(time.strftime('%x %X %Z')+': Starting light sequence')
  killer = GracefulKiller()
  while True:
    # Go white
    change_white()
    time.sleep(8)
    if b.get_light(5, 'on') == False:
      break
    elif killer.kill_now:
      break

    # Go red
    change_red()
    time.sleep(8)
    if b.get_light(5, 'on') == False:
      break
    elif killer.kill_now:
      break

    # Go blue
    change_blue()
    time.sleep(8)
    if b.get_light(5, 'on') == False:
      break
    elif killer.kill_now:
      break

  logger.info(time.strftime('%x %X %Z')+": We're done here!")
