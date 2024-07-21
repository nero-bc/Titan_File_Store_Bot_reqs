import asyncio
import base64
import logging
import os
import sys
import random
import re
import string
import time
import datetime, time
from pyrogram import Client, filters,enums, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from database.join_req import *
from pyrogram.types import ChatJoinRequest
from helper_func import subscribed, encode, decode, get_messages
from database.database import *

SECONDS = int(os.getenv("SECONDS", "600"))

@Bot.on_chat_join_request(filters.chat(FORCE_SUB_CHANNEL2))
async def join_reqs(client: Client, message: ChatJoinRequest):
  if not await db.find_join_req(message.from_user.id):
    await db.add_join_req(message.from_user.id)

@Bot.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client: Client, message: Message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id

    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Titan_Cinemas_Support_bot")
        return
        
    if not await present_user(id):
        try:
            await add_user(id)
            await client.send_message(chat_id=LOG_CHANNEL, text=f"📌 ᴀ ɴᴇᴡ ᴜsᴇʀ {user_first_name} sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴜsᴇʀ ɪᴅ - {id}")
        except:
            pass
    text = message.text
    if len(text)>7:
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
                ids = range(start,end+1)
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
        temp_msg = await message.reply("ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ғɪʟᴇs/ʟɪɴᴋs... ⚡")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("​​​sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ....!")
            return
        await temp_msg.delete()

        Titan = []
        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None
            try:
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(1)
                Titan.append(snt_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                Titan.append(snt_msg)
            except:
                pass

        k = await message.reply_text("<b>❗️ <u>ɪᴍᴘᴏʀᴛᴀɴᴛ</u> ❗️</b>\n\n<b>ᴛʜɪs ᴠɪᴅᴇᴏ/ғɪʟᴇ/ʟɪɴᴋ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ 10 ᴍɪɴᴜᴛᴇs (ᴅᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs).\n\n📌 ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜɪs ᴠɪᴅᴇᴏ/ғɪʟᴇ/ʟɪɴᴋ ᴛᴏ sᴏᴍᴇᴡʜᴇʀᴇ ᴇʟsᴇ ᴀɴᴅ sᴛᴀʀᴛ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛʜᴇʀᴇ.</b>")
        await asyncio.sleep(SECONDS)

        for data in Titan:
            try:
                await data.delete()
                await k.edit_text("<b>ʏᴏᴜʀ ᴠɪᴅᴇᴏ/ғɪʟᴇ/ʟɪɴᴋ ɪs sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ !</b>")
            except:
                pass

        return
    else:
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
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Titan_Cinemas_Support_bot")
        return
        
    buttons = [
        [
            InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",url = client.invitelink),
            InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",url = client.invitelink2),
        ]
    
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'ᴛʀʏ ᴀɢᴀɪɴ',
                    url = f"https://t.me/Titan_Files_Ind_Bot?start={message.command[1]}"
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
    id = message.from_user.id
    
    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Titan_Cinemas_Support_bot")
        return
        
    if message.from_user.id not in ADMINS:
        await message.reply_text("You don't have the permission to use this command.")
        return

    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])
            await add_banned_user(user_id)
            await message.reply_text(f"User with ID {user_id} has been banned.")
        except ValueError:
            await message.reply_text("Invalid user ID.")
    else:
        await message.reply_text("Please specify a user ID to ban.")

@Bot.on_message(filters.command("unban_user") & filters.private)
async def unban_command(client: Client, message: Message):
    id = message.from_user.id
    
    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Titan_Cinemas_Support_bot")
        return
        
    if message.from_user.id not in ADMINS:
        await message.reply_text("You don't have the permission to use this command.")
        return

    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])
            await remove_banned_user(user_id)
            await message.reply_text(f"User with ID {user_id} has been unbanned.")
        except ValueError:
            await message.reply_text("Invalid user ID.")
    else:
        await message.reply_text("Please specify a user ID to unban.")
      
@Bot.on_message(filters.command("banlist") & filters.private)
async def banlist_command(client: Client, message: Message):
    id = message.from_user.id
    
    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Titan_Cinemas_Support_bot")
        return
        
    if message.from_user.id not in ADMINS:
        await message.reply_text("You don't have the permission to use this command.")
        return

    banned_users = await list_banned_users()
    if banned_users:
        users_list = "\n".join(str(user_id) for user_id in banned_users)
        await message.reply_text(f"Banned Users:\n{users_list}")
    else:
        await message.reply_text("No users are currently banned.")


@Bot.on_message(filters.command("help") & filters.private)
async def report_command(client: Client, message: Message):
    user = message.from_user
    id = message.from_user.id

    user_id = user.id
    username = user.username or "Not Available"
    first_name = user.first_name
    last_name = user.last_name or "Not Available"

    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Titan_Cinemas_Support_bot")
        return
    
    buttons = [
            [
                InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ", url="https://t.me/Titan_Community_India")
            ],
            [
                InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Titan_CInemas")
            ]   
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_photo(
        photo=random.choice(PICS),
        caption=HELP_MSG.format(first_name=first_name, last_name=last_name, user_id=user_id, username=username),
        reply_markup=reply_markup,
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    id = message.from_user.id
    
    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Titan_Cinemas_Support_bot")
        return
        
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    id = message.from_user.id
    if id in await list_banned_users():
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Titan_Cinemas_Support_bot")
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
