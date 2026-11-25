import asyncio
import os
import random  # 🔥 RANDOM LINE PICK KARNE KE LIYE 🔥
from telethon import events
from utils import get_user_settings, send_inverted_msg, get_target_reply_id

# 🔥 WAHI SMALL CAPS FONT 🔥
NORMAL_TEXT = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
FONTS_DICT = {
    'outline': '𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ',
    'bold': '𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭',
    'script': '𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩',
    'square': '🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉'
}

def apply_font(text, font_name):
    if font_name in FONTS_DICT:
        return text.translate(str.maketrans(NORMAL_TEXT, FONTS_DICT[font_name]))
    return text

def get_file_msg():
    if os.path.exists("raid_msg.txt"):
        with open("raid_msg.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content: return content
    return "☠️ FILE ME KUCH NAHI HAI YA FILE NAHI BANI! ☠️"

# 🔥 NAYA RANDOM LINE SYSTEM 🔥
async def run_fontraid(client, uid, font, text):
    session = get_user_settings(uid)
    
    # Text ko alag-alag lines me tod dega
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        lines = ["☠️ KHALI HAI ☠️"]

    while session.get('fontraid_active'):
        reply_id = await get_target_reply_id(client, session['target_chat'], session['target_user'], session['target_msg_id'])
        
        # 🔥 Har baar ek RANDOM line uthayega 🔥
        random_line = random.choice(lines)
        styled_text = apply_font(random_line, font)
        
        if session.get('target_chat'):
            try:
                if reply_id: asyncio.create_task(client.send_message(session['target_chat'], styled_text, reply_to=reply_id))
                else: asyncio.create_task(client.send_message(session['target_chat'], styled_text))
            except Exception: pass
        await asyncio.sleep(session.get('raid_delay', 1.0))

async def run_oneword(client, uid, words_list):
    session = get_user_settings(uid)
    while session.get('oneword_active'):
        reply_id = await get_target_reply_id(client, session['target_chat'], session['target_user'], session['target_msg_id'])
        
        if not reply_id and session.get('target_user'):
            await client.send_message(uid, "<blockquote>❌ <b>ᴀʟᴇʀᴛ:</b> ᴛᴀʀɢᴇᴛ ᴍᴇssᴀɢᴇ ᴅᴇʟᴇᴛᴇᴅ! ᴏɴᴇᴡᴏʀᴅ sᴘᴀᴍ sᴛᴏᴘᴘᴇᴅ.</blockquote>")
            session['oneword_active'] = False
            break

        for word in words_list:
            if not session.get('oneword_active'): break
            final_word = word
            if session['prefix_text']: final_word = f"{session['prefix_text']} {final_word}"
            if session['suffix_text']: final_word = f"{final_word} {session['suffix_text']}"
            
            try:
                if reply_id: asyncio.create_task(client.send_message(session['target_chat'], final_word.strip(), reply_to=reply_id))
                else: asyncio.create_task(client.send_message(session['target_chat'], final_word.strip()))
            except Exception: pass
            await asyncio.sleep(session.get('raid_delay', 1.0))

def setup(client, uid):
    @client.on(events.NewMessage())
    async def raid_handler(event):
        
        # 🔥 STRICT LOCK: ONLY SAVED MESSAGES 🔥
        if event.chat_id != uid: return
        
        session = get_user_settings(uid)
        text = event.raw_text.strip()
        cmd = text.lower().split()[0] if text else ""

        # 🟢 UNIVERSAL DELAY COMMAND 🟢
        if cmd in ['.delay', '!delay', 'delay']:
            parts = text.split(maxsplit=1)
            if len(parts) > 1:
                try:
                    delay = float(parts[1].strip())
                    session['raid_delay'] = delay
                    await event.delete()
                    await send_inverted_msg(event.client, uid, f"<blockquote>✅ <b>GLOBAL SPEED SET TO:</b> <code>{delay}s</code></blockquote>")
                except ValueError:
                    await event.delete()
                    await event.respond("<blockquote>❌ <b>INVALID SPEED! Use numbers like 0.1, 0.5, 2.0</b></blockquote>")
            return

        # 🟢 FONT RAID (SIRF FILE SE LEGA) 🟢
        if cmd in ['.fontraid', '!fontraid', 'fontraid']:
            parts = text.split(maxsplit=2) 
            if len(parts) >= 3:
                font_name = parts[1].lower()
                raw_link = parts[2].strip().replace("https://t.me/", "").replace("@", "")
                
                raid_text = get_file_msg()

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
                    except Exception: session['target_user'] = None
                else:
                    session['target_chat'] = int(raw_link) if raw_link.lstrip('-').isdigit() else raw_link
                    session['target_msg_id'] = None
                    session['target_user'] = None

                session['is_active'] = True
                session['fontraid_active'] = True
                if session.get('fontraid_task'): session['fontraid_task'].cancel()
                session['fontraid_task'] = asyncio.create_task(run_fontraid(event.client, uid, font_name, raid_text))
                
                await event.delete()
                await send_inverted_msg(event.client, uid, f"<blockquote>🚀 <b>RANDOM LINE FONT RAID STARTED!</b>\n🔠 <b>Font:</b> <code>{font_name}</code>\n⚡ <b>Speed:</b> <code>{session.get('raid_delay', 1.0)}s</code></blockquote>")
            else:
                await event.delete()
                await event.respond("<blockquote>❌ <b>Usage:</b> <code>.fontraid [font] [link]</code>\n(Message automatically raid_msg.txt se lega)</blockquote>")
            return
            
        if cmd in ['.stopfontraid', '!stopfontraid', 'stopfontraid']:
            session['fontraid_active'] = False
            if session.get('fontraid_task'): session['fontraid_task'].cancel()
            if session.get('target_chat'):
                try: await event.client.send_message(session['target_chat'], session.get('default_stop_msg'))
                except Exception: pass
            await event.delete()
            await send_inverted_msg(event.client, uid, "<blockquote>🛑 <b>FONT RAID STOPPED!</b></blockquote>")
            return

        # 🟢 ONEWORD (SIRF MANUAL LIKHA HUA LEGA) 🟢
        if cmd in ['.oneword', '!oneword', 'oneword']:
            parts = text.split(maxsplit=2)
            if len(parts) == 3: 
                raw_link = parts[1].strip().replace("https://t.me/", "").replace("@", "")
                words_list = parts[2].strip().split()

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
                    except Exception: session['target_user'] = None
                else:
                    session['target_chat'] = int(raw_link) if raw_link.lstrip('-').isdigit() else raw_link
                    session['target_msg_id'] = None
                    session['target_user'] = None

                session['is_active'] = True
                session['oneword_active'] = True
                if session.get('oneword_task'): session['oneword_task'].cancel()
                session['oneword_task'] = asyncio.create_task(run_oneword(event.client, uid, words_list))
                
                await event.delete()
                await send_inverted_msg(event.client, uid, f"<blockquote>🚀 <b>ONEWORD STARTED!</b>\n🎯 <b>Target Locked directly from link!</b>\n⚡ <b>Speed:</b> <code>{session.get('raid_delay', 1.0)}s</code></blockquote>")
            else:
                await event.delete()
                await event.respond("<blockquote>❌ <b>Message kahan hai bhai?</b>\nUsage: <code>.oneword [link] Tera Message Yahan Likh</code></blockquote>")
            return
            
        if cmd in ['.stoponeword', '!stoponeword', 'stoponeword']:
            session['oneword_active'] = False
            if session.get('oneword_task'): session['oneword_task'].cancel()
            await event.delete()
            await send_inverted_msg(event.client, uid, "<blockquote>🛑 <b>ONEWORD STOPPED!</b></blockquote>")
            return

