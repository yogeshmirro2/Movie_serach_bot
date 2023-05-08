import os
from os import environ

PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))


class Config(object):
    APP_ID = os.environ.get("APP_ID","")
    API_HASH = os.environ.get("API_HASH","")
    BOT_TOKEN = os.environ.get("BOT_TOKEN","")
    DB_URI = os.environ.get("DB_URI","")
    USER_SESSION = os.environ.get("USER_SESSION","")
    ADDITIONAL_KEYWORD = os.environ.get("ADDITIONAL_KEYWORD","")
    DB_NAME = os.environ.get("DB_NAME", "Adv_Auto_Filter")
    VERIFY_DAYS = os.environ.get("VERIFY_DAYS",'')
    VERIFY_KEY = os.environ.get("VERIFY_KEY", "").split()#this is for use pre shorted link.plz don't use special character like @#$%* etc us only letter number and = ,To use this VERIFY_DAYS var value must be fill.multiple key separted by space,verify_key and verify_link must be at same index. example if 'unfhd" this key is related to https://www.shorted.link then and verify_key is at index 1 in string(separated by space) then verify_link must be at index 1 in verify_link string
    VERIFY_LINK = os.environ.get("VERIFY_LINK","").split()#this is use for pre shorted link.To use this VERIFY_DAYS var value must be fill. multiple verification link separted by space. these links can be shorted links which is all related to VERIFY_KEY . Which link you want to short ,must be in this formate -- https://t.me/{YOUR BOT USERNAME without @}?start=verifylink_{any text which u want to add(this variable  is verify_key)}
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")#without @
    SHORTNER_API_LINK = os.environ.get("SHORTNER_API_LINK", '')#if u not use pre shorted link than shortner_ this var mus be fill
    SHORTNER_API = os.environ.get("SHORTNER_API", '')
    HOW_TO_VERIFY_LINK = os.environ.get("HOW_TO_VERIFY_LINK","")
