import random
import asyncio
from telethon.tl.functions.messages import SendMessageRequest
from telethon.extensions import html

user_settings = {}

def get_user_settings(uid):
    if uid not in user_settings:
        user_settings[uid] = {
            'target_chat': None, 'target_user': None, 'target_msg_id': None,
            'prefix_text': None, 'suffix_text': None, 'is_active': False,
            'oneword_active': False, 'oneword_text': "", 'oneword_delay': 1.0, 'oneword_task': None,
            'fontraid_active': False, 'fontraid_task': None,
            'faketype_active': False, 'faketype_task': None,
            'raid_delay': 1.0,
            'default_stop_msg': '🛑 Operation Stopped By Sniper Master! 🛑'
        }
    return user_settings[uid]

MY_PICS = [
    "https://files.catbox.moe/7g5h40.png",
    "https://files.catbox.moe/3zxn2c.png",
    "https://files.catbox.moe/ichp4m.jpg",
    "https://files.catbox.moe/l4s4rx.jpg",
    "https://files.catbox.moe/tzp8ll.png"
]

def get_random_pic():
    return random.choice(MY_PICS)

async def send_inverted_msg(client, chat_id, html_text):
    pic_link = get_random_pic()
    if html_text.startswith("<blockquote>"):
        full_text = f"<blockquote><a href='{pic_link}'>&#x200B;</a>{html_text[12:]}"
    else:
        full_text = f"<a href='{pic_link}'>&#x200B;</a>{html_text}"
    try:
        msg_text, msg_entities = html.parse(full_text)
        peer = await client.get_input_entity(chat_id)
        await client(SendMessageRequest(
            peer=peer, message=msg_text, random_id=random.randint(1, 2**63 - 1),
            entities=msg_entities, invert_media=True
        ))
    except Exception:
        await client.send_message(chat_id, full_text, parse_mode="html", link_preview=True)

# 🔥 LIVE RADAR TRACKER 🔥
async def get_target_reply_id(client, chat, target_user, target_msg_id):
    if target_user:
        try:
            async for msg in client.iter_messages(chat, limit=30):
                if msg.sender_id == target_user and not getattr(msg, 'empty', False):
                    return msg.id
            async for msg in client.iter_messages(chat, from_user=target_user, limit=1):
                if not getattr(msg, 'empty', False):
                    check = await client.get_messages(chat, ids=msg.id)
                    if check and not getattr(check, 'empty', False):
                        return msg.id
        except Exception: pass
        return target_msg_id if target_msg_id else None
    else:
        if target_msg_id:
            try:
                check_msg = await client.get_messages(chat, ids=target_msg_id)
                if check_msg and not getattr(check_msg, 'empty', False): return target_msg_id
            except Exception: pass
        return None

