from pyrogram import __version__
from bot import Bot
import random
from config import OWNER_ID, START_MSG, PICS, HELP_MSG
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

contact_button = InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/Titan_Cinemas_Support_bot")
keyboard = InlineKeyboardMarkup([[contact_button]])

PLAN_PIC = "https://te.legra.ph/file/c2aa509df2e82077c7a0d.jpg"

PREMIUM_TXT = """<b>⚡ ᴡʜᴀᴛ ɪs ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ ?
ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ ɪs ᴀ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇ ᴊʜᴏ ɪss ᴋᴏ sᴜʙsᴄʀɪʙᴇ ᴋᴀʀᴇɢᴀ ᴜss ᴋᴏ ᴘʀᴇᴍɪᴜᴍ ᴘʀᴇᴋs ᴍɪʟᴇɢᴀ ʟɪᴋᴇ

🚀 ᴅɪʀᴇᴄᴛ ғɪʟᴇs ᴡɪᴛʜ ғᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋs
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
⚡ ǫʀ ᴄᴏᴅᴇ - <a href='https://te.legra.ph/file/c2aa509df2e82077c7a0d.jpg'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>

‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.
<blockquote>⚡ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/Titan_Cinemas_Support_bot'>⚡ ᴛɪᴛᴀɴ ɪɴᴅɪᴀ</a></blockquote>"""

@Bot.on_callback_query()
async def cb_handler_func(client, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text=(
                f"<b>──────[ 🚀 ᴛɪᴛᴀɴ ᴄɪɴᴇᴍᴀs 🚀 ]───────────\n"
                f"├🌟 ᴍʏ ɴᴀᴍᴇ : <a href=https://t.me/Titan_Link_Store_Bot>ᴛɪᴛᴀɴ ʟɪɴᴋ ᴘʀᴏᴠɪᴅᴇʀ</a>\n"
                f"├💻 ʟᴀɴɢᴜᴀɢᴇ: <a href=https://python.org/>ᴘʏᴛʜᴏɴ & ᴘʏʀᴏɢʀᴀᴍ</a>\n"
                f"├🌐 ʜᴏsᴛᴇᴅ ᴏɴ: <a href=www.hostinger.in>ʜᴏsᴛɪɴɢᴇʀ ᴠᴘs</a>\n"
                f"├👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: <a href=https://t.me/Titan_Cinemas_Support_bot>ᴛɪᴛᴀɴ ᴏᴡɴᴇʀ</a>\n"
                f"├🛠️ ʙᴏᴛ sᴜᴘᴘᴏʀᴛ: <a href=https://t.me/Titan_Cinemas_Support_bot>ᴛɪᴛᴀɴ sᴜᴘᴘᴏʀᴛ</a>\n"
                f"├📢 ʙᴏᴛ ᴜᴘᴅᴀᴛᴇs: <a href=https://t.me/Titan_Bots_India>ʙᴏᴛ ᴜᴘᴅᴀᴛᴇs</a>\n"
                f"╰──────[ 🇮🇳 ᴛɪᴛᴀɴ ᴄᴏᴍᴍᴜɴɪᴛʏ 🇮🇳 ]───────────</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📝 ʙᴀᴄᴋ", callback_data="start")],
                    [InlineKeyboardButton("🎉 ᴄʟᴏsᴇ", callback_data="close")]
                ]
            ),
        )
    elif data == "help":
        
        user = message.from_user
        id = message.from_user.id
        
        user_id = user.id
        username = user.username or "Not Available"
        first_name = user.first_name
        last_name = user.last_name or "Not Available"
        
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

        await query.message.edit_text(
            text=HELP_MSG,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await query.message.reply_photo(
            photo=random.choice(PICS),
            caption=HELP_MSG.format(first_name=first_name, last_name=last_name, user_id=user_id, username=username),
            reply_markup=reply_markup,
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

        await query.message.edit_text(
            text=PREMIUM_TXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await query.message.reply_photo(
            photo=random.choice(PICS),
            caption=PREMIUM_TXT,
            reply_markup=reply_markup,
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

        await query.message.edit_text(
            text=PREPREMIUM,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await query.message.reply_photo(
            photo=PLAN_PIC,
            caption=PREPREMIUM,
            reply_markup=reply_markup,
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
                    InlineKeyboardButton("🚀 ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ : ʀᴇᴍᴏᴠᴇ ᴀᴅꜱ 🚀", url="https://t.me/Titan_Cinemas_Support_bot")
                ]
            ]
        )
        await query.message.edit_text(
            text=START_MSG.format(
                first=query.from_user.first_name,
                last=query.from_user.last_name,
                username=None if not query.from_user.username else '@' + query.from_user.username,
                mention=query.from_user.mention,
                id=query.from_user.id
            ),
            reply_markup=reply_markup
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
