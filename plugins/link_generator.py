from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, shortner_url, shortner_api
from helper_func import encode, get_message_id
from cloudscraper import create_scraper
from urllib.parse import quote

async def short_url(url):
    c = create_scraper().request
    r = c('GET', f'https://{shortner_url}/api?api={shortner_api}&url={quote(url)}').json()
    return (r['shortenedUrl'])

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "ғᴏʀᴡᴀʀᴅ ᴛʜᴇ ғɪʀsᴛ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..\n\n ᴏʀ sᴇɴᴅ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ʟɪɴᴋ", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ ᴇʀʀᴏʀ\n\n ᴛʜɪs ғᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ɪs ɴᴏᴛ ғʀᴏᴍ ᴍʏ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴛʜɪs ʟɪɴᴋ ɪs ᴛᴀᴋᴇɴ ғʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "ғᴏʀᴡᴀʀᴅ ᴛʜᴇ ʟᴀsᴛ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..\n ᴏʀ sᴇɴᴅ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ʟɪɴᴋ", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ ᴇʀʀᴏʀ\n\n ᴛʜɪs ғᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ɪs ɴᴏᴛ ғʀᴏᴍ ᴍʏ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴛʜɪs ʟɪɴᴋ ɪs ᴛᴀᴋᴇɴ ғʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/Movies_WebSeries_RequestBot?start={base64_string}"
    slink = await short_url(link)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("⚡ sʜᴀʀᴇ ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ ⚡", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ - <code>{link}</code>\n\n⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ sʜᴏʀᴛ ʟɪɴᴋ :- <code>{slink}</code></b>", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "ғᴏʀᴡᴀʀᴅ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..\n ᴏʀ sᴇɴᴅ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ʟɪɴᴋ", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ ᴇʀʀᴏʀ\n\n ᴛʜɪs ғᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ɪs ɴᴏᴛ ғʀᴏᴍ my ᴅʙ ᴄʜᴀɴɴᴇʟ or ᴛʜɪs ʟɪɴᴋ ɪs ɴᴏᴛ ᴛᴀᴋᴇɴ ғʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/Movies_WebSeries_RequestBot?start={base64_string}"
    slink = await short_url(link)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("⚡ sʜᴀʀᴇ ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ ⚡", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ - <code>{link}</code>\n\n⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ sʜᴏʀᴛ ʟɪɴᴋ :- <code>{slink}</code></b>", quote=True, reply_markup=reply_markup)
