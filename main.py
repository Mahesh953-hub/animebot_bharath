import sys

if sys.platform != "win32":
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass

from bot import Bot

Bot().run()
