import atexit
import os

_xvfb = None

def start_xvfb():
  from xvfbwrapper import Xvfb
  global _xvfb
  if "DISPLAY" in os.environ:
    del os.environ["DISPLAY"]
  _xvfb = Xvfb()
  _xvfb.start()
  atexit.register(_xvfb.stop)

def stop_xvfb():
  global _xvfb
  _xvfb.stop()
