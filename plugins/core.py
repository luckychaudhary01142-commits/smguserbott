import random
import asyncio
from telethon import events
from utils import get_user_settings, send_inverted_msg, get_target_reply_id

def setup(client, uid):
    # 🔥 STRICTLY LISTEN IN SAVED MESSAGES ONLY 🔥
    @client.on(events.NewMessage())
    async def core_handler(event):
        
        # 🛑 SABSE BADA LOCK: Agar chat tera Saved Message nahi hai, toh ignore 🛑
        if event.chat_id != uid: 
            return

        text = event.raw_text.strip()
        if not text: return
        cmd = text.lower().split()[0]

        session = get_user_settings(uid)

        # 📜 YE SARE COMMANDS HAIN
        all_cmds = [
            '.help', '!help', 'help', 
            '.at', '!at', 'at', 
            '.st1', '!st1', '.st2', '!st2', 
            '.stop', '!stop', 'stop', 
            '.setstopmsg', '!setstopmsg',
            '.fontraid', '!fontraid', 'fontraid',
            '.oneword', '!oneword', 'oneword',
            '.faketype', '!faketype', 'faketype',
            '.delay', '!delay', 'delay',
            '.stopfontraid', '!stopfontraid', 'stopfontraid',
            '.stoponeword', '!stoponeword', 'stoponeword',
            '.stopfaketype', '!stopfaketype', 'stopfaketype'
        ]

        # 🔥 LIVE GHOST RELAY (SMART AUTO-TRACKING TARGET) 🔥
        if cmd not in all_cmds:
            if session.get('is_active') and session.get('target_chat'):
                final_text = text
                if session.get('prefix_text'): final_text = f"{session['prefix_text']} {final_text}"
                if session.get('suffix_text'): final_text = f"{final_text} {session['suffix_text']}"
                
                try:
                    # 🔥 JAISE ONEWORD ME HAI, WAISE HI HAR BAAR LATEST MESSAGE DHOONDHEGA 🔥
                    reply_id = await get_target_reply_id(event.client, session['target_chat'], session['target_user'], session['target_msg_id'])
                    
                    if reply_id:
                        await client.send_message(session['target_chat'], final_text, reply_to=reply_id)
                    else:
                        await client.send_message(session['target_chat'], final_text)
                except Exception:
                    pass
            return

        # ⚙️ HELP COMMAND
        if cmd in ['.help', '!help', 'help']:
            help_msg = """<blockquote>🛠️ <b>s ɴ ɪ ᴘ ᴇ ʀ  ᴍ ᴀ s ᴛ ᴇ ʀ</b> 🛠️\n
🎯 <b>ᴛ ᴀ ʀ ɢ ᴇ ᴛ ɪ ɴ ɢ</b>
🔸 <code>.at &lt;ʟɪɴᴋ&gt;</code> : ʟᴏᴄᴋ ᴠɪᴀ ʟɪɴᴋ
🔸 <code>.st1 &lt;ᴛᴇxᴛ&gt;</code> : ᴀᴅᴅ ᴘʀᴇғɪx
🔸 <code>.st2 &lt;ᴛᴇxᴛ&gt;</code> : ᴀᴅᴅ sᴜғғɪx

💬 <b>ʟ ɪ ᴠ ᴇ  ᴄ ʜ ᴀ ᴛ (sᴍᴀʀᴛ ᴛʀᴀᴄᴋ)</b>
👉 <i>ᴀғᴛᴇʀ ʟᴏᴄᴋɪɴɢ, ᴛʏᴘᴇ ᴀɴʏᴛʜɪɴɢ ʜᴇʀᴇ (ɪᴛ ᴡɪʟʟ sᴛᴀʏ ʜᴇʀᴇ) ᴀɴᴅ ᴀᴜᴛᴏ-ʀᴇᴘʟʏ ᴛᴏ ᴛᴀʀɢᴇᴛ's ʟᴀᴛᴇsᴛ ᴍsɢ!</i>

⚔️ <b>ᴀ ᴛ ᴛ ᴀ ᴄ ᴋ s</b>
🔸 <code>.fontraid [font] &lt;ʟɪɴᴋ&gt;</code> : ғᴏɴᴛ ʀᴀɪᴅ
🔸 <code>.oneword &lt;ʟɪɴᴋ&gt; [text]</code> : ᴏɴᴇᴡᴏʀᴅ ᴍᴏᴅᴇ
🔸 <code>.faketype &lt;ʟɪɴᴋ&gt;</code> : ɢʜᴏsᴛ ᴛʏᴘɪɴɢ

⚙️ <b>s ᴇ ᴛ ᴛ ɪ ɴ ɢ s</b>
🔸 <code>.delay [sec]</code> : sᴇᴛ sᴘᴇᴇᴅ
🔸 <code>.stop</code> : ᴋɪʟʟ ᴀʟʟ ᴀɴᴅ ʀᴇsᴛᴏʀᴇ ɴᴏʀᴍᴀʟ ᴄʜᴀᴛ!</blockquote>"""
            await send_inverted_msg(event.client, uid, help_msg)
            try: await event.delete()
            except Exception: pass
            return

        if cmd in ['.setstopmsg', '!setstopmsg']:
            if len(text.split()) > 1: session['default_stop_msg'] = text.split(maxsplit=1)[1].strip()
            await send_inverted_msg(event.client, uid, f"<blockquote>✅ sᴛᴏᴘ ᴍᴇssᴀɢᴇ ᴜᴘᴅᴀᴛᴇᴅ.</blockquote>")
            try: await event.delete()
            except Exception: pass
            return

        # 🎯 STRICT LINK TARGETING (.at https://t.me/...)
        if cmd in ['.at', '!at', 'at']:
            parts = text.split(maxsplit=1)
            if len(parts) > 1:
                raw_link = parts[1].strip().replace("https://t.me/", "").replace("@", "")
                if "/" in raw_link:
                    split_data = raw_link.split("/")
                    if split_data[0] == "c":
                        session['target_chat'] = int("-100" + split_data[1])
                        session['target_msg_id'] = int(split_data[2])
                    else:
                        chat_part = split_data[0]
                        session['target_chat'] = int(chat_part) if chat_part.lstrip('-').isdigit() else chat_part
                        session['target_msg_id'] = int(split_data[1])
                    try:
                        msg_obj = await event.client.get_messages(session['target_chat'], ids=session['target_msg_id'])
                        session['target_user'] = msg_obj.sender_id if msg_obj and getattr(msg_obj, 'sender_id', None) else None
                        await send_inverted_msg(event.client, uid, f"<blockquote>🎯 <b>ᴛᴀʀɢᴇᴛ ʟᴏᴄᴋᴇᴅ ᴠɪᴀ ʟɪɴᴋ!</b>\n👤 ᴜsᴇʀ: <code>{session['target_user']}</code>\n\n🟢 <b>ʟ ɪ ᴠ ᴇ  ʀ ᴇ ʟ ᴀ ʏ  ᴏ ɴ :</b> <i>ɴᴏᴡ ᴀɴʏᴛʜɪɴɢ ʏᴏᴜ ᴛʏᴘᴇ ʜᴇʀᴇ ᴡɪʟʟ ᴀᴜᴛᴏ-ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇɪʀ ʟᴀᴛᴇsᴛ ᴍᴇssᴀɢᴇ!</i></blockquote>")
                    except Exception:
                        session['target_user'] = None
                        await send_inverted_msg(event.client, uid, "<blockquote>🎯 <b>ᴛᴀʀɢᴇᴛ ᴍᴇssᴀɢᴇ ʟᴏᴄᴋᴇᴅ (ʟɪɴᴋ)!</b>\n\n🟢 <b>ʟ ɪ ᴠ ᴇ  ʀ ᴇ ʟ ᴀ ʏ  ᴏ ɴ :</b> <i>ɴᴏᴡ ᴀɴʏᴛʜɪɴɢ ʏᴏᴜ ᴛʏᴘᴇ ʜᴇʀᴇ ᴡɪʟʟ ɢᴏ ᴛᴏ ᴛʜᴇ ᴛᴀʀɢᴇᴛ!</i></blockquote>")
                else:
                    session['target_chat'] = int(raw_link) if raw_link.lstrip('-').isdigit() else raw_link
                    session['target_msg_id'] = None
                    session['target_user'] = None
                    await send_inverted_msg(event.client, uid, "<blockquote>✅ <b>ɢʀᴏᴜᴘ sᴇᴛ! (ɴᴏ ᴍᴇssᴀɢᴇ ʟɪɴᴋ)</b>\n\n🟢 <b>ʟ ɪ ᴠ ᴇ  ʀ ᴇ ʟ ᴀ ʏ  ᴏ ɴ :</b> <i>ɴᴏᴡ ᴀɴʏᴛʜɪɴɢ ʏᴏᴜ ᴛʏᴘᴇ ʜᴇʀᴇ ᴡɪʟʟ ɢᴏ ᴛᴏ ᴛʜᴇ ᴛᴀʀɢᴇᴛ!</i></blockquote>")

                session['is_active'] = True
            else:
                await send_inverted_msg(event.client, uid, "<blockquote>❌ <b>ᴇʀʀᴏʀ: ᴘʀᴏᴠɪᴅᴇ ᴀ ʟɪɴᴋ!</b></blockquote>")
            
            try: await event.delete()
            except Exception: pass
            return

        if cmd in ['.st1', '!st1']:
            if len(text.split()) > 1: session['prefix_text'] = text.split(maxsplit=1)[1].strip()
            await send_inverted_msg(event.client, uid, f"<blockquote>✅ <b>ᴘʀᴇғɪx sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ!</b></blockquote>")
            try: await event.delete()
            except Exception: pass
            return

        if cmd in ['.st2', '!st2']:
            if len(text.split()) > 1: session['suffix_text'] = text.split(maxsplit=1)[1].strip()
            await send_inverted_msg(event.client, uid, f"<blockquote>✅ <b>sᴜғғɪx sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ!</b></blockquote>")
            try: await event.delete()
            except Exception: pass
            return

        # 🔥 YAHI STOP COMMAND SAB KUCH BAND KAREGA 🔥
        if cmd in ['.stop', '!stop', 'stop']:
            session['is_active'] = False
            session['target_chat'] = None
            session['target_user'] = None
            session['target_msg_id'] = None
            session['prefix_text'] = None
            session['suffix_text'] = None

            session['oneword_active'] = False
            session['fontraid_active'] = False
            session['faketype_active'] = False

            if session.get('oneword_task'): session['oneword_task'].cancel()
            if session.get('fontraid_task'): session['fontraid_task'].cancel()
            if session.get('faketype_task'): session['faketype_task'].cancel()

            await send_inverted_msg(event.client, uid, "<blockquote>🛑 <b>ᴀʟʟ ᴛᴀʀɢᴇᴛs sᴛᴏᴘᴘᴇᴅ! sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ɪs ɴᴏᴡ ɴᴏʀᴍᴀʟ!</b></blockquote>")
            try: await event.delete()
            except Exception: pass
            return

