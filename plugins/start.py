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
                    [InlineKeyboardButton("🔥 sʀᴍ ᴛᴇʟᴇ ᴍɪx 🔥", url="https://t.me/SRMkMiX")]
                ])
                reply_markup = inline_keyboard
                
            try:
                sent_message = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                              reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                
                warning_msg = await message.reply("ᴛʜᴇ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ sʜᴏʀᴛʟʏ. ғᴏʀᴡᴀʀᴅɪɴɢ ᴛʜɪs ᴍᴇssᴀɢᴇ ғᴏʀ ʏᴏᴜʀ ʀᴇғᴇʀᴇɴᴄᴇ.")
                await asyncio.sleep(global_timer_value)
                await warning_msg.delete()
                await sent_message.delete()

            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_message = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                              reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                
                warning_msg = await message.reply("ᴛʜᴇ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ sʜᴏʀᴛʟʏ. ғᴏʀᴡᴀʀᴅɪɴɢ ᴛʜɪs ᴍᴇssᴀɢᴇ ғᴏʀ ʏᴏᴜʀ ʀᴇғᴇʀᴇɴᴄᴇ.")
                await asyncio.sleep(global_timer_value)
                await warning_msg.delete()
                await sent_message.delete()

            except:
                pass
        return
    else:
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
    
    if id in BANNED_USERS:
        await message.reply_text("Sorry, you are banned.")
        return
        
    buttons = [
        [
            InlineKeyboardButton(
                "🇮🇳 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ [ sʀᴍ ᴛᴇʟᴇ ᴍɪx ] 🇮🇳",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'ᴛʀʏ ᴀɢᴀɪɴ',
                    url = f"https://t.me/Titan_Cinemas_bot?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command("ban_user") & filters.private)
async def ban_command(client: Client, message: Message):
    print("Received /ban command")
    if message.from_user.id not in SUDO_USERS:
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
    if message.from_user.id not in SUDO_USERS:
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

@Bot.on_message(filters.command("banlist") & filters.private)
async def all_banned_command(client: Client, message: Message):
    print("Received /allbanned command")
    if message.from_user.id not in SUDO_USERS:
        await message.reply_text("𝚈𝙾𝚄 𝙳𝙾𝙽𝚃 𝙷𝙰𝚅𝙴 𝚃𝙷𝙴 𝙿𝙴𝚁𝙼𝙸𝚂𝚂𝙸𝙾𝙽 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳.")
        return

    if BANNED_USERS:
        banned_users_list = "\n".join([str(user_id) for user_id in BANNED_USERS])
        await message.reply_text(f"📋 ʟɪsᴛ ᴏғ ᴀʟʟ ʙᴀɴɴᴇᴅ ᴜsᴇʀs:\n{banned_users_list}")
    else:
        await message.reply_text("👍 ɴᴏ ᴜsᴇʀs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ʙᴀɴɴᴇᴅ.")

@Bot.on_message(filters.command("help") & filters.private)
async def report_command(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("🌐 𝚃𝙸𝚃𝙰𝙽 𝙾𝚆𝙽𝙴𝚁𝚂 🌐", url="https://t.me/Titan_Association_bot")
        ],
        [
            InlineKeyboardButton("🚀 𝙰𝙱𝙾𝚄𝚃", callback_data="about"),
            InlineKeyboardButton("📝 𝙲𝙾𝙿𝙸𝚁𝙸𝙶𝙷𝚃𝚂", callback_data="button2")
        ],
        [
            InlineKeyboardButton("📝 𝚃𝙸𝚃𝙰𝙽 𝙿𝚁𝙴𝙼𝙸𝚄𝙼", callback_data="premium"),
            InlineKeyboardButton("🌟 𝙻𝙸𝙽𝙺 𝙱𝙻𝙾𝙲𝙺𝙴𝙳?", url="https://t.me/Titan_Association_bot")
        ],
        [
            InlineKeyboardButton("🔥 𝙷𝙾𝚆 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 🔥", callback_data="tutorial")
        ]   
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_photo(
        photo=random.choice(PICS),
        caption="🆘 𝗛𝗲𝗹𝗽 ? 𝗬𝗲𝗮𝗵 𝗪𝗲 𝗮𝗿𝗲 𝗵𝗲𝗿𝗲 𝘁𝗼 𝗵𝗲𝗹𝗽  🆘\n"
                "𝚂𝙾 𝙲𝙻𝙸𝙲𝙺 𝚃𝙷𝙴 𝙱𝚄𝚃𝚃𝙾𝙽𝚂 𝙱𝙴𝙻𝙾𝚆 MOST 𝙰𝚂𝙺𝙴𝙳 𝚀𝚄𝙴𝚂𝚃𝙸𝙾𝙽𝚂.\n\n"
                "𝚂𝚃𝙸𝙻𝙻 𝚂𝙾𝙻𝚅𝙴 𝙽𝙴𝙷𝙸 𝙷𝚄𝙰 𝙽𝙾 𝙿𝚁𝙾𝙱𝙻𝙴𝙼 𝙲𝙾𝙽𝚃𝙰𝙲𝚃 𝙱𝚄𝚃𝚃𝙾𝙽 𝙿𝙴 𝙲𝙻𝙸𝙲𝙺 𝙺𝙰𝚁𝙾 ✅",
        reply_markup=reply_markup,
    )
    
@Bot.on_message(filters.command('settimer') & filters.private)
async def set_timer_command(client: Bot, message: Message):
    try:
        if message.from_user.id in ADMINS:
            global global_timer_value
            timer_argument = message.text.split(" ", 1)[1]
            
            if 's' in timer_argument:
                timer_value = int(timer_argument[:-1])
            elif 'm' in timer_argument:
                timer_value = int(timer_argument[:-1]) * 60
            elif 'h' in timer_argument:
                timer_value = int(timer_argument[:-1]) * 3600
            else:
                timer_value = int(timer_argument)
            
            if 1 <= timer_value <= 3600:
                global_timer_value = timer_value
                await message.reply(f"⏰ Global auto-delete timer set to {timer_value} seconds. ⏰")
            else:
                await message.reply("⚠️ Please enter a timer value between 1 and 3600 seconds. ⚠️")
        else:
            await message.reply("🚫 Sorry, only admins can set the auto-delete timer. 🚫")
    except (IndexError, ValueError):
        await message.reply("❌ Invalid command usage. Please use /settimer <value>s, /settimer <value>m, or /settimer <value>h. ❌")

@Bot.on_message(filters.command('checktimer') & filters.private)
async def check_timer_command(client: Bot, message: Message):
    try:
        if message.from_user.id in ADMINS:
            global global_timer_value
            
            if global_timer_value is not None:
                await message.reply(f"⏰ Global auto-delete timer is currently set to {global_timer_value} minutes. ⏰")
            else:
                await message.reply("⚠️ Global auto-delete timer hasn't been set yet. ⚠️")
        else:
            await message.reply("🚫 Sorry, only admins can check the auto-delete timer. 🚫")
    except AttributeError:
        await message.reply("❌ Please use /checktimer as a reply to a user's message. ❌")

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):

    if message.from_user.id not in SUDO_USERS:
        await message.reply_text("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")
        return
        
    try:
        msg = await client.send_message(chat_id=message.chat.id, text="🔄 Fetching user information. Please wait... ⏳")
        
        for i in range(5, 0, -1):
            await asyncio.sleep(1)
            await msg.edit_text(f"🔄 ғᴇᴛᴄʜɪɴɢ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ... {i} ⏳")

        users = await full_userbase()
        
        await msg.edit(f"✅ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ғᴇᴛᴄʜᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!\n\n👥 ɴᴜᴍʙᴇʀ ᴏғ ᴜsᴇʀs: {len(users)} 🌐")
    except Exception as e:
        await msg.edit(f"❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ғᴇᴛᴄʜɪɴɢ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.\n\n ᴇʀʀᴏʀ: {str(e)}")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    
    if message.from_user.id not in SUDO_USERS:
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
