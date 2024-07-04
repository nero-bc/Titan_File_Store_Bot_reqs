from pyrogram import Client, enums, filters
from bot import Bot
from pyrogram.types import Message, ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, MessageTooLong, FloodWait
from config import *
import random
from database.premium_db import db1
from database.fsub_db import Fsub_DB
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

REQUEST_CHANNELS = [REQUEST_CHANNEL, REQUEST_CHANNEL2]
INVITE_LINKS = [None, None]
FSUB_TEMP = {}

fsub_db = Fsub_DB()

FSUB_TXT = """
<b> ʜᴇʏ {first} 💞

ᴛᴜᴍ ɴᴇ ʜᴀᴍᴀʀᴇ ᴄʜᴀɴɴᴇʟs ᴍᴀɪ ᴊᴏɪɴ ɴᴇʜɪ ᴋɪʏᴀ ᴊᴏɪɴ ᴋᴀʀᴏ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ʙᴜᴛᴛᴏɴ ᴘᴇʀ ᴄʟɪᴄᴋ ᴋᴀʀᴏ 

<blockquote>💞 ʙᴏᴛ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ <a href=https://t.me/Titan_Cinemas_Support_bot>⚡ᴛɪᴛᴀɴ ᴄɪɴᴇᴍᴀs</a></b></blockquote>"""   

@Bot.on_chat_join_request(filters.chat(REQUEST_CHANNELS))
async def fetch_reqs(client: Client, request: ChatJoinRequest):
    try:
        user = await fsub_db.get_user(request.chat.id, request.from_user.id)
        if not user:
            await fsub_db.add_user(
                channel=request.chat.id,
                user_id=request.from_user.id,
                first_name=request.from_user.first_name,
                user_name=request.from_user.username,
                date=request.date
            )
    except Exception as e:
        print("An error occurred:", e)  

@Bot.on_message(filters.command("total_reqs") & filters.private & filters.user(ADMINS))
async def total_requests(client: Client , message: Message):
    total_channel1 = await fsub_db.total_users(REQUEST_CHANNELS[0])
    total_channel2 = await fsub_db.total_users(REQUEST_CHANNELS[1])
    total = total_channel1 + total_channel2
    await message.reply_text(
        text=f"<b>The total number of requests is {total}</b>",
        parse_mode=enums.ParseMode.HTML
    )

@Bot.on_message(filters.command("delete_all_reqs") & filters.private & filters.user(ADMINS))
async def purge_reqs(client: Client , message: Message):
    await fsub_db.purge_all(REQUEST_CHANNELS[0])
    await fsub_db.purge_all(REQUEST_CHANNELS[1])
    await message.reply_text(
        text=f"<b>Successfully deleted all join requests from DB.</b>",
        parse_mode=enums.ParseMode.HTML
    )

@Bot.on_message(filters.command("get_req") & filters.private & filters.user(ADMINS))
async def fetch_request(client: Client , message: Message):
    try:
        id = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(
            text="<b>Please give me a user ID to search.</b>",
            parse_mode=enums.ParseMode.HTML
        )
    
    user1 = await fsub_db.get_user(REQUEST_CHANNELS[0], int(id))
    user2 = await fsub_db.get_user(REQUEST_CHANNELS[1], int(id))
    
    if user1 or user2:
        user_info = user1 or user2
        return await message.reply_text(
            text=f"<b>ID: {user_info['id']}\nFirst Name: {user_info['fname']}\nUserName: {user_info['uname']}\nDate: {user_info['date']}</b>",
            parse_mode=enums.ParseMode.HTML
        )
    else:
        return await message.reply_text(
            text="<b>No such user found!</b>",
            parse_mode=enums.ParseMode.HTML
        )

@Bot.on_message(filters.command("delete_req") & filters.private & filters.user(ADMINS))
async def delete_request(client: Client , message: Message):
    try:
        command, id = message.text.split(" ", 1)
        if not id.isdigit() and not id.startswith('@'):
            raise ValueError("Invalid user ID")
    except (IndexError, ValueError):
        return await message.reply_text(
            text="<b>Please use the command in the format:</b>\n<code>/delete_req {user_id}</code>",
            parse_mode=enums.ParseMode.HTML
        )
    
    try:
        if id.startswith('@'):
            user = await bot.get_users(id)
            user_id = user.id
        else:
            user_id = int(id)
    except ValueError:
        return await message.reply_text(
            text="<b>User ID must be a numeric value.</b>",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        return await message.reply_text(
            text="<b>No user found with the provided username.</b>",
            parse_mode=enums.ParseMode.HTML
        )
    
    user1 = await fsub_db.get_user(REQUEST_CHANNELS[0], user_id)
    user2 = await fsub_db.get_user(REQUEST_CHANNELS[1], user_id)
    
    if user1:
        await fsub_db.delete_user(REQUEST_CHANNELS[0], user_id)
    if user2:
        await fsub_db.delete_user(REQUEST_CHANNELS[1], user_id)
    
    if user1 or user2:
        return await message.reply_text(
            text=f"<b>Successfully deleted {user1['fname'] if user1 else user2['fname']} from the database.</b>",
            parse_mode=enums.ParseMode.HTML
        )
    else:
        return await message.reply_text(
            text="<b>No user found with the provided ID</b>"
        )

@Bot.on_message(filters.command("fetch_reqs") & filters.private & filters.user(ADMINS))
async def fetch_all_reqs(client: Client , message: Message):
    txt = await message.reply_text("Processing...")
    requests_channel1 = await fsub_db.get_all(REQUEST_CHANNELS[0])
    requests_channel2 = await fsub_db.get_all(REQUEST_CHANNELS[1])
    requests = requests_channel1 + requests_channel2

    msg = "These are the Join Requests saved on DB:\n\n"
    for request in requests:
        msg += f"ID: {request['id']}\nFirst Name: {request['fname']}\nUserName: {request['uname']}\nDate: {request['date']}\n\n"
    
    try:
        await txt.edit_text(text=msg)
    except MessageTooLong:
        with open("Requests.txt", "w+") as outputFile:
            outputFile.write(msg)
        await message.reply_document(document="Requests.txt", caption="List of all Join Requests saved on DB.")


async def Force_Sub(client: Client, message: Message):
    user = message.from_user
    user_id = message.from_user.id
    
    if await db1.has_premium_access(user_id) or user_id in ADMINS:
        return True

    global INVITE_LINKS
    if not all(REQUEST_CHANNELS):
        return True

    try:
        user_in_channel1 = await fsub_db.get_user(REQUEST_CHANNELS[0], int(message.from_user.id))
        user_in_channel2 = await fsub_db.get_user(REQUEST_CHANNELS[1], int(message.from_user.id))
        
        if user_in_channel1 and user_in_channel2:
            return True
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.reply_text(f"Error: {e}")
        return False
        
    need_to_join = False
    btn = []

    for n, channel in enumerate(REQUEST_CHANNELS):
        try:
            if INVITE_LINKS[n] is None:
                link = await client.create_chat_invite_link(chat_id=channel, creates_join_request=True)
                INVITE_LINKS[n] = link.invite_link
                logger.info(f"Invite Link for Channel {n+1} Generated!")
            need_to_join = True
        except Exception as e:
            logger.error(f"Unable to generate invite link for Channel {n+1}!\nError: {e}")
            return False

    if need_to_join:
        btn.append([
            InlineKeyboardButton(f"⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=INVITE_LINKS[0]),
            InlineKeyboardButton(f"⚡ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=INVITE_LINKS[1])
        ])
        btn.append([
            InlineKeyboardButton(f"✔ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ ✔", callback_data="checksub")
        ])
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=FSUB_TXT.format(first=message.from_user.first_name),
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.HTML
        )
        return False

    return True
