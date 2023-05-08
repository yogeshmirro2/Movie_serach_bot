#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @SpEcHIDe

from pyrogram import Client, enums, __version__
from configs import Config,TG_BOT_WORKERS
from . import LOGGER

from .user import User


class Bot(Client):
  USER: User = None
  USER_ID: int = None

  def __init__(self):
    super().__init__("bot",
                     api_hash=Config.API_HASH,
                     api_id=Config.APP_ID,
                     plugins={"root": "bot/plugins"},
                     workers=TG_BOT_WORKERS,
                     bot_token=Config.BOT_TOKEN,
                     sleep_threshold=10)
    self.LOGGER = LOGGER

  async def start(self):
    await super().start()
    bot_details = await self.get_me()
    self.set_parse_mode(enums.ParseMode.HTML)
    self.LOGGER(__name__).info(f"@{bot_details.username}  started! ")
    self.USER, self.USER_ID = await User().start()

  async def stop(self, *args):
    await super().stop()
    self.LOGGER(__name__).info("Bot stopped. Bye.")
