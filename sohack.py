from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import random
import asyncio
import json
import os

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
NORMAL_BALLS = [
    "⚾️ 1 run", "⚾️ 2 run", "⚾️ 3 run",
    "⚾️ 4 run", "⚾️ 6 run",
    "⚾️ Bowled", "⚾️ Run out",
    "⚾️ Wide", "⚾️ No ball"
]

# ================== TOSS DATA ==================
TOSS_MODES = [
    ["Heads", "Tails"],  # random
    ["Heads"],           # fixed heads
    ["Tails"]            # fixed tails
]
toss_mode = 0

# ================== FIX STATE ==================
FIXED_BALLS = []
FIX_INDEX = 0

# ================== ADMIN ==================
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

# ================== FIXED OVER GENERATOR ==================
def generate_fixed_over(target):
    balls = []
    remaining = target
    legal_balls = 0

    while legal_balls < 6:
        balls_left = 6 - legal_balls
        max_possible = balls_left * 6

        # 🔒 force sixes if required
        if remaining == max_possible:
            balls.append("⚾️ 6 run")
            remaining -= 6
            legal_balls += 1
            continue

        options = []

        # scoring shots (only if still reachable)
        for r, label in [
            (6, "⚾️ 6 run"),
            (4, "⚾️ 4 run"),
            (3, "⚾️ 3 run"),
            (2, "⚾️ 2 run"),
            (1, "⚾️ 1 run"),
        ]:
            if remaining - r >= 0 and remaining - r <= (balls_left - 1) * 6:
                options.append(label)

        # extras (+1 run, no legal ball)
        if remaining - 1 >= 0 and remaining - 1 <= max_possible:
            options += ["⚾️ Wide", "⚾️ No ball"]

        # wickets only if safe
        if remaining <= (balls_left - 1) * 6:
            options += ["⚾️ Bowled", "⚾️ Run out"]

        # absolute safety fallback
        if not options:
            options.append("⚾️ 6 run")

        outcome = random.choice(options)
        balls.append(outcome)

        # apply runs
        if "6 run" in outcome:
            remaining -= 6
            legal_balls += 1
        elif "4 run" in outcome:
            remaining -= 4
            legal_balls += 1
        elif "3 run" in outcome:
            remaining -= 3
            legal_balls += 1
        elif "2 run" in outcome:
            remaining -= 2
            legal_balls += 1
        elif "1 run" in outcome:
            remaining -= 1
            legal_balls += 1
        elif "Wide" in outcome or "No ball" in outcome:
            remaining -= 1
        else:  # wicket
            legal_balls += 1

    return balls



def run_value(ball):
    if "1 run" in ball: return 1
    if "2 run" in ball: return 2
    if "3 run" in ball: return 3
    if "4 run" in ball: return 4
    if "6 run" in ball: return 6
    if "Wide" in ball or "No ball" in ball: return 1
    return 0

# ================== GROUP TRACKING ==================
@client.on(events.ChatAction)
async def track_bot_chats(event):
    me = await client.get_me()

    if (event.user_added or event.user_joined) and event.user_id == me.id:
        chat = await event.get_chat()
        JOINED_GROUPS[str(chat.id)] = {
            "title": getattr(chat, "title", "Unknown"),
            "link": f"https://t.me/{chat.username}" if getattr(chat, "username", None) else "PRIVATE"
        }
        save_groups()

    if event.user_left and event.user_id == me.id:
        JOINED_GROUPS.pop(str(event.chat_id), None)
        save_groups()

# ================== COMMANDS ==================
@client.on(events.NewMessage(pattern=r'(?i)/do .+'))
async def set_toss(event):
    global toss_mode
    if not await is_admin(event): return

    try:
        toss_mode = int(event.text.split()[1])
        if toss_mode not in (0, 1, 2):
            raise ValueError
    except:
        await event.reply("❌ Use /do 0 (random), /do 1 (heads), /do 2 (tails)")
        return

    await event.reply("✅ TOSS MODE UPDATED")

@client.on(events.NewMessage(pattern=r'(?i)/toss'))
async def toss(event):
    if not await is_admin(event): return
    await event.reply(random.choice(TOSS_MODES[toss_mode]))

@client.on(events.NewMessage(pattern=r'(?i)/fix .+'))
async def fix_over(event):
    global FIXED_BALLS, FIX_INDEX
    if not await is_admin(event): return

    try:
        target = int(event.text.split()[1])
    except:
        await event.reply("❌ Invalid number")
        return

    FIXED_BALLS = generate_fixed_over(target)
    FIX_INDEX = 0
    await event.reply(f"🎯 OVER FIXED TO {target} RUNS")

@client.on(events.NewMessage(pattern=r'(?i)/ball'))
async def ball(event):
    global FIX_INDEX, FIXED_BALLS
    if not await is_admin(event): return

    if FIX_INDEX < len(FIXED_BALLS):
        outcome = FIXED_BALLS[FIX_INDEX]
        FIX_INDEX += 1
    else:
        outcome = random.choice(NORMAL_BALLS)

    await event.reply(f"{outcome}")

    if FIX_INDEX >= 6:
        FIXED_BALLS = []
        FIX_INDEX = 0

@client.on(events.NewMessage(pattern=r'(?i)/over'))
async def over(event):
    global FIX_INDEX, FIXED_BALLS
    if not await is_admin(event):
        return

    legal_balls = 0
    ball_no = 1
    total = 0

    while legal_balls < 6:
        # get next outcome
        if FIX_INDEX < len(FIXED_BALLS):
            outcome = FIXED_BALLS[FIX_INDEX]
            FIX_INDEX += 1
        else:
            outcome = random.choice(NORMAL_BALLS)

        # add runs
        total += run_value(outcome)

        # reply
        await event.reply(f"𝐁𝐚𝐥𝐥 0.{ball_no}  {outcome}")
        await asyncio.sleep(1)

        # legal delivery check
        if "Wide" not in outcome and "No ball" not in outcome:
            legal_balls += 1
            ball_no += 1
        # else → extra ball, same ball number

    await event.reply(f"📊 SCORECARD\n\nTHIS OVER: {total} RUNS")

    # reset fix after one over
    FIXED_BALLS = []
    FIX_INDEX = 0


# ================== START ==================
print("🤖 BOT RUNNING")

if JOINED_GROUPS:
    print("\n📋 KNOWN GROUPS:")
    for cid, d in JOINED_GROUPS.items():
        print(f"• {d['title']} | {cid} | {d['link']}")
else:
    print("\n📋 No stored groups yet")

client.start()
client.run_until_disconnected()



