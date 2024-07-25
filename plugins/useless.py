from bot import Bot
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from config import *

contact_button = [
    [
        InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/Titan_Community_India")
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
