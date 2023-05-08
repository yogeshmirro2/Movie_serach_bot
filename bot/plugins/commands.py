#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery,Message
from bot import Translation, LOGGER # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
from configs import Config
from bot.plugins.verify_helper import get_validation_min
from bot.plugins.add_user_to_db import add_user_to_database
from bot.plugins import linkshort
db = Database()

@Client.on_message(filters.private)
async def _(bot, update):
    await add_user_to_database(bot, update)

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    try:
        verify_check = update.command[1].split("_")[0] if "_" in update.command[1] else False
    except Exception as e:
        print(e)
        verify_check = False
        pass
    
    if verify_check:
        try:
            verify_key = update.command[1].split("_")[1]
            user_key = await db.get_verify_key(update.from_user.id)
            if verify_check == "verify" and verify_key==user_key:
                await db.update_verify_key(update.from_user.id)
                await db.update_verify_date(update.from_user.id)
                await bot.send_message(update.from_user.id,"<b>Verifiaction Complete☑️☑️☑️</b>")
                return
            elif verify_check == "verify" and verify_key!=user_key:
                if Config.VERIFY_KEY:
                    user_key = await db.get_verify_key(update.from_user.id)
                    shorted_link = Config.VERIFY_LINK[Config.VERIFY_KEY.index(user_key)]
                    await bot.send_message(update.from_user.id,f"<b>This Verification Link Expired🚫\nPlz Verify by This New Link👉👉</b>\n{shorted_link}\n🥁<i>Once You Verify, Your Verification Valid Till Next {Config.VERIFY_DAYS} Days</i>🥁\nHow To Verify👉👉{Config.HOW_TO_VERIFY_LINK}")
                    return
                else:
                    user_key = await db.get_verify_key(update.from_user.id)
                    to_be_short = f"https://t.me/{Config.BOT_USERNAME}?start=verify_"+user_key
                    shorted_link = await linkshort.Short(f"{to_be_short}")
                    await bot.send_message(update.from_user.id,f"<b>This Verification Link Expired🚫\nPlz Verify by This New Link👉👉</b>\n{shorted_link}\n🥁<i>Once You Verify, Your Verification Valid Till Next {Config.VERIFY_DAYS} Days</i>🥁\nHow To Verify👉👉{Config.HOW_TO_VERIFY_LINK}")
                    return
            else:
                await bot.send_message(update.from_user.id,f"<b>This Verification Link is Invalid🚫🚫</b>")
                return
        except Exception as e:
            print(e)
            await bot.send_message(update.from_user.id,f"<b>Something Went Wrong\nPlz Share This Error to Bot Owner</b>\n`{e}`")
            return
    if file_uid and not verify_check:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        try:
            if Config.VERIFY_DAYS:
                user_date = await db.get_verify_date(update.from_user.id)
                user_verify_min = await get_validation_min(user_date)
                if user_verify_min < 0 :
                    if Config.VERIFY_KEY:
                        user_key = await db.get_verify_key(update.from_user.id)
                        shorted_link = Config.VERIFY_LINK[Config.VERIFY_KEY.index(user_key)]
                        await bot.send_message(update.from_user.id,f"<b>You are n'Not Verifed🚫\nPlz Verify by This Link👉👉</b>\n{shorted_link}\n🥁<i>Once you Verify, Your Verification Valid till Next {Config.VERIFY_DAYS} Days</i>🥁\nHow To Verify👉👉{Config.HOW_TO_VERIFY_LINK}")
                        return
                    else:
                        user_key = await db.get_verify_key(cmd.from_user.id)
                        to_be_short = f"https://t.me/{Config.BOT_USERNAME}?start=verifylink_"+user_key
                        shorted_link = await linkshort.Short(f"{to_be_short}")
                        await bot.send_message(cmd.from_user.id,f"<b>You are Not Verifed🚫\nPlz Verify by This Link👉👉</b>\n{shorted_link}\n🥁<i>Once You Yerify, Your Verification Valid Till Next {Config.VERIFY_DAYS} days</i>🥁\nHow To Verify👉👉{Config.HOW_TO_VERIFY_LINK}")
                        return
                await update.reply_cached_media(
                    file_id,
                    quote=True,
                    caption = caption,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await update.reply_cached_media(
                    file_id,
                    quote=True,
                    caption = caption,
                    parse_mode=enums.ParseMode.HTML
                )
        except Exception as e:
            await update.reply_text(f"<b>Error:</b>\n<code>{e}</code>", True, parse_mode=enums.ParseMode.HTML)
            LOGGER(__name__).error(e)
        return

    buttons = [[
        InlineKeyboardButton('Developers', url='https://t.me/'),
        InlineKeyboardButton('Source Code 🧾', url ='https://github.com/')
    ],[
        InlineKeyboardButton('Support 🛠', url='https://t.me/')
    ],[
        InlineKeyboardButton('Help ⚙', callback_data="help")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(
                update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('About 🚩', callback_data='about')
    ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )
