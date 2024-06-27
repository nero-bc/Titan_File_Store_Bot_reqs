from bot import Bot
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from config import *
from datetime import datetime
from helper_func import get_readable_time

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

contact_button = [
    [
        InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/Titan_Cinemas_Support_bot")
    ],
    [
        InlineKeyboardButton("🚀 ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ", callback_data="about"),
        InlineKeyboardButton("📝 ᴄᴏᴘɪʀɪɢʜᴛs", url="https://t.me/Titan_Cinemas_Support_bot")
    ]
]

keyboard = InlineKeyboardMarkup(contact_button)

@Bot.on_message(filters.private & filters.incoming)
async def useless(bot: Bot, message: Message):
    content = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    if user_id in ADMINS:
        return

    text_message = """
ʜᴇʏ ᴘʀᴏʙʟᴇᴍ ʜᴀɪ ᴋʏᴀ ? 💔
    
<blockquote>✪ ᴊᴜsᴛ sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ
✪ ᴀʟsᴏ sᴇɴᴅ ᴛʜᴇ sᴄʀᴇᴇɴ sʜᴏᴛ ?
✪ ᴀɴᴅ ᴛʜᴀᴛ's ɪᴛ ᴘʟs ᴡᴀɪᴛ ᴡᴇ ᴡɪʟʟ ʜᴇʟᴘ 🥰</blockquote>
        
🚀 ᴄᴏɴᴛᴀᴄᴛ ᴜs ʜᴇʀᴇ - <a href='https://t.me/Titan_Cinemas_Support_bot'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>
ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ᴄᴏɴᴛᴀᴄᴛ ᴜs"""

    await bot.send_message(
        chat_id=user_id,
        text=text_message,
        reply_markup=keyboard
    )

    await bot.send_photo(
        chat_id=MAIN_LOG_CHNL,
        photo="https://telegra.ph/file/d2b162dca637ca9ff54fb.jpg",
        caption=f"User ID: {user_id}\nUsername: {username}\nContent: {content}"
    )
