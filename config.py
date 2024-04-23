import os
import logging
from logging.handlers import RotatingFileHandler


# Get This Details From My telegram.org And From The @BotFather
APP_ID = int(os.environ.get("APP_ID", "29663344"))
API_HASH = os.environ.get("API_HASH", "1ce180a5008f81cb3e23fd4143fe0f6a")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7052151160:AAFgtuGxrFlQiPaEkdYA5CTAMVB7HItt6iU")

# All The Channel Variables That You Have To Fill Its Important For Furter Working Of Bot
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002129294563"))
CONFIRM_ID_CHNL = int(os.environ.get("CONFIRM_ID_CHNL", "-1002112771713"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL_ID", "-1002033440783"))
MAIN_LOG_CHNL = int(os.environ.get("MAIN_LOG_CHNL", "-1002045697706"))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002025477526"))

# The Users Id Whoe Control Your Bot And Manage It For Further
OWNER_ID = int(os.environ.get("OWNER_ID", "6529179563"))
ADMINS = int(os.environ.get("ADMINS", "6529179563"))

# This Is Where You Can Add The Restart Message And Image Url That Will Send To The Admins
RESTART_CHNL_ID = int(os.environ.get("RESTART_CHNL_ID", "-1002033440783"))
RESTART_IMAGE_PATH = os.environ.get("RESTART_IMAGE_PATH", "https://graph.org/file/9f5c7ca64ae1c76b53914.jpg")
RESTART_CAPTION = os.environ.get("RESTART_CAPTION", "Apologies for the interruption! I've just been given a quick recharge and I'm back online now. Let's continue where we left off!")

# This Is Where It Controls All Here You Can Add The Database Url And Name At The Same Time
PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://favorod148:srikar@cluster0.3c3aldt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# kind of important
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False") == 'True'
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "Bhai This Is A Bot And Yeah Ye Programmed Hai And Surely Reply nehi Dega Tum Ko So Agar Problem Hai Tho /help Likko Agar Tutorial Chayie Tho /tutorial liiko"
PICS = [
    "https://telegra.ph/file/564a1b5c88ca8d3e3c453.jpg",
    "https://telegra.ph/file/dea3f5330fcc97dee3042.jpg",
    "https://telegra.ph/file/c57a7df479750521d3a33.jpg",
    "https://telegra.ph/file/5b5bea15bedeaafedd18a.jpg",
    "https://telegra.ph/file/f5039bcf2c931816018fa.jpg",
]

# start Message And Texts
START_MSG = os.environ.get("START_MESSAGE", """
Hello... 💖 {first}\n ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ғɪʟᴇɢᴜᴀʀᴅ ʙᴏᴛ! 📂
🌟 ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴛᴏʀᴇ ғɪʟᴇs ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ʟɪɴᴋs.
🔐 ʏᴏᴜʀ ғɪʟᴇs ᴀʀᴇ sᴇᴄᴜʀᴇ – ᴜsᴇʀs ᴄᴀɴ ᴍᴀᴋᴇ ᴄʜᴀɴɢᴇs.
💬 ɴᴇᴇᴅ ᴀᴄᴄᴇss? ᴊᴜsᴛ ᴀsᴋ ᴀɴ ᴀᴅᴍɪɴ ғᴏʀ ᴛʜᴇ ʟɪɴᴋ.\n\n ʜᴀᴘᴘʏ sᴛᴏʀɪɴɢ! 🚀""")

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE","""
</b>🌟 ɢʀᴇᴇᴛɪɴɢs, {first}! 

 ✨ᴇɴɢʟɪsʜ👇👇
ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ ᴛᴏ ᴜsᴇ ᴍᴇ
ᴋɪɴᴅʟʏ ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ
ᴄʟɪᴄᴋ ᴏɴ ᴛʀʏ ᴀɢᴀɪɴ

✨ʜɪɴᴅɪ👇👇
मेरा उपयोग करने के लिए आपको मेरे Channel में Join
होगा, कृपया Channel मैं Join करे
ᴛʀʏ ᴀɢᴀɪɴ ᴘᴇ ᴄʟɪᴄᴋ ᴋᴀʀᴏ</b>""")

disable_web_page_prewiew = True

try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "1314613615").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
