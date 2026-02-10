import json, time, asyncio, base64
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = 22410897
api_hash = "a746b342a0fab522229835892ead0942"
PREFIX = "."

app = Client("ubot_full", api_id=api_id, api_hash=api_hash)

# ================= DB =================

DBF="db.json"
try:
    db=json.load(open(DBF))
except:
    db={
        "auto":False,
        "afk":False,
        "afk_text":"AFK",
        "notes":{},
        "targets":[],
        "share_text":"test"
    }
    json.dump(db,open(DBF,"w"))

def save():
    json.dump(db,open(DBF,"w"),indent=2)

# ================= PANEL =================

def main_panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("TOOLS","m_tools"),
         InlineKeyboardButton("GROUP","m_group")],
        [InlineKeyboardButton("SHARE","m_share"),
         InlineKeyboardButton("SYSTEM","m_sys")],
        [InlineKeyboardButton("Close","close")]
    ])

def back():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅ BACK","back")]])

@app.on_message(filters.me & filters.command("menu", PREFIX))
async def menu(_,m):
    await m.edit("📦 UBOT FULL PANEL", reply_markup=main_panel())

@app.on_callback_query()
async def cb(_,q):
    d=q.data

    if d=="close":
        return await q.message.delete()

    if d=="back":
        return await q.message.edit("📦 UBOT FULL PANEL", reply_markup=main_panel())

    if d=="m_tools":
        return await q.message.edit("""
TOOLS
.ping .say .edit
.time .id .info
.b64 .db64
.rev .upper .lower
.calc
""", reply_markup=back())

    if d=="m_group":
        return await q.message.edit("""
GROUP
.tagall
.purge
.pin
.unpin
.kick (reply)
""", reply_markup=back())

    if d=="m_share":
        return await q.message.edit("""
SHARE
.addtarget
.deltarget
.setshare
.share
.targets
""", reply_markup=back())

    if d=="m_sys":
        return await q.message.edit("""
SYSTEM
.auto on/off
.afk
.unafk
.note
.get
.notes
""", reply_markup=back())

# ================= TOOLS =================

@app.on_message(filters.me & filters.command("ping", PREFIX))
async def ping(_,m): await m.edit("🏓 pong")

@app.on_message(filters.me & filters.command("say", PREFIX))
async def say(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1: await m.edit(t[1])

@app.on_message(filters.me & filters.command("edit", PREFIX))
async def edit(_,m):
    if m.reply_to_message:
        t=m.text.split(maxsplit=1)
        if len(t)>1:
            await m.reply_to_message.edit(t[1])
            await m.delete()

@app.on_message(filters.me & filters.command("time", PREFIX))
async def waktu(_,m): await m.edit(time.ctime())

@app.on_message(filters.me & filters.command("id", PREFIX))
async def cid(_,m): await m.edit(str(m.chat.id))

@app.on_message(filters.me & filters.command("info", PREFIX))
async def info(_,m):
    u=await app.get_me()
    await m.edit(f"{u.first_name}\n@{u.username}\nID: {u.id}")

@app.on_message(filters.me & filters.command("b64", PREFIX))
async def b64(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1:
        await m.edit(base64.b64encode(t[1].encode()).decode())

@app.on_message(filters.me & filters.command("db64", PREFIX))
async def db64(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1:
        await m.edit(base64.b64decode(t[1]).decode())

@app.on_message(filters.me & filters.command("rev", PREFIX))
async def rev(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1: await m.edit(t[1][::-1])

@app.on_message(filters.me & filters.command("upper", PREFIX))
async def upper(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1: await m.edit(t[1].upper())

@app.on_message(filters.me & filters.command("lower", PREFIX))
async def lower(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1: await m.edit(t[1].lower())

@app.on_message(filters.me & filters.command("calc", PREFIX))
async def calc(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1:
        try:
            await m.edit(str(eval(t[1])))
        except:
            await m.edit("error")

# ================= GROUP =================

@app.on_message(filters.me & filters.command("tagall", PREFIX))
async def tagall(_,m):
    text="Tag All\n"
    async for u in app.get_chat_members(m.chat.id):
        text+=f"[{u.user.first_name}](tg://user?id={u.user.id}) "
    await m.reply(text)

@app.on_message(filters.me & filters.command("purge", PREFIX))
async def purge(_,m):
    if not m.reply_to_message: return
    for i in range(m.reply_to_message.id, m.id+1):
        try: await app.delete_messages(m.chat.id,i)
        except: pass

@app.on_message(filters.me & filters.command("pin", PREFIX))
async def pin(_,m):
    if m.reply_to_message:
        await m.reply_to_message.pin()

@app.on_message(filters.me & filters.command("unpin", PREFIX))
async def unpin(_,m):
    await app.unpin_chat_message(m.chat.id)

@app.on_message(filters.me & filters.command("kick", PREFIX))
async def kick(_,m):
    if m.reply_to_message:
        uid = m.reply_to_message.from_user.id
        await app.ban_chat_member(m.chat.id, uid)
        await app.unban_chat_member(m.chat.id, uid)

# ================= SHARE =================

@app.on_message(filters.me & filters.command("addtarget", PREFIX))
async def addt(_,m):
    if m.chat.id not in db["targets"]:
        db["targets"].append(m.chat.id)
        save()
    await m.edit("target added")

@app.on_message(filters.me & filters.command("deltarget", PREFIX))
async def delt(_,m):
    if m.chat.id in db["targets"]:
        db["targets"].remove(m.chat.id)
        save()
    await m.edit("target removed")

@app.on_message(filters.me & filters.command("targets", PREFIX))
async def targets(_,m):
    await m.edit(str(db["targets"]))

@app.on_message(filters.me & filters.command("setshare", PREFIX))
async def setshare(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1:
        db["share_text"]=t[1]
        save()
        await m.edit("set")

@app.on_message(filters.me & filters.command("share", PREFIX))
async def share(_,m):
    for gid in db["targets"]:
        try:
            await app.send_message(gid, db["share_text"])
            await asyncio.sleep(1)
        except: pass
    await m.edit("share done")

# ================= AUTO =================

@app.on_message(filters.me & filters.command("auto", PREFIX))
async def auto(_,m):
    db["auto"] = "on" in m.text
    save()
    await m.edit(f"auto {db['auto']}")

@app.on_message(filters.private & ~filters.me)
async def autoreply(_,m):
    if db["auto"]:
        await m.reply("auto reply aktif")

# ================= AFK =================

@app.on_message(filters.me & filters.command("afk", PREFIX))
async def afk(_,m):
    db["afk"]=True
    db["afk_text"]=m.text.split(maxsplit=1)[1] if " " in m.text else "AFK"
    save()
    await m.edit("AFK ON")

@app.on_message(filters.me & filters.command("unafk", PREFIX))
async def unafk(_,m):
    db["afk"]=False
    save()
    await m.edit("AFK OFF")

@app.on_message(filters.mentioned)
async def afk_reply(_,m):
    if db["afk"]:
        await m.reply(db["afk_text"])

# ================= NOTES =================

@app.on_message(filters.me & filters.command("note", PREFIX))
async def note(_,m):
    t=m.text.split(maxsplit=2)
    if len(t)>=3:
        db["notes"][t[1]]=t[2]
        save()
        await m.edit("saved")

@app.on_message(filters.me & filters.command("get", PREFIX))
async def get(_,m):
    t=m.text.split(maxsplit=1)
    if len(t)>1 and t[1] in db["notes"]:
        await m.edit(db["notes"][t[1]])

@app.on_message(filters.me & filters.command("notes", PREFIX))
async def notes(_,m):
    await m.edit(", ".join(db["notes"].keys()))

# ================= RUN =================

app.run()