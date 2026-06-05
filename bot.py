#(©)Codexbotz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import (
    API_HASH, 
    APP_ID, 
    LOGGER, 
    TG_BOT_TOKEN, 
    TG_BOT_WORKERS, 
    FORCE_SUB_CHANNEL, 
    CHANNEL_ID, 
    PORT
)
from keepalive import KeepAliveManager

ascii_art = """
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
"""


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER
        self._keepalive: KeepAliveManager | None = None

    async def start(self):
        await super().start()

        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        self.username = usr_bot_me.username

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    "Bot can't Export Invite link from Force Sub Channel!"
                )
                self.LOGGER(__name__).warning(
                    "Please Double check the FORCE_SUB_CHANNEL value and Make sure "
                    "Bot is Admin in channel with Invite Users via Link Permission, "
                    "Current Force Sub Channel Value: %s", FORCE_SUB_CHANNEL
                )
                self.LOGGER(__name__).info(
                    "\nBot Stopped. Join https://t.me/CodeXBotzSupport for support"
                )
                sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                "Make Sure bot is Admin in DB Channel, and Double check the "
                "CHANNEL_ID Value, Current Value %s", CHANNEL_ID
            )
            self.LOGGER(__name__).info(
                "\nBot Stopped. Join https://t.me/CodeXBotzSupport for support"
            )
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(
            "Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz"
        )
        print(ascii_art)
        print("""Welcome to CodeXBotz File Sharing Bot""")

        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        await super().stop()

        self._keepalive = KeepAliveManager(
            client=self,
            heartbeat_interval=300,
            reconnect_delay=5,
        )
        await self._keepalive.run()

    async def stop(self, *args):
        if self._keepalive:
            self._keepalive.request_shutdown()
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")



if __name__ == "__main__":
    bot = Bot()
    try:
        bot.run()
    except KeyboardInterrupt:
        asyncio.run(bot.stop())

