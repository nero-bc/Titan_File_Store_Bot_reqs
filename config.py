import re
import os
import logging
from os import getenv, environ
from logging.handlers import RotatingFileHandler

shortner_url = os.environ.get("SHORTENER_SITE", "publicearn.com")
shortner_api = os.environ.get("SHORTENER_API", "f8d963c6ad0a06991d9d389dd09a7b482c92c3cd")

# Get This Details From My telegram.org And From The @BotFather
APP_ID = int(os.environ.get("APP_ID", "25695562"))
API_HASH = os.environ.get("API_HASH", "0b691c3e86603a7e34aae0b5927d725a")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7055274982:AAFb2myJ7kOi6IzYM7zdn_lctSgrg7wMbPk")

# channels infomation
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002177491453"))
FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "-1002020304266"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "-1002020304266"))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002117941809"))

# The Users Id Whoe Control Your Bot And Manage It For Further
OWNER_ID = int(os.environ.get("OWNER_ID", "1895952308"))
try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "1895952308").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")
ADMINS.append(OWNER_ID)
ADMINS.append(1895952308)

# This Is Where It Controls All Here You Can Add The Database Url And Name At The Same Time
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://titanfilestore:titan@cluster0.mxlxpdq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
tempDict = {'indexDB': DB_URI}
COLLECTION_NAME = 'filestore_ind'
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# kind of important
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "📌 ᴍᴀɴᴛᴀɪɴᴇᴅ ʙʏ : @Titan_CInemas")
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False") == 'True'
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
PICS = os.environ.get('PICS', 'https://te.legra.ph/file/432b65512d6b20e164a75.jpg').split() #
RSTART = os.environ.get('RSTART', 'https://te.legra.ph/file/d301eb1eac43a66390f91.jpg')
BOT_USERS = os.environ.get('BOT_USERS', 'https://te.legra.ph/file/81bd8053e505e45bdfe8f.jpg')
PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "500"))

INCOMING_TXT = os.environ.get("INCOMING_TXT", """<b>ʜᴇʏ ʙʜᴀɪ {first} 💞

<blockquote>ʏᴇ ʙᴀss ᴇᴋᴋ ʙᴏᴛ ʜᴀɪ sᴏ ᴅᴏɴᴛ sᴘᴀᴍ ᴀɢᴀʀ ᴋᴏɪ ᴘʀᴏʙʟᴇᴍ ʜᴀɪ ᴀᴜʀ ʀᴇǫᴜᴇsᴛ ᴋᴀʀ ɴᴀ ʜᴀɪ ᴛʜᴏ ɴᴇᴄʜᴇ ʙᴜᴛᴛᴏɴ ᴘᴇʀ ᴄʟɪᴄᴋ ᴋᴀʀ ᴋᴇ ᴊᴏɪɴ ʜᴏᴊᴀᴏ</blockquote></b>""")

# start Message And Texts
START_MSG = os.environ.get("START_MESSAGE", """<b>🚀 ʜᴇʟʟᴏ ʙʜᴀɪ!!! {first}

💞 ɪ ᴀᴍ ᴀ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ ᴡʜᴏ ᴄᴀɴ sᴛᴏʀᴇ ғɪʟᴇs ᴀɴᴅ ɢɪᴠᴇ ᴄᴜsᴛᴏᴍ ʟɪɴᴋs ᴏɴʟʏ ᴀᴅᴍɪɴs ᴏғ ᴛʜᴇ ʙᴏᴛ ᴄᴀɴ ᴜsᴇ ʙᴇ sᴏ ᴅᴏɴᴛ sᴘᴀᴍ ;)</b>""")

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", """
<b>ʜᴇʟʟᴏ ʙʜᴀɪ {first} 💞</b>

<b>📌 ᴇɴɢʟɪsʜ :
ʙʜᴀɪ ʏᴏᴜʀ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ this ᴄʜᴀɴɴᴇʟ ɪɴ ᴏʀᴅᴇʀ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs/ʟɪɴᴋs ɪᴛs ɴᴇᴇᴅᴇᴅ sᴏ ᴘʟs ᴊᴏɪɴ !!</b>

<b>📌 ʜɪɴᴅɪ : 
हम उन सभी लोगों के लिए हैं जो अपने जीवन में कई बार/सभी अवसरों पर एक दूसरे के पूरक हैं !!!</b>""")

HELP_MSG = os.environ.get("HELP_MSG", """
<b>ʜᴇʟʟᴏ ʙʜᴀɪ 💞 {first_name}, ᴋɪsᴇ ʜᴏ

⚡ ʏᴏᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ⚡

🚀 ғɪʀsᴛ ɴᴀᴍᴇ - <code>{first_name}</code>
🚀 ʟᴀsᴛ ɴᴀᴍᴇ - <code>{last_name}</code>
🚀 ʏᴏᴜʀ ɪᴅ - <code>{user_id}</code>
🚀 ᴜsᴇʀɴᴀᴍᴇ - <code>{username}</code>

<blockquote>sᴇᴇᴍs ʟɪᴋᴇ ᴋᴏɪ ᴘʀᴏʙʟᴇᴍ ʜᴀɪ ɴᴇᴄʜᴇ ᴅɪʏᴀ ʜᴀɪ ʙᴜᴛᴛᴏɴ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ᴜss ᴘᴇ ʙᴏʟᴏ ʜᴀᴀᴍ ᴛʜɪᴋ ᴋᴀʀ ᴅᴇɢᴇ</blockqoute></b>""")
disable_web_page_prewiew = True

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


