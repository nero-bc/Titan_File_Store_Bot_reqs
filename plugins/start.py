import asyncio
import base64
import logging
import os
import sys
import random
import re
import string
import time
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, PICS, CONFIRM_ID_CHNL
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

global_timer_value = None

BANNED_USERS = set()

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id

    if id in BANNED_USERS:
        await message.reply_text("Sorry, you are banned.")
        return

    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return

        temp_msg = await message.reply("ᴘʀᴏᴄᴇssɪɴɢ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")

        for progress in range(10, 101, 10):
            await temp_msg.edit_text(f"ᴘʀᴏᴄᴇssɪɴɢ ɪɴғᴏʀᴍᴀᴛɪᴏɴ... {progress}%")
            await asyncio.sleep(0.3)

        await temp_msg.delete()

        user_first_name = message.from_user.first_name
        user_last_name = message.from_user.last_name
        user_username = message.from_user.username
        user_id = message.from_user.id

        await client.send_message(
            chat_id=CONFIRM_ID_CHNL,
            text=f"ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ✅\n\n ᴘʀᴏᴄᴇssᴇᴅ {len(ids)} ᴍᴇssᴀɢᴇs ғʀᴏᴍ ᴜsᴇʀ:"
                 f"\n ғɪʀsᴛ ɴᴀᴍᴇ: {user_first_name}"
                 f"\n ʟᴀsᴛ ɴᴀᴍᴇ: {user_last_name}"
                 f"\n ᴜsᴇʀɴᴀᴍᴇ: {user_username}"
                 f"\n ᴜsᴇʀ ɪᴅ: {user_id}."
        )

        messages = await get_messages(client, ids)

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                inline_keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⚡ ᴛɪᴛᴀɴ ᴄɪɴᴇᴍᴀs ⚡", url="https://t.me/Titan_CInemas")]
                ])
                reply_markup = inline_keyboard
                
            try:
                sent_message = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                              reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                
                warning_msg = await message.reply("ᴛʜᴇ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ sʜᴏʀᴛʟʏ. ғᴏʀᴡᴀʀᴅɪɴɢ ᴛʜɪs ᴍᴇssᴀɢᴇ ғᴏʀ ʏᴏᴜʀ ʀᴇғᴇʀᴇɴᴄᴇ.")
                await asyncio.sleep(180)
                await warning_msg.delete()
                await sent_message.delete()

            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_message = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                              reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                
                warning_msg = await message.reply("ᴛʜᴇ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ sʜᴏʀᴛʟʏ. ғᴏʀᴡᴀʀᴅɪɴɢ ᴛʜɪs ᴍᴇssᴀɢᴇ ғᴏʀ ʏᴏᴜʀ ʀᴇғᴇʀᴇɴᴄᴇ.")
                await asyncio.sleep(180)
                await warning_msg.delete()
                await sent_message.delete()

            except:
                pass
        return
    else:
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
        await message.reply_photo(
            photo=random.choice(PICS),
            caption = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            quote = True
        )
        return

#=====================================================================================##

WAIT_MSG = """"<b>ᴘʀᴏᴄᴇssɪɴɢ ...</b>"""

REPLY_ERROR = """<code>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀs ᴀ ʀᴇᴘʟᴀʏ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ᴏᴜᴛ ᴀɴʏ sᴘᴀᴄᴇs.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    id = message.from_user.id

    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Official_Snowball")
        return
        
    buttons = [
        [
            InlineKeyboardButton("⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 1",url = client.invitelink),
            InlineKeyboardButton("⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 2",url = client.invitelink2)
        ],
        [
            InlineKeyboardButton("⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 3",url = client.invitelink3),
            InlineKeyboardButton("⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 4",url = client.invitelink4)
        ],
        [
            InlineKeyboardButton("⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 5",url = client.invitelink5)
        ]
    
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '💞 ᴛʀʏ ᴀɢᴀɪɴ 💞',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply_photo(
        photo=random.choice(PICS),
        caption = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
        ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True
    )

@Bot.on_message(filters.command("ban_user") & filters.private)
async def ban_command(client: Client, message: Message):
    print("Received /ban command")
    if message.from_user.id not in ADMINS:
        await message.reply_text("ʏ𝙾𝚄 ᴅᴏɴᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return

    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])
            BANNED_USERS.add(user_id)
            await message.reply_text(f"ᴜsᴇʀ ᴡɪᴛʜ ɪᴅ {user_id} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.")
        except ValueError:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ.")
    else:
        await message.reply_text("ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ʙᴀɴ.")

@Bot.on_message(filters.command("unban_user") & filters.private)
async def unban_command(client: Client, message: Message):
    print("Received /unban command")
    if message.from_user.id not in ADMINS:
        await message.reply_text("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return

    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])
            if user_id in BANNED_USERS:
                BANNED_USERS.remove(user_id)
                await message.reply_text(f"ᴜsᴇʀ ᴡɪᴛʜ ɪᴅ {user_id} ʜᴀs ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ.")
            else:
                await message.reply_text(f"ᴜsᴇʀ ᴡɪᴛʜ ɪᴅ {user_id} ɪs ɴᴏᴛ ᴄᴜʀʀᴇɴᴛʟʏ ʙᴀɴɴᴇᴅ.")
        except ValueError:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ.")
    else:
        await message.reply_text("ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ᴜɴʙᴀɴ.")


@Bot.on_message(filters.command("help") & filters.private)
async def report_command(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("⚡ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ ⚡", url="https://t.me/Titan_Cinemas_Support_bot")
        ],
        [
            InlineKeyboardButton("🚀 ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("📝 ᴄᴏᴘɪʀɪɢʜᴛs", url="https://t.me/Titan_Cinemas_Support_bot")
        ],
        [
            InlineKeyboardButton("📝 ᴛɪᴛᴀɴ ᴘʀᴇᴍɪᴜᴍ", url="https://t.me/Titan_Cinemas_Support_bot"),
            InlineKeyboardButton("🌟 ʟɪɴᴋ ʙʟᴏᴄᴋᴇᴅ?", url="https://t.me/Titan_Cinemas_Support_bot")
        ],
        [
            InlineKeyboardButton("🔥 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ 🔥", url="https://t.me/howtoopentitan/4")
        ]   
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_photo(
        photo=random.choice(PICS),
        caption="🆘 ʜᴇʟᴘ ? ʏᴇᴀʜ ᴡᴇ ᴀʀᴇ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ  🆘\n"
                "sᴏ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴍᴏsᴛ ᴀsᴋᴇᴅ ǫᴜᴇsᴛɪᴏɴs.\n\n"
                "sᴛɪʟʟ sᴏʟᴠᴇ ɴᴇʜɪ ʜᴜᴀ ɴᴏ ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛᴀᴄᴛ ʙᴜᴛᴛᴏɴ ᴘᴇ ᴄʟɪᴄᴋ ᴋᴀʀᴏ ✅",
        reply_markup=reply_markup,
    )

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    
    if message.from_user.id not in ADMINS:
        await message.reply_text("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return

    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>💌 ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴇssᴀɢᴇ.. ᴛʜɪs ᴡɪʟʟ ᴛᴀᴋᴇ sᴏᴍᴇ ᴛɪᴍᴇ </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u> 🇮🇳 ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ 🇮🇳 </u>

⚡ ᴛᴏᴛᴀʟ ᴜsᴇʀs: <code>{total}</code>
⚡ sᴜᴄᴄᴇssғᴜʟ: <code>{successful}</code>
⚡ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: <code>{blocked}</code>
⚡ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: <code>{deleted}</code>
⚡ ᴜɴsᴜᴄᴄᴇssғᴜʟ: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

@Bot.on_message(filters.command('restart') & filters.private & filters.user(ADMINS))
async def restart_bot(client: Bot, message: Message):
    try:
        restart_message = await message.reply("🔄 ʀᴇsᴛᴀʀᴛɪɴɢ ᴛʜᴇ ʙᴏᴛ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ... ⏳")
        
        for i in range(10, 101, 10):
            await asyncio.sleep(0.5)
            await restart_message.edit(f"🔄 ʀᴇsᴛᴀʀᴛɪɴɢ ᴛʜᴇ ʙᴏᴛ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ... {i}% ⏳")

        await restart_message.edit("✅ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
        await asyncio.sleep(2)
        await restart_message.delete()

        os.execl(sys.executable, sys.executable, *sys.argv)

    except Exception as e:
        await restart_message.edit(f"❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʀᴇsᴛᴀʀᴛɪɴɢ ᴛʜᴇ ʙᴏᴛ.\n\nError: {str(e)}")
