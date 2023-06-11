from telethon import TelegramClient, events
import random
import time
from itertools import combinations, combinations_with_replacement
import random

#import settings

client = TelegramClient('prateek', 1441531,'6e5c383bb1a3e68f7f2b435ced717a55')
score = ["⚾️ Bowled","⚾️ 2 run","⚾️ 1 run","⚾️ Run out","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run"]
rscore = ["⚾️ Bowled","⚾️ 2 run","⚾️ 1 run","⚾️ Run out","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run","⚾️ Wide","⚾️ No ball"]
score2 = ["⚾️ 2 run","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run","⚾️ Wide"]
score3 = ["⚾️ Bowled","⚾️ 2 run","⚾️ 1 run","⚾️ Run out","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run","⚾️ Wide"]


scoredist={"⚾️ Bowled":0,"⚾️ 2 run":2,"⚾️ 1 run":1,"⚾️ Wide":1,"⚾️ Run out":0,"⚾️ 4 run":4,"⚾️ 6 run":6,"⚾️ 3 run":3}

lambi = ["⚾️ Bowled","⚾️ 2 run","⚾️ 1 run","⚾️ Run out","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run","⚾️ Wide",'⚾️ Wide', '⚾️ 3 run', '⚾️ 2 run', '⚾️ 4 run', '⚾️ 6 run', '⚾️ Bowled', '⚾️ Run out', '⚾️ 1 run','⚾️ Wide', '⚾️ Bowled', '⚾️ 3 run', '⚾️ 1 run', '⚾️ 2 run', '⚾️ 4 run', '⚾️ 6 run',
         '⚾️ Run out','⚾️ Wide', '⚾️ Bowled', '⚾️ 3 run', '⚾️ 1 run', '⚾️ 2 run', '⚾️ 4 run', '⚾️ 6 run', '⚾️ Run out',"⚾️ Bowled","⚾️ 2 run","⚾️ 1 run","⚾️ Run out","⚾️ 4 run","⚾️ 6 run","⚾️ 3 run","⚾️ Wide",'⚾️ Wide', '⚾️ 3 run', '⚾️ 2 run', '⚾️ 4 run', '⚾️ 6 run', '⚾️ Bowled','⚾️ 1 run','⚾️ Wide', '⚾️ Bowled', '⚾️ 3 run']




all_lst=[rscore,score2,score3]
head = ["Heads"]
tail = ["Tails"]
tosso = ["Tails","Heads"]
allto = [tosso,head,tail]
list_to_use=all_lst[0]
list_use = allto[0]

ilist = []

touse = [ilist,lambi]
to = touse[0]

ts = [ ]
ts1 = []
sa = 0

my_head = [1670999439,1540276745,1790945086,1029307155,679390206,774997425,861769159] #All Admins Of the Group
all_over_run = 0

def clear():
        ts.clear()
        ts1.clear()
        
#@client.on(events.NewMessage)
#async def handler(event):
        #print("NEW MESSAGE")
        #print(event)
        #await event.respond(" ")

#settings.my()
ts1.clear()

@client.on(events.NewMessage(chats=[861769159,774997425],pattern='(?i)/set .+'))
async def handler(event):
        print("RUN")
        global list_to_use
        

        msg=event.message.message
        a=msg.split()
        print(a,a[1])
        list_to_use=all_lst[int(a[1])]
        print('##')
        await event.respond("- CHANGES DONE")

@client.on(events.NewMessage(chats=[861769159,774997425],pattern='(?i)/win .+'))
async def handler(event):
        print("RUN")
        global list_to_use
        

        msg=event.message.message
        a=msg.split()
        print(a,a[1])
        to=touse[int(a[1])]
        print('##')
        await event.respond("- CHANGES DONE")
        

@client.on(events.NewMessage(chats=[861769159,774997425],pattern='(?i)/do .+'))
async def handler(event):
        print("tOSS")
        global list_use
        

        msg=event.message.message
        a=msg.split()
        print(a,a[1])
        list_use=allto[int(a[1])]
        print('##')
        await event.respond("- CHANGES DONE")
        await event.respond("[+] UNDER THE SUPERVISION OF MY BOSS ")

@client.on(events.NewMessage(pattern=r'(?i).*/BALL'))
async def handler(event):
        global my_head
        global ilist
        msg=event.message.message
        ab= "0."
        cd  = f'{ab}/ball'

        try:
                ballist = ilist
         
                        
                        
                try:
                        n_user = event.message.peer_id.user_id
                except:
                        n_user = event.message.from_id.user_id
                #await event.reply(random.choice(list_to_use))
                        
              
                if n_user in my_head:
                        a = random.choice(ballist)
                        await event.reply(f'{cd}{a}')
                        ballist.remove(a)
                else:
                        print("not authorized")
        except IndexError:
                try:
                        n_user = event.message.peer_id.user_id
                except:
                        n_user = event.message.from_id.user_id
                await event.reply(random.choice(list_to_use))
              
                if n_user in Admin:
                        rd = random.choice(rscore)
                        await event.reply(f'{cd}{rd}')
                else:
                        await event.reply()




@client.on(events.NewMessage(pattern=r'(?i).*/toss'))
async def handler(event):
        global my_head
        try:
                n_user = event.message.peer_id.user_id
        except:
                n_user = event.message.from_id.user_id
        #await event.reply(random.choice(list_use))
      
        if n_user in my_head:
                await event.reply(random.choice(list_use))
        else:
                #await event.reply("TALK TO MY HAND")
                await event.reply()


def run():
    a = random.choice(list_to_use)
    return a

def total_ov(balls):
    if balls%6 == 0:
        s = balls/6
    s = balls%6/10+balls//6
    return s




@client.on(events.NewMessage(pattern=r'(?i).*/0ver'))
async def handler(event):


            msg=event.message.message
            a=msg.split()
            
            total_over = int(a[1])
            over = 0
            all1 = 0
            n_over = 1
            cu_ball = 1
            total_run=0
            total_balls = total_over*6
            global my_head
            all_over_run = 0
                    
            while over < total_over:
                    
                    balcount=0
                    ball=1
                    cb = 7
                    
                    while ball <7:
                        balcount+=1
                        balrun=run()
                        cur_ball = total_ov(cu_ball)
                        s_str = "𝐁𝐚𝐥𝐥 "  
                        sym = "🎾:Score "    
                        scr = "ＳＣＯＲＥＣＡＲＤ"
                        th_over = "🅣🅗🅘🅢 🅞🅥🅔🅡: "
                        space = "🏏🏏🏏🏏🏏🏏🏏🏏🏏🏏🏏"
                        to_so = "🅣🅞🅣🅐🅛 🅢🅒🅞🅡🅔 : "
                        ov = "🅞🅥🅔🅡🅢 : "
                        r = "RUN "
                        
                        
                        f_score = f'{s_str}{cur_ball}{sym}{balrun}'
                        numrun       = scoredist[balrun]
                        total_run    = total_run+numrun
                        all_over_run = all_over_run+numrun
                        #print(f'{all_over_run}_________{balrun}_____{numrun}____{total_run}')
                        if balrun=="⚾️ Wide":
                                await event.reply(f_score)
                                time.sleep(2)
                                continue
                        
                        ball+=1
                        cu_ball+=1
                                
                        try:
                                n_user = event.message.peer_id.user_id
                        except:
                                n_user = event.message.from_id.user_id
                        #await event.reply(random.choice(list_to_use))
                      
                        if n_user in my_head:
                                await event.reply(f_score)
                                time.sleep(2)
                        else:
                                await event.reply(f_score)
                                break
                        
                        
                        banner = f'{scr}\n\n{th_over}{total_run}\n\n{space}\n\n{to_so}{all_over_run}{r}\n\n{ov}{n_over}'
                    await event.reply(banner)

                    
                    
                    over+=1
                    n_over+=1
                    ts.clear()
                    if over<total_over:
                            await event.reply(f'Next Over:{n_over}')
                            print("next over")
                            time.sleep(3)
                            total_run = 0
                    
all_over_run = 0

def flogic(num):
    global ilist

    ilist.clear()
    Flist={0:["⚾️ Bowled","⚾️ Run out"] , 2 : "⚾️ 2 run"  ,  1 : "⚾️ 1 run"  ,4 : "⚾️ 4 run" , 6 : "⚾️ 6 run" , 3 : "⚾️ 3 run"}


    list1 = [0,1,2,3,4,6]

    req = num#int(input("total of random number you want"))

    ls1 = []
      
    for comb in combinations_with_replacement(list1, 6):
     if sum(comb) == req:
         ls1.append(comb)
         a = len(ls1)
    f = random.choice(ls1)
    print(a)
    print (f)

    for x in f:
        #print(x)
        ab = [0,1,0,1,1,0,1,0,0,0,1,1,0,1,0,1]
        b = random.choice(ab)
        if x == 0:
            a = Flist.get(x)[b]
            ilist.append(a)
        else:


            a = Flist.get(x)
            ilist.append(a)
        print(Flist.get(x))

sa = random.randint(6,23)
flogic(sa)

@client.on(events.NewMessage(chats=[861769159,774997425],pattern='(?i)/fix .+'))
async def handler(event):
        global sa
        print("fix")
        

        msg=event.message.message
        a=msg.split()
        sa = int(a[1])
        print('##')
        if sa == 0:
            sa = random.randint(6,23)
            flogic(sa)
        else:
        
            flogic(sa)
        await event.respond("- CHANGES DONE")
        await event.respond("[+] UNDER THE SUPERVISION OF MY BOSS ")
        print(sa)
        print(ilist)

@client.on(events.NewMessage(chats=[861769159,774997425],pattern=r'(?i).*/over'))
async def handler(event):
                        global sa
                        random.shuffle(ilist)
                        print(ilist)
                        listtouse = ilist
                        await event.reply(f'𝐁𝐚𝐥𝐥 {0.1}🎾:Score {listtouse[0]}')
                        time.sleep(2)
                        await event.reply(f'𝐁𝐚𝐥𝐥 {0.2}🎾:Score {listtouse[1]}')
                        time.sleep(2)
                        await event.reply(f'𝐁𝐚𝐥𝐥 {0.3}🎾:Score {listtouse[2]}')
                        time.sleep(2)
                        await event.reply(f'𝐁𝐚𝐥𝐥 {0.4}🎾:Score {listtouse[3]}')
                        time.sleep(2)
                        await event.reply(f'𝐁𝐚𝐥𝐥 {0.5}🎾:Score {listtouse[4]}')
                        time.sleep(2)
                        await event.reply(f'𝐁𝐚𝐥𝐥 {1.0}🎾:Score {listtouse[5]}')
                        time.sleep(2)
                        await event.reply(f'ＳＣＯＲＥＣＡＲＤ\n\n🅣🅗🅘🅢 🅞🅥🅔🅡: {sa}\n\n🏏🏏🏏🏏🏏🏏🏏🏏🏏🏏🏏\n\n🅣🅞🅣🅐🅛 🅢🅒🅞🅡🅔 : {sa}RUN\n\n🅞🅥🅔🅡🅢: 1')

                        sa = random.randint(6,23)
                        flogic(sa)

                
            
        
client.start()
client.run_until_disconnected()