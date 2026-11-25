import asyncio
import json
import os
import importlib
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

from utils import send_inverted_msg

API_ID = 30491795
API_HASH = "9f0f88a409eb3779cb91bb1c980f2ca4"
BOT_TOKEN = "9135183367:AAF3i9BT3bvOZtL-nmp5dDYhEgrC-YL3br0"

manager_bot = TelegramClient('manager_bot', API_ID, API_HASH)
manager_bot.parse_mode = 'html'

hosted_clients = {}
SESSION_FILE = 'saved_sessions.json'

def load_sessions():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f: return json.load(f)
    return {}

def save_session(user_id, session_string):
    sessions = load_sessions()
    sessions[str(user_id)] = session_string
    with open(SESSION_FILE, 'w') as f: json.dump(sessions, f)

# 🔥 PLUGIN LOADER ENGINE 🔥
async def start_sniper_userbot(user_client, user_id):
    user_client.parse_mode = 'html'
    me = await user_client.get_me()

    if not os.path.exists("plugins"): os.makedirs("plugins")

    loaded_plugins = 0
    for file in os.listdir("plugins"):
        if file.endswith(".py") and not file.startswith("__"):
            plugin_name = file[:-3]
            try:
                module = importlib.import_module(f"plugins.{plugin_name}")
                if hasattr(module, 'setup'):
                    module.setup(user_client, me.id)
                    loaded_plugins += 1
            except Exception as e: print(f"❌ Error loading {plugin_name}: {e}")

    print(f"✅ Userbot Started for {me.first_name} | 🧩 Plugins Loaded: {loaded_plugins}")

async def startup_saved_clients():
    sessions = load_sessions()
    print(f"🔄 Found {len(sessions)} saved sessions. Auto-starting them...")
    for uid_str, s_string in sessions.items():
        try:
            uid = int(uid_str)
            client = TelegramClient(StringSession(s_string), API_ID, API_HASH)
            await client.connect()
            if await client.is_user_authorized():
                hosted_clients[uid] = client
                asyncio.create_task(start_sniper_userbot(client, uid))
            else: print(f"❌ Session for {uid} expired.")
        except Exception as e: print(f"⚠️ Failed to auto-start session {uid_str}: {e}")

@manager_bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await send_inverted_msg(manager_bot, event.chat_id, "<blockquote>🚀 <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ sɴɪᴘᴇʀ ʙᴏᴛ!</b>\nsᴇɴᴅ /ʟᴏɢɪɴ ᴛᴏ sᴛᴀʀᴛ.</blockquote>")

@manager_bot.on(events.NewMessage(pattern='/users'))
async def users_handler(event):
    if not hosted_clients:
        await send_inverted_msg(manager_bot, event.chat_id, "<blockquote>🔴 <b>ɴᴏ ᴜsᴇʀs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ ʜᴏsᴛᴇᴅ.</b></blockquote>")
        return
    msg = "<blockquote>👥 <b>ᴀᴄᴛɪᴠᴇ ʜᴏsᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs:</b>\n\n"
    for count, (uid, client) in enumerate(hosted_clients.items(), 1):
        try:
            me = await client.get_me()
            name = me.first_name if me.first_name else "Unknown"
            msg += f"🔸 <b>{count}.</b> {name} (<code>{uid}</code>)\n"
        except Exception: msg += f"🔸 <b>{count}.</b> <i>Session Error</i> (<code>{uid}</code>)\n"
    await send_inverted_msg(manager_bot, event.chat_id, f"{msg}\n📊 <b>ᴛᴏᴛᴀʟ ᴀᴄᴛɪᴠᴇ:</b> {len(hosted_clients)}</blockquote>")

@manager_bot.on(events.NewMessage(pattern='/login'))
async def login_handler(event):
    chat = event.chat_id
    user_id = event.sender_id
    if user_id in hosted_clients:
        await send_inverted_msg(manager_bot, chat, "<blockquote>⚠️ <b>ʏᴏᴜʀ ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ʜᴏsᴛᴇᴅ!</b></blockquote>")
        return

    async with manager_bot.conversation(chat) as conv:
        try:
            await send_inverted_msg(manager_bot, chat, "<blockquote>📱 <b>sᴇɴᴅ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ɴᴜᴍʙᴇʀ:</b></blockquote>")
            phone_number = (await conv.wait_event(events.NewMessage())).raw_text.strip()
            user_client = TelegramClient(StringSession(), API_ID, API_HASH)
            await user_client.connect()

            await send_inverted_msg(manager_bot, chat, "<blockquote>⏳ <b>sᴇɴᴅɪɴɢ ᴏᴛᴘ...</b></blockquote>")
            await user_client.send_code_request(phone_number)

            await send_inverted_msg(manager_bot, chat, "<blockquote>✅ <b>ᴏᴛᴘ sᴇɴᴛ!</b> sᴇɴᴅ ᴡɪᴛʜ sᴘᴀᴄᴇs (e.g. 1 2 3 4 5)</blockquote>")
            otp_code = (await conv.wait_event(events.NewMessage())).raw_text.replace(" ", "").strip()

            try: await user_client.sign_in(phone_number, otp_code)
            except SessionPasswordNeededError:
                await send_inverted_msg(manager_bot, chat, "<blockquote>🔐 <b>sᴇɴᴅ ʏᴏᴜʀ 2sᴛᴇᴘ ᴘᴀssᴡᴏʀᴅ:</b></blockquote>")
                pwd = (await conv.wait_event(events.NewMessage())).raw_text.strip()
                await user_client.sign_in(password=pwd)

            # 🔥 FIX: SESSION STRING PRINT 🔥
            session_string = user_client.session.save()
            save_session(user_id, session_string)
            hosted_clients[user_id] = user_client
            asyncio.create_task(start_sniper_userbot(user_client, user_id))

            msg3 = f"<blockquote>🔑 <b>ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ:</b>\n\n<code>{session_string}</code>\n\n⚠️ <i>ᴋᴇᴇᴘ ᴛʜɪs sᴇᴄʀᴇᴛ! ᴅᴏ ɴᴏᴛ sʜᴀʀᴇ ɪᴛ.</i></blockquote>"
            await send_inverted_msg(manager_bot, chat, msg3)

            await send_inverted_msg(manager_bot, chat, "<blockquote>🎉 <b>ʟᴏɢɪɴ sᴜᴄᴄᴇssғᴜʟ & sᴀᴠᴇᴅ!</b> ᴜsᴇʀʙᴏᴛ ʜᴏsᴛᴇᴅ 24/7.</blockquote>")
        except Exception as e:
            await send_inverted_msg(manager_bot, chat, f"<blockquote>❌ <b>ᴇʀʀᴏʀ:</b> <code>{e}</code></blockquote>")

@manager_bot.on(events.NewMessage(pattern='/logout'))
async def logout_handler(event):
    if event.sender_id in hosted_clients:
        try: await hosted_clients[event.sender_id].log_out()
        except: pass
        del hosted_clients[event.sender_id]
        sessions = load_sessions()
        if str(event.sender_id) in sessions:
            del sessions[str(event.sender_id)]
            with open(SESSION_FILE, 'w') as f: json.dump(sessions, f)
        await send_inverted_msg(manager_bot, event.chat_id, "<blockquote>✅ <b>ʟᴏɢɢᴇᴅ ᴏᴜᴛ!</b></blockquote>")
    else: await send_inverted_msg(manager_bot, event.chat_id, "<blockquote>❌ <b>ɴᴏᴛ ʟᴏɢɢᴇᴅ ɪɴ!</b></blockquote>")

print("🤖 Premium Plugin Bot Started...")
manager_bot.start(bot_token=BOT_TOKEN)
manager_bot.loop.run_until_complete(startup_saved_clients())
manager_bot.run_until_disconnected()

