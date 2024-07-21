from pyrogram import __version__
from bot import Bot
import random, asyncio
from config import *
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

contact_button = InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/Titan_Cinemas_Support_bot")
keyboard = InlineKeyboardMarkup([[contact_button]])

from database.database import *


ABOUT_TXT = """╔════════════⦿
├⋗ ᴄʀᴇᴀᴛᴏʀ : <a href=https://t.me/Titan_Cinemas_Support_bot>ᴛɪᴛᴀɴ 💞</a>
├⋗ ʟᴀɴɢᴜᴀɢᴇ : <a href=https://python.org/>ᴘʏᴛʜᴏɴ3</a>
├⋗ ʟɪʙʀᴀʀʏ :  <a href=https://docs.pyrogram.org/>ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 2.0.106</a>
├⋗ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ : <a href=https://github.com/SirishChowdary/Titan_File_Store_Bot>ᴛɪᴛᴀɴ ᴄɪɴᴇᴍᴀs ᴘʀᴏᴠɪᴅᴇʀ</a>
├⋗ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/Titan_CInemas>ᴛɪᴛᴀɴ ᴄɪɴᴇᴍᴀs</a>
├⋗ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : <a href=https://t.me/Titan_Community_India>ᴛɪᴛᴀɴ ᴄᴏᴍᴍᴜɴɪᴛʏ</a>
╚═════════════════⦿ """

@Bot.on_callback_query()
async def cb_handler_func(client, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text=ABOUT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="start"),
                        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")
                    ]
                ]
            ),
        )
    elif data == "help":
        buttons = [
            [
                InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ", url="https://t.me/Titan_Community_India")
            ],
            [
                InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Titan_CInemas")
            ]   
        ]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=HELP_MSG.format(
                first_name=query.from_user.first_name,
                last_name=query.from_user.last_name or "Not Available",
                user_id=query.from_user.id, 
                username=None if not query.from_user.username else '@' + query.from_user.username or "Not Available",
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data == "start":
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴛɪᴛᴀɴ ᴄᴏᴍᴍᴜɴɪᴛʏ", url="https://t.me/Titan_Community_India")
                ],
                [
                    InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")
                ],
                [
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ", url="https://t.me/Titan_CInemas")
                ]
            ]
        )
        await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))   
        )
        await query.message.edit_text(
            text=START_MSG.format(first=query.from_user.first_name),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )    
        
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
