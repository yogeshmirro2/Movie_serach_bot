import os
import re
import logging
import asyncio
from telegraph import Telegraph
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait
from configs import Config
from bot.database import Database # pylint: disable=import-error
from bot.bot import Bot # pylint: disable=import-error

FIND = {}
INVITE_LINK = {}
ACTIVE_CHATS = {}
db = Database()

@Bot.on_message(filters.text & filters.group, group=0)
async def auto_filter(bot, update):
    """
    A Funtion To Handle Incoming Text And Reply With Appropriate Results
    """
    group_id = update.chat.id

    if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return
    
    if ("https://" or "http://") in update.text:
        return
    
    query = re.sub(r"[1-2]\d{3}", "", update.text) # Targetting Only 1000 - 2999 😁
    
    if len(query) < 2:
        print("len(query) is less return line 34")
        return
    
    results = ""
    
    global ACTIVE_CHATS
    global FIND
    
    configs = await db.find_chat(group_id)
    achats = ACTIVE_CHATS[str(group_id)] if ACTIVE_CHATS.get(str(group_id)) else await db.find_active(group_id)
    ACTIVE_CHATS[str(group_id)] = achats
    
    if not configs:
        print("config not found so return line 47")
        return
    
    allow_video = configs["types"]["video"]
    allow_audio = configs["types"]["audio"] 
    allow_document = configs["types"]["document"]
    
    max_pages = configs["configs"]["max_pages"] # maximum page result of a query
    pm_file_chat = configs["configs"]["pm_fchat"] # should file to be send from bot pm to user
    max_results = configs["configs"]["max_results"] # maximum total result of a query
    max_per_page = configs["configs"]["max_per_page"] # maximum buttom per page 
    show_invite = configs["configs"]["show_invite_link"] # should or not show active chat invite link
    
    show_invite = (False if pm_file_chat == True else show_invite) # turn show_invite to False if pm_file_chat is True
    
    filters = await db.get_filters(group_id, query)
    
    if filters:
        i = 1
        for filter in filters: # iterating through each files
            file_name = filter.get("file_name")
            file_type = filter.get("file_type")
            file_link = filter.get("file_link")
            file_size = int(filter.get("file_size", "0"))
            
            # from B to MiB
            
            if file_size < 1024:
                file_size = f"[{file_size} B]"
            elif file_size < (1024**2):
                file_size = f"[{str(round(file_size/1024, 2))} KiB] "
            elif file_size < (1024**3):
                file_size = f"[{str(round(file_size/(1024**2), 2))} MiB] "
            elif file_size < (1024**4):
                file_size = f"[{str(round(file_size/(1024**3), 2))} GiB] "
            
            
            file_size = "" if file_size == ("[0 B]") else file_size
            
            # add emoji down below inside " " if you want..
            button_text = f"{file_size}:{file_name}"
            

            if file_type == "video":
                if allow_video: 
                    pass
                else:
                    continue
                
            elif file_type == "audio":
                if allow_audio:
                    pass
                else:
                    continue
                
            elif file_type == "document":
                if allow_document:
                    pass
                else:
                    continue
            
            unique_id = filter.get("unique_id")
#             if not FIND.get("bot_details"):
#                 try:
#                     bot_= await bot.get_me()
#                     FIND["bot_details"] = bot_
#                 except FloodWait as e:
#                     await asyncio.sleep(e.value)
#                     bot_= await bot.get_me()
#                     FIND["bot_details"] = bot_
                
#             bot_ = FIND.get("bot_details")
            file_link = f"https://t.me/{Config.BOT_USERNAME}?start={unique_id}"
            results = results + f"<p><b>{i}.</b>{button_text}👉<a href={file_link}>Download Link</a></p>"
            i += 1
            
    else:
        print("no file found line 124")
        return # return if no files found for that query
    

    if len(results) == 0:# double check
        print("results len is zero so return line 129")
        return
    
    else:
        try:
            short_name = "movies_search"
            telegraphs = Telegraph()
            new_user = telegraphs.create_account(short_name=short_name)
            auth_url = new_user["auth_url"]
            title = f"Result For {update.text}"
            content = results
            try:
                response = telegraphs.create_page(title=title, html_content=content)
            except Exception as e:
                print(e)
            await bot.send_message(chat_id=update.chat.id,
            text=f"<b>Found {i} Results For Your Query. To View Click Below Link:</b> https://telegra.ph/{response['path']}",
            reply_to_message_id=update.id)
            results = ""
        except Exception as e:
            print(e)


async def gen_invite_links(db, group_id, bot, update):
    """
    A Funtion To Generate Invite Links For All Active 
    Connected Chats In A Group
    """
    chats = db.get("chat_ids")
    global INVITE_LINK
    
    if INVITE_LINK.get(str(group_id)):
        return
    
    Links = []
    if chats:
        for x in chats:
            Name = x["chat_name"]
            
            if Name == None:
                continue
            
            chatId=int(x["chat_id"])
            
            Link = await bot.export_chat_invite_link(chatId)
            Links.append({"chat_id": chatId, "chat_name": Name, "invite_link": Link})

        INVITE_LINK[str(group_id)] = Links
    return 


async def recacher(group_id, ReCacheInvite=True, ReCacheActive=False, bot=Bot, update=Message):
    """
    A Funtion To rechase invite links and active chats of a specific chat
    """
    global INVITE_LINK, ACTIVE_CHATS

    if ReCacheInvite:
        if INVITE_LINK.get(str(group_id)):
            INVITE_LINK.pop(str(group_id))
        
        Links = []
        chats = await db.find_chat(group_id)
        chats = chats["chat_ids"]
        
        if chats:
            for x in chats:
                Name = x["chat_name"]
                chat_id = x["chat_id"]
                if (Name == None or chat_id == None):
                    continue
                
                chat_id = int(chat_id)
                
                Link = await bot.export_chat_invite_link(chat_id)
                Links.append({"chat_id": chat_id, "chat_name": Name, "invite_link": Link})

            INVITE_LINK[str(group_id)] = Links
    
    if ReCacheActive:
        
        if ACTIVE_CHATS.get(str(group_id)):
            ACTIVE_CHATS.pop(str(group_id))
        
        achats = await db.find_active(group_id)
        achatId = []
        if achats:
            for x in achats["chats"]:
                achatId.append(int(x["chat_id"]))
            
            ACTIVE_CHATS[str(group_id)] = achatId
    return 

