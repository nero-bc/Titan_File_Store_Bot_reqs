import asyncio
import base64
import logging
import os
import sys
import random
import re
import string
import time
from pyrogram import Client, filters,enums, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from helper_func import subscribed, encode, decode, get_messages
from database.database import *
from database.premium_db import db1
from database.fsub_db import Fsub_DB
from plugins.fsub import Force_Sub
fsub_db = Fsub_DB()

REQUEST_CHANNELS = [REQUEST_CHANNEL, REQUEST_CHANNEL2]

PREMIUM_PIC = os.environ.get('PREMIUM_PIC', 'https://te.legra.ph/file/abcf32b7c864caac94c9b.jpg')

PREMIUM_TEXT = """<b>👋 ʜᴇʏ {first},
    
🎖️ <u>ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs</u>

● <code>10₹</code> ➛ <u>ʙʀᴏɴᴢᴇ ᴘʟᴀɴ</u> » <code>7 ᴅᴀʏꜱ</code>
● <code>29₹</code> ➛ <u>ꜱɪʟᴠᴇʀ ᴘʟᴀɴ</u> » <code>30 ᴅᴀʏꜱ</code>
● <code>129₹</code> ➛ <u>ɢᴏʟᴅ ᴘʟᴀɴ</u> » <code>90 ᴅᴀʏꜱ</code>
● <code>370₹</code> ➛ <u>ᴘʟᴀᴛɪɴᴜᴍ ᴘʟᴀɴ</u> » <code>180 ᴅᴀʏꜱ</code>
● <code>500₹</code> ➛ <u>ᴅɪᴀᴍᴏɴᴅ ᴘʟᴀɴ</u> » <code>365 ᴅᴀʏꜱ</code>

💵 ᴜᴘɪ ɪᴅ - <code>titanindia@ibl</code>
⚡ ǫʀ ᴄᴏᴅᴇ - <a href='https://te.legra.ph/file/c2aa509df2e82077c7a0d.jpg'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>

‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.
<blockquote>⚡ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='http://t.me/Official_Snowball'>sɴᴏᴡ ʙᴀʟʟ 🧿</a></blockquote>"""

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    user_first_name = message.from_user.first_name

    is_req = await Force_Sub(client, message)
    if not is_req:
        return
    
    if id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Official_Snowball")
        return

    if not await present_user(id):
        try:
            await add_user(id)
            await client.send_message(chat_id=LOG_CHANNEL, text=f"🔥 {user_first_name} ɢᴏᴛ ʜɪs ғɪʟᴇ ᴀɴᴅ ʜɪs ᴜsᴇʀ ɪᴅ ɪs {id}")
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

        temp_msg = await message.reply("ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ғɪʟᴇs ɪɴғᴏ...💞")

        for progress in range(10, 101, 10):
            await temp_msg.edit_text(f"ᴄᴏʟʟᴇᴄᴛɪɴɢ ʏᴏᴜʀ ғɪʟᴇs ɪɴғᴏ ᴘʟs ᴡᴀɪᴛ ⚡... {progress}%")
            await asyncio.sleep(0.3)
            
        await temp_msg.edit_text("🚀 ᴅᴏɴᴇ sᴇɴᴅɪɴɢ ɴᴏᴡ @titan_Cinemas")
        await asyncio.sleep(1)
        await temp_msg.delete()

        user_first_name = message.from_user.first_name
        user_id = message.from_user.id

        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"⚡ {user_first_name} ɢᴏᴛ ʜɪs ғɪʟᴇ ᴀɴᴅ ʜɪs ᴜsᴇʀ ɪᴅ ɪs {user_id}"
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
                
                warning_msg = await message.reply("<b><u>❗️❗️❗️ɪᴍᴘᴏʀᴛᴀɴᴛ❗️️❗️❗️</u></b>\n\n ᴛʜɪs ғɪʟᴇ/ᴠɪᴅᴇᴏ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ <b><u>10 ᴍɪɴᴜᴛᴇs</u> 🫥 <i></b>(ᴅᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs)</i>.\n\n<b><i>ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜɪs ғɪʟᴇ/ᴠɪᴅᴇᴏ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ᴀɴᴅ sᴛᴀʀᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇʀᴇ</b>")
                await asyncio.sleep(600)
                await warning_msg.delete()
                await sent_message.delete()

            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_message = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                              reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                
                warning_msg = await message.reply("<b><u>❗️❗️❗️ɪᴍᴘᴏʀᴛᴀɴᴛ❗️️❗️❗️</u></b>\n\n ᴛʜɪs ғɪʟᴇ/ᴠɪᴅᴇᴏ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ <b><u>10 ᴍɪɴᴜᴛᴇs</u> 🫥 <i></b>(ᴅᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs)</i>.\n\n<b><i>ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜɪs ғɪʟᴇ/ᴠɪᴅᴇᴏ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ᴀɴᴅ sᴛᴀʀᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇʀᴇ</b>")
                await asyncio.sleep(600)
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
                    InlineKeyboardButton("🚀 ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ : ʀᴇᴍᴏᴠᴇ ᴀᴅꜱ 🚀", callback_data="premium")
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
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
        return
        
    buttons = [
        [
            InlineKeyboardButton("⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",url = client.invitelink),
        ]
    
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '💞 ᴛʀʏ ᴀɢᴀɪɴ 💞',
                    url = f"https://t.me/Titan_Link_Store_Bot?start={message.command[1]}"
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

@Bot.on_message(filters.command('plans') & filters.private)
async def plans_command(bot: Bot, message: Message):
    user = message.from_user
    user_id = message.from_user.id
    username = message.from_user.username
    first = user.first_name

    if user_id in await list_banned_users():
        await message.reply("ɪᴛ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜʀ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴍᴇ ᴄᴏɴᴛᴀᴄᴛ ɴᴏᴡ @Official_Snowball")
        return
    
    contact_owner_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Contact Owner 📩", url=f"https://t.me/Official_Snowball")
            ]
        ]
    )

    # Send the premium plans text as a caption along with the photo
    await bot.send_photo(
        chat_id=user_id,
        photo=PREMIUM_PIC,  # Add the URL of the image explaining premium plans
        caption=PREMIUM_TEXT.format(first=first),
        reply_markup=contact_owner_button
    )

@Bot.on_message(filters.command("ban_user") & filters.private)
async def ban_command(client: Client, message: Message):
    id = message.from_user.id
    
    if id in await list_banned_users():
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
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
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
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
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
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
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
        return
    
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
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
        return
        
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    id = message.from_user.id
    
    if message.from_user.id not in ADMINS:
        await message.reply_text("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return

    if id in await list_banned_users():
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
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

@Bot.on_message(filters.command("info") & filters.private)
async def showid(client: Client, message: Message):
    user = message.from_user
    id = message.from_user.id

    if id in await list_banned_users():
        await message.reply("It Looks Like Your Are Banned From Using Me Contact Now @Official_Snowball")
        return
        
    user_id = user.id
    username = user.username or "Not Available"
    first_name = user.first_name
    last_name = user.last_name or "Not Available"
    
    user_link = f"<a href='tg://user?id={user_id}'>Click Here</a>"
    
    caption = (
        f"👤 User ID: <code>{user_id}</code>\n"
        f"👤 Username: <code>{username}</code>\n"
        f"👤 First Name: <code>{first_name}</code>\n"
        f"👤 Last Name: <code>{last_name}</code>\n"
        f"🔗 User Link: {user_link}"
    )

    button = InlineKeyboardButton(
        "Click Here", url=f"tg://user?id={user_id}"
    )
    keyboard = InlineKeyboardMarkup([[button]])

    await message.reply_photo(
        photo=BOT_USERS, caption=caption, reply_markup=keyboard
    )

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
