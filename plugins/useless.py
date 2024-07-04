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
        InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/+whP0B-ffw2hkZDU1")
    ]
]
keyboard = InlineKeyboardMarkup(contact_button)

@Bot.on_message(filters.private & filters.incoming)
async def useless(bot: Bot, message: Message):
    content = message.text
    user_id = message.from_user.id
    username = message.from_user.username
    user_first_name = message.from_user.first_name
    
    if user_id in ADMINS:
        return
    await bot.send_message(
        chat_id=user_id,
        text=INCOMING_TXT.format(first=message.from_user.first_name),
        reply_markup=keyboard
    )
    await bot.send_text(
        chat_id=LOG_CHANNEL,
        text="User ID: {user_id}\nUsername: {username}\nContent: {content}"
    )
