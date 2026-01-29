from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import random
import time
import asyncio
from itertools import combinations_with_replacement

# ================== TELEGRAM CONFIG ==================
API_ID = 1441531
API_HASH = "6e5c383bb1a3e68f7f2b435ced717a55"
SESSION = "akki"

client = TelegramClient(SESSION, API_ID, API_HASH)

SUPERADMIN_ID = 5600587227
ADMIN_CACHE = {}  # chat_id -> set(admin_ids)

# ================== SCORE DATA ==================
score = ["⚾️ Bowled","⚾️ 2 run","⚾️ 1 run","⚾️ Run out","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run"]
rscore = score + ["⚾️ Wide","⚾️ No ball"]
score2 = ["⚾️ 2 run","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run","⚾️ Wide"]
score3 = score + ["⚾️ Wide"]

all_lst = [rscore, score2, score3]
list_to_use = all_lst[0]

tosso = ["Heads", "Tails"]
allto = [tosso, ["Heads"], ["Tails"]]
list_use = allto[0]

ilist = []
sa = random.randint(6, 23)

# ================== ADMIN HANDLING ==================
async def get_admins(chat_id):
    if chat_id in ADMIN_CACHE:
        return ADMIN_CACHE[chat_id]

    admins = {SUPERADMIN_ID}

    try:
        async for user in client.iter_participants(
            chat_id, filter=ChannelParticipantsAdmins
        ):
            admins.add(user.id)
    except:
        pass  # bot may not have permission

    ADMIN_CACHE[chat_id] = admins
    return admins

async def is_admin(event):
    admins = await get_admins(event.chat_id)
    return event.sender_id in admins

# ================== GAME LOGIC ==================
def run():
    return random.choice(list_to_use)

def flogic(num):
    ilist.clear()
    Flist = {
        0:["⚾️ Bowled","⚾️ Run out"],
        1:"⚾️ 1 run",2:"⚾️ 2 run",3:"⚾️ 3 run",
        4:"⚾️ 4 run",6:"⚾️ 6 run"
    }

    combos = [
        c for c in combinations_with_replacement([0,1,2,3,4,6], 6)
        if sum(c) == num
    ]

    # ✅ fallback if no valid fixed over exists
    if not combos:
        for _ in range(6):
            ilist.append(random.choice(list_to_use))
        return

    for x in random.choice(combos):
        ilist.append(random.choice(Flist[x]) if x == 0 else Flist[x])


# ================== COMMANDS ==================
@client.on(events.NewMessage(pattern='(?i)/set .+'))
async def set_score(event):
    global list_to_use
    if not await is_admin(event): return
    list_to_use = all_lst[int(event.text.split()[1])]
    await event.reply("✅ SCORE MODE CHANGED")

@client.on(events.NewMessage(pattern='(?i)/do .+'))
async def set_toss(event):
    global list_use
    if not await is_admin(event): return
    list_use = allto[int(event.text.split()[1])]
    await event.reply("✅ TOSS MODE CHANGED")

@client.on(events.NewMessage(pattern=r'(?i)/toss'))
async def toss(event):
    if await is_admin(event):
        await event.reply(random.choice(list_use))

@client.on(events.NewMessage(pattern=r'(?i)/ball'))
async def ball(event):
    if not await is_admin(event): return
    await event.reply(random.choice(ilist) if ilist else random.choice(list_to_use))

@client.on(events.NewMessage(pattern='(?i)/fix .+'))
async def fix_over(event):
    global sa
    if not await is_admin(event): return
    sa = int(event.text.split()[1]) or random.randint(6, 23)
    flogic(sa)
    await event.reply("✅ OVER FIXED")

@client.on(events.NewMessage(pattern=r'(?i)/over'))
async def play_over(event):
    if not await is_admin(event):
        return

    if len(ilist) < 6:
        flogic(random.randint(6, 23))

    random.shuffle(ilist)

    for i in range(6):
        await event.reply(f"𝐁𝐚𝐥𝐥 0.{i+1} {ilist[i]}")
        await asyncio.sleep(1)

    await event.reply(f"ＳＣＯＲＥＣＡＲＤ\n\n🅣🅗🅘🅢 🅞🅥🅔🅡: {sa} RUN")


# ================== START ==================
print("🤖 BOT RUNNING")
client.start()
client.run_until_disconnected()





