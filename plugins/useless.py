from bot import Bot
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT, MAIN_LOG_CHNL
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
        InlineKeyboardButton("Button 1", url="https://example.com/button1")
    ],
    [
        InlineKeyboardButton("Button 2", url="https://example.com/button2"),
        InlineKeyboardButton("Button 3", url="https://example.com/button3")
    ]
]

keyboard = InlineKeyboardMarkup([[contact_button]])

@Bot.on_message(filters.private & filters.incoming)
async def useless(bot: Bot, message: Message):
    content = message.text
    user_id = message.from_user.id
    username = message.from_user.username
    
    if user_id in ADMINS:
        return

    text_message = """ ʜᴇʏ ᴘʀᴏʙʟᴇᴍ ʜᴀɪ ᴋʏᴀ ? 💔
    
    ✪ ʜᴀᴀᴍ ʜᴀɪ ɴᴀ ᴊᴜsᴛ ʜᴀᴀᴍ ᴋᴏ ᴍᴇssᴀɢᴇ ᴋᴀʀᴏ
    ✪ sᴄʀᴇᴇɴ sʜᴏᴛ sᴇɴᴅ ᴋᴀʀᴏ ᴋʏᴀ ᴘʀᴏʙʟᴇᴍs ʜᴀɪ ?
    ✪ ᴛʜᴇɴ ᴊᴜsᴛ ᴡᴀɪᴛ ᴡᴇ ᴡᴇ ᴄᴏɴᴛᴀᴄᴛ ʏᴏᴜ 🥰
        
    🚀 ᴄᴏɴᴛᴀᴄᴛ ᴜs ʜᴇʀᴇ - @Titan_Association_bot
    ᴏʀ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ᴄᴏɴᴛᴀᴄᴛ ᴜs ❤️"""

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
