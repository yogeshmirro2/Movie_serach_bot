#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from pyrogram import Client, __version__
from configs import Config
from . import LOGGER


class User(Client):
    def __init__(self):
        super().__init__(
            "userbot",
            api_hash=Config.API_HASH,
            api_id=Config.APP_ID,
            session_string=Config.USER_SESSION,
            workers=20
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        try: await self.export_session_string()
        except: pass
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
