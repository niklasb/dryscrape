import atexit
import os
from xvfbwrapper import Xvfb

xvfb = Xvfb()

def start_xvfb():
  if "DISPLAY" in os.environ:
    del os.environ["DISPLAY"]
  xvfb.start()
  atexit.register(xvfb.stop)

def stop_xvfb():
	if "DISPLAY" in os.environ:
		xvfb.stop()
		del os.environ["DISPLAY"]
