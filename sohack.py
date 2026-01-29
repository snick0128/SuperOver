from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import random
import asyncio
import json
import os
from itertools import combinations_with_replacement

# ================== TELEGRAM CONFIG ==================
API_ID = 1441531
API_HASH = "6e5c383bb1a3e68f7f2b435ced717a55"
SESSION = "akki"

client = TelegramClient(SESSION, API_ID, API_HASH)

SUPERADMIN_ID = 5600587227
ADMIN_CACHE = {}

# ================== STORAGE ==================
GROUP_FILE = "joined_groups.json"

def load_groups():
    if os.path.exists(GROUP_FILE):
        with open(GROUP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_groups():
    with open(GROUP_FILE, "w") as f:
        json.dump(JOINED_GROUPS, f, indent=2)

JOINED_GROUPS = load_groups()

# ================== SCORE DATA ==================
score = ["⚾️ Bowled","⚾️ 1 run","⚾️ 2 run","⚾️ 3 run","⚾️ 4 run","⚾️ 6 run","⚾️ Run out"]
rscore = score + ["⚾️ Wide","⚾️ No ball"]
score2 = ["⚾️ 2 run","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run","⚾️ Wide"]
score3 = score + ["⚾️ Wide"]

all_lst = [rscore, score2, score3]
list_to_use = all_lst[0]

ilist = []
sa = random.randint(6, 23)

# ================== ADMIN HANDLING ==================
async def get_admins(chat_id):
    if chat_id in ADMIN_CACHE:
        return ADMIN_CACHE[chat_id]

    admins = {SUPERADMIN_ID}
    try:
        async for user in client.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
            admins.add(user.id)
    except:
        pass

    ADMIN_CACHE[chat_id] = admins
    return admins

async def is_admin(event):
    admins = await get_admins(event.chat_id)
    return event.sender_id in admins

# ================== GAME LOGIC ==================
def flogic(num):
    ilist.clear()
    Flist = {
        0: ["⚾️ Bowled", "⚾️ Run out"],
        1: "⚾️ 1 run",
        2: "⚾️ 2 run",
        3: "⚾️ 3 run",
        4: "⚾️ 4 run",
        6: "⚾️ 6 run"
    }

    combos = [
        c for c in combinations_with_replacement([0,1,2,3,4,6], 6)
        if sum(c) == num
    ]

    # fallback → random over
    if not combos:
        for _ in range(6):
            ilist.append(random.choice(list_to_use))
        return

    for x in random.choice(combos):
        ilist.append(random.choice(Flist[x]) if x == 0 else Flist[x])

def calculate_runs(balls):
    total = 0
    for b in balls:
        if "1 run" in b: total += 1
        elif "2 run" in b: total += 2
        elif "3 run" in b: total += 3
        elif "4 run" in b: total += 4
        elif "6 run" in b: total += 6
    return total

# ================== TRACK GROUP JOIN / LEAVE ==================
@client.on(events.ChatAction)
async def track_bot_chats(event):
    me = await client.get_me()

    if event.user_added or event.user_joined:
        if event.user_id == me.id:
            chat = await event.get_chat()
            title = getattr(chat, "title", "Unknown")
            chat_id = str(chat.id)
            link = f"https://t.me/{chat.username}" if getattr(chat, "username", None) else "PRIVATE"

            JOINED_GROUPS[chat_id] = {
                "title": title,
                "link": link
            }
            save_groups()

            print("\n➕ BOT ADDED")
            print(title, chat_id, link)

    if event.user_left:
        if event.user_id == me.id:
            chat = await event.get_chat()
            JOINED_GROUPS.pop(str(chat.id), None)
            save_groups()

            print("\n➖ BOT REMOVED")
            print(getattr(chat, "title", "Unknown"))

# ================== COMMANDS ==================
@client.on(events.NewMessage(pattern=r'(?i)/ball'))
async def ball(event):
    if not await is_admin(event): return
    await event.reply(random.choice(ilist) if ilist else random.choice(list_to_use))

@client.on(events.NewMessage(pattern=r'(?i)/fix .+'))
async def fix_over(event):
    global sa
    if not await is_admin(event): return
    try:
        sa = int(event.text.split()[1])
    except:
        sa = random.randint(6, 23)

    flogic(sa)
    await event.reply(f"✅ OVER FIXED ({sa} RUNS)")

@client.on(events.NewMessage(pattern=r'(?i)/over'))
async def play_over(event):
    if not await is_admin(event): return

    if len(ilist) < 6:
        flogic(random.randint(6, 23))

    random.shuffle(ilist)
    balls = ilist[:6]

    for i in range(6):
        await event.reply(f"𝐁𝐚𝐥𝐥 0.{i+1} 🎾 {balls[i]}")
        await asyncio.sleep(1)

    runs = calculate_runs(balls)
    await event.reply(f"📊 SCORECARD\n\nTHIS OVER: {runs} RUNS")

# ================== START ==================
print("🤖 BOT RUNNING")

if JOINED_GROUPS:
    print("\n📋 KNOWN GROUPS:")
    for cid, data in JOINED_GROUPS.items():
        print(f"• {data['title']} | {cid} | {data['link']}")
else:
    print("\n📋 No stored groups yet")
client.start()
client.run_until_disconnected()

