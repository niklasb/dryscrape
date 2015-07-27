import atexit
import os

def start_xvfb():
  from xvfbwrapper import Xvfb
  if "DISPLAY" in os.environ:
    del os.environ["DISPLAY"]
  xvfb = Xvfb()
  xvfb.start()
  atexit.register(xvfb.stop)
