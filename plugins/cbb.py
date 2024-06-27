from pyrogram import __version__
from bot import Bot
import random
from config import *
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

contact_button = InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/Titan_Cinemas_Support_bot")
keyboard = InlineKeyboardMarkup([[contact_button]])

PLAN_PIC = "https://telegra.ph/file/96be180072e7e004bf3f1.jpg"

PREMIUM_TXT = """<b>⚡ ᴡʜᴀᴛ ɪs ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ ?
ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ ɪs ᴀ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇ ᴊʜᴏ ɪss ᴋᴏ sᴜʙsᴄʀɪʙᴇ ᴋᴀʀᴇɢᴀ ᴜss ᴋᴏ ᴘʀᴇᴍɪᴜᴍ ᴘʀᴇᴋs ᴍɪʟᴇɢᴀ ʟɪᴋᴇ

🚀 ᴅɪʀᴇᴄᴛ ғɪʟᴇs ᴡɪᴛʜ ғᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ
🚀 ᴘʀᴇᴍɪᴜᴍ ʀᴇǫᴜᴇsᴛ ɢʀᴏᴜᴘ
🚀 ᴘʀᴇᴍɪᴜᴍ ᴀʟʟ ᴀʀᴏᴜɴᴅ ᴏᴜʀ ʙᴏᴛs 💞
🚀 ᴀᴅᴠᴀɴᴄᴇ 24x7 sᴜᴘᴘᴏʀᴛ 
🚀 ᴘʀɪᴏʀɪᴛʏ ᴛᴏ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛs
🚀 ᴘʀᴇᴍɪᴜᴍ ᴄʜᴀɴɴᴇʟs ᴡɪᴛʜ ᴅɪʀᴇᴄᴛ ғɪʟᴇs ᴇᴠᴇʀʏ ᴅᴀʏ 100+ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴜᴘʟᴏᴀᴅᴇᴅ
    
<blockquote>📌 ɴᴏᴛᴇ : ᴡᴇ ᴋɴᴏᴡ ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇ ᴡɪʟʟ ʜᴀᴠᴇ ʟɪᴍɪᴛs ғᴏʀ sᴜʀᴇ ᴄᴀᴜsᴇ ᴡᴇ ᴀʀᴇ sᴛɪʟʟ ɪɴ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ sᴛᴀɢᴇ sᴏ ɪғ ʏᴏᴜ ɢᴇᴛ ᴜs ᴛɪᴍᴇ ᴀɴᴅ sᴜᴘᴘᴏʀᴛ ᴜs ᴡᴇ ᴡɪʟʟ sᴜʀᴇʟʏ ᴄᴏᴍᴇ ᴜᴘ ᴛᴏ ʏᴏᴜʀ ᴛʜᴏᴜɢʜᴛs ᴀɴᴅ ᴇxᴘᴇᴄᴛᴀᴛɪᴏɴs ᴛʜᴀɴᴋs~ᴛɪᴛᴀɴ</blockquote></b>"""

PREPREMIUM = """
ᴏᴏᴏᴏ ᴛʜᴀɴᴋs ғᴏʀ ᴍᴀᴋɪɴɢ ʏᴏᴜʀ ᴄʜᴏɪᴄᴇ ᴛᴏ ʙᴇ ᴡɪᴛʜ ᴜs ᴀɴᴅ ᴛʜᴀɴᴋs ғᴏʀ sᴜᴘᴘᴏʀᴛɪɴɢ

🎖️ <u>ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs</u>

● <code>10₹</code> ➛ <u>ʙʀᴏɴᴢᴇ ᴘʟᴀɴ</u> » <code>7 ᴅᴀʏꜱ</code>
● <code>29₹</code> ➛ <u>ꜱɪʟᴠᴇʀ ᴘʟᴀɴ</u> » <code>30 ᴅᴀʏꜱ</code>
● <code>129₹</code> ➛ <u>ɢᴏʟᴅ ᴘʟᴀɴ</u> » <code>90 ᴅᴀʏꜱ</code>
● <code>370₹</code> ➛ <u>ᴘʟᴀᴛɪɴᴜᴍ ᴘʟᴀɴ</u> » <code>180 ᴅᴀʏꜱ</code>
● <code>500₹</code> ➛ <u>ᴅɪᴀᴍᴏɴᴅ ᴘʟᴀɴ</u> » <code>365 ᴅᴀʏꜱ</code>

💵 ᴜᴘɪ ɪᴅ - <code>titanindia@ibl</code>
⚡ ǫʀ ᴄᴏᴅᴇ - <a href='https://telegra.ph/file/96be180072e7e004bf3f1.jpg'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>

‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.
<blockquote>⚡ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/Titan_Cinemas_Support_bot'>⚡ ᴛɪᴛᴀɴ ɪɴᴅɪᴀ</a></blockquote>"""

from database.database import *
from database.premium_db import db1
from database.fsub_db import Fsub_DB
fsub_db = Fsub_DB()

REQUEST_CHANNELS = [REQUEST_CHANNEL, REQUEST_CHANNEL2]

@Bot.on_callback_query()
async def cb_handler_func(client, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text=(
                f"<b>─[ 🚀 ᴛɪᴛᴀɴ ᴄɪɴᴇᴍᴀs 🚀 ]──\n"
                f"├🌟 ᴍʏ ɴᴀᴍᴇ : <a href=https://t.me/Titan_Link_Store_Bot>ᴛɪᴛᴀɴ ʟɪɴᴋ ᴘʀᴏᴠɪᴅᴇʀ</a>\n"
                f"├💻 ʟᴀɴɢᴜᴀɢᴇ: <a href=https://python.org/>ᴘʏᴛʜᴏɴ & ᴘʏʀᴏɢʀᴀᴍ</a>\n"
                f"├🌐 ʜᴏsᴛᴇᴅ ᴏɴ: <a href=www.hostinger.in>ʜᴏsᴛɪɴɢᴇʀ ᴠᴘs</a>\n"
                f"├👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: <a href=https://t.me/Titan_Cinemas_Support_bot>ᴛɪᴛᴀɴ ᴏᴡɴᴇʀ</a>\n"
                f"├🛠️ ʙᴏᴛ sᴜᴘᴘᴏʀᴛ: <a href=https://t.me/Titan_Cinemas_Support_bot>ᴛɪᴛᴀɴ sᴜᴘᴘᴏʀᴛ</a>\n"
                f"├📢 ʙᴏᴛ ᴜᴘᴅᴀᴛᴇs: <a href=https://t.me/Titan_Bots_India>ʙᴏᴛ ᴜᴘᴅᴀᴛᴇs</a>\n"
                f"╰─[ 🇮🇳 ᴛɪᴛᴀɴ ᴄᴏᴍᴍᴜɴɪᴛʏ 🇮🇳 ]──</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💞 ʙᴀᴄᴋ", callback_data="start"),
                        InlineKeyboardButton("🌜 ᴄʟᴏsᴇ", callback_data="close")
                    ]
                ]
            ),
        )
    elif data == "help":
        buttons = [
            [
                InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/Titan_Cinemas_Support_bot")
            ],
            [
                InlineKeyboardButton("📌 ᴀʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("📌 ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ", callback_data="premium")
            ],
            [
                InlineKeyboardButton("🔥 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ 🔥", url="https://t.me/howtoopentitan")
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
    elif data == "premium":
        buttons = [
            [
                InlineKeyboardButton("⚡ ᴡᴀɴɴᴀ ʙᴇ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ? ⚡", callback_data="preplan")
            ],
            [
                InlineKeyboardButton("🎉 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ 🎉", callback_data="start")
            ]
        ]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=PREMIUM_TXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data == "preplan":
        buttons = [
            [
                InlineKeyboardButton("🔥 sᴇɴᴅ sᴄʀᴇᴇɴ sʜᴏᴛ ɴᴏᴡ 🔥", url="https://t.me/Titan_Cinemas_Support_bot")
            ],
            [
                InlineKeyboardButton("🎉 ʙᴀᴄᴋ 🎉", callback_data="premium")
            ]
        ]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=PREPREMIUM,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data == "start":
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚡ ᴛɪᴛᴀɴ ᴄɪɴᴇᴍᴀs ⚡", url="https://t.me/Titan_CInemas")
                ],
                [
                    InlineKeyboardButton("🧿 ʜᴇʟᴘ", callback_data="help"),
                    InlineKeyboardButton("🔥 ᴀʙᴏᴜᴛ", callback_data="about")
                ],
                [
                    InlineKeyboardButton("🚀 ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ : ʀᴇᴍᴏᴠᴇ ᴀᴅꜱ 🚀", callback_data="premium")
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

    elif data == "checksub":
            user_id = query.from_user.id

            if await db1.has_premium_access(user_id) or user_id in ADMINS:
                await query.message.reply_text("You have premium access.")
                return True

            if not all(REQUEST_CHANNELS):
                await query.message.reply_text("Please provide the channels to check your subscription.")
                return True

            try:
                user_in_channel1 = await fsub_db.get_user(REQUEST_CHANNELS[0], user_id)
                user_in_channel2 = await fsub_db.get_user(REQUEST_CHANNELS[1], user_id)

                if user_in_channel1 and user_in_channel2:
                    await query.message.reply_text("⚡ ʏᴏᴜ ᴀʀᴇ ɴᴏᴡ ᴊᴏɪɴᴇᴅ ᴄʜᴀɴɴᴇʟs ᴘᴏsᴛ ᴘᴇ ᴊᴀᴏ ᴘʜɪʀ sᴇ ᴄʟɪᴄᴋ ᴋᴀʀᴏ ᴇɴᴊᴏʏ!!!")
                    return True

                elif user_in_channel1 or user_in_channel2:
                    await query.message.reply_text("💫 ʟᴏᴏᴋɪɴɢ ɢᴏᴏᴅ sᴏ ғᴀʀ ʏᴏᴜ ᴊᴏɪɴᴇᴅ 1 ᴄʜᴀɴɴᴇʟ")
                    return True

                else:
                    await query.message.reply_text("💞 ᴅᴏɴ'ᴛ ᴛʀʏ ᴛᴏ ʙᴇ ᴏᴠᴇʀ sᴍᴀʀᴛ ʙᴜᴅᴅʏ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟs ᴀʙᴏᴠᴇ")
                    return False

            except Exception as e:
                logger.error(f"Error: {e}")
                await query.message.reply_text(f"Error: {e}")
                await query.message.reply_text("There was an error checking your subscription. Please try again later.")
                return False

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
