from bot.database.database import Database
from pyrogram.types import Message
from pyrogram import Client
db = Database()
async def add_user_to_database(bot,cmd):
    if not await db.is_user_exist(cmd.from_user.id):
        await db.add_user(cmd.from_user.id)
