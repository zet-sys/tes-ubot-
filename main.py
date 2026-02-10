import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===================== CONFIG =====================
API_ID = 22410897          # isi dari my.telegram.org
API_HASH = "a746b342a0fab522229835892ead0942"    # isi dari my.telegram.org
BOT_TOKEN = "8071451055:AAGEhOgfjv343wpVcE3sRpMM-ZW1CFU0OSE"  # bot Telegram

# ===================== INIT =======================
bot = Client("bot_client", bot_token=BOT_TOKEN)
userbot = Client("user_client", api_id=API_ID, api_hash=API_HASH)

login_data = {}  # simpan nomor + code_hash sementara

# ===================== PANEL / MENU ====================
def panel_main():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛠 Tools", "menu_tools"),
            InlineKeyboardButton("👥 Group", "menu_group")
        ],
        [
            InlineKeyboardButton("📢 Share", "menu_share"),
            InlineKeyboardButton("⚙️ System", "menu_system")
        ],
        [
            InlineKeyboardButton("❌ Logout", "menu_close")
        ]
    ])

def panel_back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Back", "menu_back")]
    ])

def panel_tools():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(".ping", "noop"),
            InlineKeyboardButton(".time", "noop"),
            InlineKeyboardButton(".id", "noop")
        ],
        [
            InlineKeyboardButton(".b64", "noop"),
            InlineKeyboardButton(".rev", "noop"),
            InlineKeyboardButton(".calc", "noop")
        ],
        [InlineKeyboardButton("⬅ Back", "menu_back")]
    ])

def panel_group():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(".tagall", "noop"),
            InlineKeyboardButton(".purge", "noop")
        ],
        [
            InlineKeyboardButton(".pin", "noop"),
            InlineKeyboardButton(".kick", "noop")
        ],
        [InlineKeyboardButton("⬅ Back", "menu_back")]
    ])

def panel_share():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(".addtarget", "noop"),
            InlineKeyboardButton(".setshare", "noop")
        ],
        [
            InlineKeyboardButton(".share", "noop"),
            InlineKeyboardButton(".targets", "noop")
        ],
        [InlineKeyboardButton("⬅ Back", "menu_back")]
    ])

def panel_system():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(".auto on/off", "noop"),
            InlineKeyboardButton(".afk", "noop")
        ],
        [
            InlineKeyboardButton(".note", "noop"),
            InlineKeyboardButton(".notes", "noop")
        ],
        [InlineKeyboardButton("⬅ Back", "menu_back")]
    ])

# ===================== BOT HANDLER ====================
@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Selamat datang! Klik tombol login untuk userbot:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔑 Login Userbot", "login_userbot")]
        ])
    )

# ===================== CALLBACK ====================
@bot.on_callback_query()
async def cb(client, query):
    data = query.data

    # LOGIN FLOW
    if data == "login_userbot":
        await query.message.edit("Masukkan nomor Telegram (contoh: +6281234567890):")
        bot.add_handler(filters.private & filters.text, input_number, group=1)
        await query.answer()
        return

    # PANEL MENU
    if data == "menu_close":
        await query.message.edit("Userbot logout!")
        await userbot.stop()
        return

    if data == "menu_back":
        await query.message.edit("📦 **UBOT PANEL**", reply_markup=panel_main())
        return

    if data == "menu_tools":
        await query.message.edit("🛠 TOOLS MENU", reply_markup=panel_tools())
        return

    if data == "menu_group":
        await query.message.edit("👥 GROUP MENU", reply_markup=panel_group())
        return

    if data == "menu_share":
        await query.message.edit("📢 SHARE MENU", reply_markup=panel_share())
        return

    if data == "menu_system":
        await query.message.edit("⚙️ SYSTEM MENU", reply_markup=panel_system())
        return

    if data == "noop":
        await query.answer("Command ini harus diketik manual 👍", show_alert=True)
        return

# ===================== LOGIN HANDLER =================
async def input_number(client, message):
    phone = message.text.strip()
    try:
        async with userbot:
            code = await userbot.send_code(phone)
        login_data["phone"] = phone
        login_data["code_hash"] = code.phone_code_hash
        await message.reply(f"Nomor diterima: {phone}\nSilakan kirim OTP yang dikirim Telegram.")
        bot.add_handler(filters.private & filters.text, input_otp, group=2)
        bot.remove_handler(input_number, group=1)
    except Exception as e:
        await message.reply(f"❌ Gagal kirim kode OTP: {e}")

async def input_otp(client, message):
    otp = message.text.strip()
    phone = login_data.get("phone")
    code_hash = login_data.get("code_hash")
    if not phone or not code_hash:
        await message.reply("Error: nomor belum diterima atau kode OTP tidak tersedia.")
        return
    try:
        async with userbot:
            await userbot.sign_in(phone_number=phone, phone_code_hash=code_hash, code=otp)
        await message.reply("✅ Userbot login sukses! Panel aktif.", reply_markup=panel_main())
    except Exception as e:
        await message.reply(f"❌ Login gagal: {e}")
    bot.remove_handler(input_otp, group=2)

# ===================== RUN BOT ======================
async def main():
    await bot.start()
    print("Bot Telegram berjalan... Tunggu user login OTP.")
    await asyncio.get_event_loop().create_future()  # keep alive

asyncio.run(main())
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
