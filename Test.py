import os
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction

API_ID = 32112636
API_HASH = "3ca47bf341eeb3a3f0b520a07da67d90"

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

MSG_FILE = "messages.txt"
VOICE_FILE = "voices.txt"

OWNERS = {6336493222}

active_bully1 = {}
active_bully2 = {}
active_bully3 = {}
active_hide = {}
custom_names = {}
global_count = 3

capturing_messages = False
capturing_voices = False

owner_filter = filters.me | filters.user(list(OWNERS))

@app.on_message(filters.command("Add_Message", prefixes="/") & owner_filter)
async def start_add_message(client: Client, message: Message):
    global capturing_messages, capturing_voices
    try:
        await message.delete()
    except Exception:
        pass
    capturing_messages = True
    capturing_voices = False

@app.on_message(filters.command("stop_message", prefixes="/") & owner_filter)
async def stop_add_message(client: Client, message: Message):
    global capturing_messages
    try:
        await message.delete()
    except Exception:
        pass
    capturing_messages = False

@app.on_message(filters.command("Add_voice", prefixes="/") & owner_filter)
async def start_add_voice(client: Client, message: Message):
    global capturing_messages, capturing_voices
    try:
        await message.delete()
    except Exception:
        pass
    capturing_voices = True
    capturing_messages = False

@app.on_message(filters.command("stop_voice", prefixes="/") & owner_filter)
async def stop_add_voice(client: Client, message: Message):
    global capturing_voices
    try:
        await message.delete()
    except Exception:
        pass
    capturing_voices = False

@app.on_message(filters.text & owner_filter & ~filters.command(["Add_Message", "stop_message", "Add_voice", "stop_voice", "speed", "Count", "Id", "name", "Bully1", "Stopbully1", "Bully2", "Stopbully2", "Bully3", "Stopbully3", "Hide", "Stophide", "Help"]))
async def capture_owner_inputs(client: Client, message: Message):
    global capturing_messages
    if capturing_messages and message.text:
        with open(MSG_FILE, "a", encoding="utf-8") as f:
            f.write(message.text + "\n")
        try:
            await message.delete()
        except Exception:
            pass

@app.on_message(filters.voice & owner_filter)
async def capture_owner_voices(client: Client, message: Message):
    global capturing_voices
    if capturing_voices and message.voice:
        file_id = message.voice.file_id
        with open(VOICE_FILE, "a", encoding="utf-8") as f:
            f.write(file_id + "\n")
        try:
            await message.delete()
        except Exception:
            pass

def get_random_messages(count=3):
    if not os.path.exists(MSG_FILE):
        return [f"စံနှုန်းစာသား {i+1}" for i in range(count)]
    with open(MSG_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if not lines:
        return [f"စံနှုန်းစာသား {i+1}" for i in range(count)]
    if len(lines) >= count:
        return random.sample(lines, count)
    else:
        return [random.choice(lines) for _ in range(count)]

def get_random_voices(count=2):
    if not os.path.exists(VOICE_FILE):
        return []
    with open(VOICE_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if not lines:
        return []
    if len(lines) >= count:
        return random.sample(lines, count)
    else:
        return [random.choice(lines) for _ in range(count)]

@app.on_message(filters.command("speed", prefixes="/") & owner_filter)
async def set_speed(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        return
    try:
        delay_time = float(args[1])
        if delay_time < 0:
            raise ValueError()
        app.default_speed = delay_time
    except ValueError:
        pass

@app.on_message(filters.command("Count", prefixes="/") & owner_filter)
async def set_count(client: Client, message: Message):
    global global_count
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        return
    try:
        cnt = int(args[1])
        if cnt <= 0:
            raise ValueError()
        global_count = cnt
    except ValueError:
        pass

@app.on_message(filters.command("Id", prefixes="/") & owner_filter)
async def show_id_info(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    target_id = None
    target_name = "Unknown"
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name or "Unknown"
    else:
        args = message.command
        if len(args) >= 2:
            try:
                target_id = int(args[1])
            except ValueError:
                pass
    if not target_id:
        return
    mono_ui = (
        "SYSTEM // ID INFO\n"
        f"Name : {target_name}\n"
        f"ID   : `{target_id}`\n"
        f"Copy : `{target_id}`"
    )
    await client.send_message(message.chat.id, mono_ui)

@app.on_message(filters.command("name", prefixes="/") & owner_filter)
async def set_custom_name(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return
    try:
        target_id = int(args[1])
    except ValueError:
        return
    name_text = args[2]
    custom_names[target_id] = name_text

@app.on_message(filters.command("Bully1", prefixes="/") & owner_filter)
async def start_bully1(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        return
    try:
        target_id = int(args[1])
        active_bully1[target_id] = True
    except ValueError:
        pass

@app.on_message(filters.command("Stopbully1", prefixes="/") & owner_filter)
async def stop_bully1(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        active_bully1.clear()
        return
    try:
        target_id = int(args[1])
        active_bully1[target_id] = False
    except ValueError:
        pass

@app.on_message(filters.command("Bully2", prefixes="/") & owner_filter)
async def start_bully2(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        return
    try:
        target_id = int(args[1])
        active_bully2[target_id] = True
    except ValueError:
        pass

@app.on_message(filters.command("Stopbully2", prefixes="/") & owner_filter)
async def stop_bully2(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        active_bully2.clear()
        return
    try:
        target_id = int(args[1])
        active_bully2[target_id] = False
    except ValueError:
        pass

@app.on_message(filters.command("Bully3", prefixes="/") & owner_filter)
async def start_bully3(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
        active_bully3[target_id] = True

@app.on_message(filters.command("Stopbully3", prefixes="/") & owner_filter)
async def stop_bully3(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
        active_bully3[target_id] = False
    else:
        active_bully3.clear()

@app.on_message(filters.command("Hide", prefixes="/") & owner_filter)
async def start_hide(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        return
    try:
        target_id = int(args[1])
        active_hide[target_id] = True
    except ValueError:
        pass

@app.on_message(filters.command("Stophide", prefixes="/") & owner_filter)
async def stop_hide(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    args = message.command
    if len(args) < 2:
        active_hide.clear()
        return
    try:
        target_id = int(args[1])
        active_hide[target_id] = False
    except ValueError:
        pass

@app.on_message(filters.command("Help", prefixes="/") & owner_filter)
async def help_command(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    help_text = (
        "USERBOT COMMANDS DIRECTORY\n\n"
        "/Add_Message          - Start capturing text messages\n"
        "/stop_message         - Stop capturing text messages\n"
        "/Add_voice            - Start capturing voice messages\n"
        "/stop_voice           - Stop capturing voice messages\n"
        "/Count [num]          - Set line count\n"
        "/Id (reply user msg)  - Get user ID info\n"
        "/speed [seconds]      - Set delay speed\n"
        "/name [id] [name]     - Set custom mention name\n"
        "/Bully1 [id]          - Start bully 1 for target ID\n"
        "/Stopbully1 [id]      - Stop bully 1\n"
        "/Bully2 [id]          - Start bully 2 for target ID\n"
        "/Stopbully2 [id]      - Stop bully 2\n"
        "/Bully3 (reply user)  - Start bully 3 via reply\n"
        "/Stopbully3 (reply)   - Stop bully 3 via reply\n"
        "/Hide [id]            - Start hide mode for target ID\n"
        "/Stophide [id]        - Stop hide mode"
    )
    await client.send_message(message.chat.id, help_text)

@app.on_message(filters.private | filters.group)
async def monitor_chats(client: Client, message: Message):
    if not message.from_user:
        return
    
    user_id = message.from_user.id
    user_name = custom_names.get(user_id, message.from_user.first_name or "Target")
    mention_tag = f"[{user_name}](tg://user?id={user_id})"

    delay_speed = getattr(client, "default_speed", 0.1)
    current_count = global_count

    if active_hide.get(user_id):
        try:
            await message.delete()
        except Exception:
            pass
        return

    if active_bully3.get(user_id):
        try:
            await client.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)
        except Exception:
            pass
        if delay_speed > 0:
            await asyncio.sleep(delay_speed)
        
        voice_ids = get_random_voices(2)
        if voice_ids:
            for v_id in voice_ids:
                await message.reply_voice(v_id, caption=mention_tag)
                if delay_speed > 0:
                    await asyncio.sleep(delay_speed)
        else:
            await message.reply_text(f"{mention_tag}\n(No voice files saved)")
        return

    if active_bully2.get(user_id):
        try:
            await message.delete()
        except Exception:
            pass
        random_lines = get_random_messages(current_count)
        for idx, line in enumerate(random_lines):
            try:
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            except Exception:
                pass
            if idx > 0 and delay_speed > 0:
                await asyncio.sleep(delay_speed)
            await client.send_message(message.chat.id, f"{mention_tag}\n{line}")
        return

    if active_bully1.get(user_id):
        random_lines = get_random_messages(current_count)
        for idx, line in enumerate(random_lines):
            try:
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            except Exception:
                pass
            if idx > 0 and delay_speed > 0:
                await asyncio.sleep(delay_speed)
            if idx == 0:
                await message.reply_text(f"{mention_tag}\n{line}")
            else:
                await client.send_message(message.chat.id, f"{mention_tag}\n{line}")
        return

if __name__ == "__main__":
    print("UserBot is running with Multi-Owner and Bully3 Voice features...")
    app.run()

