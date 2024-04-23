from pyrogram import __version__
from bot import Bot
import random
from config import OWNER_ID, START_MSG
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

PICS = [
    "https://telegra.ph/file/c3de5660d279f49966064.jpg",
    "https://telegra.ph/file/a9bca7d6c17cc964a03bc.jpg",
    "https://telegra.ph/file/62f8b5d073e5e73242c60.jpg",
    "https://telegra.ph/file/adeaee8c1c7fdb4b90d34.jpg",
    "https://telegra.ph/file/41e39fa3afd743ab993c2.jpg",
]

contact_button = InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴜs ❤️", url="https://t.me/Titan_Association")
keyboard = InlineKeyboardMarkup([[contact_button]])

@Bot.on_callback_query()
async def cb_handler_func(client, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text=(
                f"<b>──────[ 🚀 sʀᴍ ᴛᴇʟᴇ ᴍɪx 🚀 ]───────────\n"
                f"├🌟 ᴍʏ ɴᴀᴍᴇ : <a href=https://t.me/Srm_Tele_Mix_Bot>sʀᴍ ᴛᴇʟᴇ ᴍɪx</a>\n"
                f"├💻 ʟᴀɴɢᴜᴀɢᴇ: <a href=https://aka.ms/vs/17/release/vc_redist.x64.exe>ᴄ++ & ᴊᴀᴠᴀ</a>\n"
                f"├🌐 ʜᴏsᴛᴇᴅ ᴏɴ: <a href=www.hostinger.in>ʜᴏsᴛɪɴɢᴇʀ ᴠᴘs</a>\n"
                f"├👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: <a href=https://t.me/TITAN_OWNER_INDIA>ᴛɪᴛᴀɴ ɪɴᴅɪᴀ</a>\n"
                f"├🛠️ ʙᴏᴛ sᴜᴘᴘᴏʀᴛ: <a href=https://t.me/SRMk_Chat>sʀᴍ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ</a>\n"
                f"├📢 ʙᴏᴛ ᴜᴘᴅᴀᴛᴇs: <a href=https://t.me/SRMkMiX>ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴊᴏɪɴ</a>\n"
                f"╰──────[ 🇮🇳 ᴋɪɴɢ ᴏғ ᴋᴅʀᴀᴍᴀs 🇮🇳 ]───────────</b>"
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
        buttons = [
            [
                InlineKeyboardButton("🌐 ᴘʀᴏʙʟᴇᴍ ? ᴄᴏɴᴛᴀᴄᴛ  🌐", url="https://t.me/Titan_Association_bot")
            ],
            [
                InlineKeyboardButton("🚀 ᴀʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("📝 ᴄᴏᴘʏʀɪɢʜᴛs\ᴅᴄᴍᴀ", url="https://t.me/Titan_Association_bot")
            ],
            [
                InlineKeyboardButton("📝 ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅ", url="https://play.google.com/store/apps/details?id=com.dubox.drive"),
                InlineKeyboardButton("🌟 ʟɪɴᴋ ʙʟᴏᴄᴋᴇᴅ?", url="https://t.me/Titan_Association_bot")
            ],
            [
                InlineKeyboardButton("🔥 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ 🔥", url="https://t.me/Hindi_dubbed_korean_Drma/3042")
            ]   
        ]

        await query.message.edit_text(
            text="This is a new option! Click the buttons for more information.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await query.message.reply_photo(
            photo=random.choice(PICS),
            caption="🆘 ʜᴇʟᴘ ? ʏᴇᴀʜ ᴡᴇ ᴀʀᴇ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ  🆘\n"
                    "sᴏ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴍᴏsᴛ ᴀsᴋᴇᴅ ǫᴜᴇsᴛɪᴏɴs.\n\n"
                    "sᴛɪʟʟ sᴏʟᴠᴇ ɴᴇʜɪ ʜᴜᴀ ɴᴏ ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛᴀᴄᴛ ʙᴜᴛᴛᴏɴ ᴘᴇ ᴄʟɪᴄᴋ ᴋᴀʀᴏ ✅",
            reply_markup=reply_markup,
        )
    elif data == "start":
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔥 sʀᴍ ᴛᴇʟᴇ ᴍɪx 🔥", url="https://t.me/SRMkMiX")
                ],
                [
                    InlineKeyboardButton("🌐 ʜᴇʟᴘ", callback_data="help"),
                    InlineKeyboardButton("❤️‍🩹 ᴀʙᴏᴜᴛ", callback_data="about")
                ],
                [
                    InlineKeyboardButton("🎉 ɴᴇᴛғʟɪx ʜɪɴᴅɪ ᴅᴜʙʙᴇᴅ ᴅʀᴀᴍᴀ", url="https://t.me/Netflix_korean_drama_hindi"),
                    InlineKeyboardButton("🎈 ʜɪɴᴅɪ ᴅᴜʙʙᴇᴅ ᴋᴅʀᴀᴍᴀ", url="https://t.me/Hindi_dubbed_korean_Drma")
                ],
                [
                    InlineKeyboardButton("🇮🇳 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 🇮🇳", url="https://t.me/SRMk_Chat")
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
