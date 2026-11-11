import os
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction

# Telegram API credentials
API_ID = 30786663
API_HASH = "2cb195ed744a0fb3f051a8fd842a5fd9"

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

# File path for messages
MSG_FILE = "messages.txt"

# Owner ID fixed as requested
OWNER_ID = 6336493222

# Active states and custom configurations dictionaries
active_bully1 = {}      # {target_id: True/False}
active_bully2 = {}      # {target_id: True/False}
active_hide = {}        # {target_id: True/False}
custom_names = {}       # {target_id: "Custom Name"}
global_count = 3        # Default message count

# Owner filter check
owner_filter = filters.me | filters.user(OWNER_ID)

# 1. /Add_Message Command (Silent & Auto-delete)
@app.on_message(filters.command("Add_Message", prefixes="/") & owner_filter)
async def add_message(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
        
    text_to_add = message.text.split(maxsplit=1)
    if len(text_to_add) < 2:
        return
    
    msg_content = text_to_add[1]
    with open(MSG_FILE, "a", encoding="utf-8") as f:
        f.write(msg_content + "\n")

# Helper function to get random messages from file
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

# 2. /speed Command (Silent & Auto-delete)
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

# 3. /Count Command (Silent & Auto-delete)
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

# 4. /Id Command (Modern Mono Style Without Borders & Reply/ID Detection)
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

# 5. /name Command (Silent & Auto-delete)
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

# 6. /Bully1 Command (Silent & Auto-delete)
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

# 7. /Bully2 Command (Silent & Auto-delete)
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

# 8. /Hide Command (Silent & Auto-delete)
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

# 9. /Help Command (Help text with auto-delete)
@app.on_message(filters.command("Help", prefixes="/") & owner_filter)
async def help_command(client: Client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
        
    help_text = (
        "USERBOT COMMANDS DIRECTORY (GROUP ONLY)\n\n"
        "/Add_Message [text]   - Add text to file\n"
        "/Count [num]          - Set line count\n"
        "/Id (reply user msg)  - Get user ID info\n"
        "/speed [seconds]      - Set delay speed\n"
        "/name [id] [name]     - Set custom mention name\n"
        "/Bully1 [id]          - Start bully 1 for target ID\n"
        "/Stopbully1 [id]      - Stop bully 1\n"
        "/Bully2 [id]          - Start bully 2 for target ID\n"
        "/Stopbully2 [id]      - Stop bully 2\n"
        "/Hide [id]            - Start hide mode for target ID\n"
        "/Stophide [id]        - Stop hide mode"
    )
    await client.send_message(message.chat.id, help_text)

# 10. Incoming Message Monitor (GROUP CHATS ONLY)
@app.on_message(filters.group)
async def monitor_chats(client: Client, message: Message):
    if not message.from_user:
        return
    
    user_id = message.from_user.id
    user_name = custom_names.get(user_id, message.from_user.first_name or "Target")
    mention_tag = f"[{user_name}](tg://user?id={user_id})"

    delay_speed = getattr(client, "default_speed", 0.1)
    current_count = global_count

    # Check Hide mode
    if active_hide.get(user_id):
        try:
            await message.delete()
        except Exception:
            pass
        return

    # Check Bully2 mode (Delete message and send every line with mention tag sequentially)
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

    # Check Bully1 mode (Reply first line with mention, then send remaining lines with mention sequentially)
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
    print("UserBot is running for Owner 8837432063...")
    app.run()
