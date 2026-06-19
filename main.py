import sys
import asyncio

if sys.platform != "win32":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        asyncio.set_event_loop(asyncio.new_event_loop())
    except ImportError:
        pass

from bot import Bot

Bot().run()
