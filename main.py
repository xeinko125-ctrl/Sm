import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
import random
import re
import os
import logging
import libsql_experimental as libsql  # Turso client

# ==========================================
# ⚙️ CONFIG
# ==========================================
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable not set!")

OWNER_ID = 7820788748
OWNER_USERNAME = "Sir_Tokegiy"  # @Sir_Tokegiy

TURSO_URL = os.environ.get('TURSO_DATABASE_URL')
TURSO_TOKEN = os.environ.get('TURSO_AUTH_TOKEN')
if not TURSO_URL or not TURSO_TOKEN:
    raise ValueError("❌ Turso credentials not set! Add TURSO_DATABASE_URL and TURSO_AUTH_TOKEN to secrets.")

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

# ==========================================
# 📝 SAVAGE TEXTS
# ==========================================
savage_texts = [
    "ဝက်သိုးအသနားခံတာလား",
    "ဟိတ်ခွေးနာနာကိုက်",
    "ဖြစ်ထွန်းမှု့လည်းမရှိဘူး",
    "ငါ့လီးရီးပေါ်တက်ဆောင့်ပေးမှာလားမင်းမားသားက",
    "မအေလိုးနာနာကိုက်အိယောင်ဝါးမလုပ်နဲ့",
    "ဒါဆိုမင်းမေစောက်ပက်ကို 90 degrees celsiusစောင်းလိုးမယ်😂",
    "ဟိတ်ခွေး...အရိုးကိုက်မလားအောက်ထစ်ကခွေးလာမဟောင်နဲ့",
    "စောက်တောသားကျွန်ပိန်းမအေလိုးမျိုးမင်းအမေသေပီ",
    "မင်းလိုစောက်တောသားက ဘောင်ဝင်ချင်တာလားကျပ်ပြည့်အောင်ငါ့လီးလာစုပ်",
    "စောက်ပေါစကားပြောရင် စောက် emoji တကားကားနဲ့",
    "စောက်ဖာကျွန်မသား",
    "လီးထိပ်မော်တာတပ်ပီးမင်းအမေစောက်ဖုတ်ကြီးလိုးခွဲပစ်မယ်",
    "မင်းကိုမင်းလူရာဝင်ပီထင်နေတာလား",
    "မင်းရဲ့ဂုတ်ကပ်နေတဲ့ဦးနှောက်နဲ့သေချာစဥ်းစားပီးကိုက်စမ်း",
    "စောက်တောသားဆိုတာ ဖင်ခံဖို့ပဲ သိတာလား",
    "မင်းစကားပြောရင်ဖုန်းကနေပါ အပုပ်နံ့ထွက်တယ်",
    "ငါ့ရှေ့မှာ လာဟောင်မနေနဲ့ ရော့ရော့ 🦴",
    "မင်းရဲ့nameကို မြင်ရတာတောင် ငါ့ Bot က ရွံနေပြီ 🥴",
    "ဘာရပ်လုပ်နေတာလဲ typing ကလဲနှေးတုပ်နေတာပဲ ဖုန်းစောက်စုတ်နဲ့မို့လို့လား",
    "ဟားဟားအနိုင်ယူမိပြန်ပီကွာ😂",
    "မင်းရဲ့ frezz ဖြစ်နေတဲ့ brain ကို ငါ့ရဲ့ကျင်ငယ်ရေပူပူလေးနဲ့ဆေးပေးရမလား",
    "မင်းကိုဘယ်သူပေးနားလို့လဲမနားနဲ့ရုန်းထား",
    "အရင်ကတော့ရွာတို့တောတို့မှာနေမှစောက်တောသားလို့ခေါ်တာ တကယ်တော့မင်းလို ခွေးလောက်တောင်ညာဏ်ရည်မမှီတဲ့ဖာသယ်မသားတွေကိုခေါ်မှန်းအခု့မှသိတယ်😂",
    "ငိုလေမင်းဖေရှေ့မှာငို gpထဲမှာငိုစမ်း ရှက်နေတာဖာသယ်မသားလေးက",
    "ခါကာဘိုရာဇီတောင်ကနေကော့သောင်းထိဖင်ပြေးကုန်းမအေလိုး",
    "အူကြောင်ကြားမလုပ်နဲ့တပည့်ပိတ်ကန်လိုက်လို့ရှေ့သွား ၅ ချောင်းလုံးအကပ်လိုက်ပြုတ်ထွက်ကုန်မယ်",
    "မင်းရဲ့ စကားလုံးတွေက အားသွင်းထားတာ ကြာလို့ ဖောင်းကြွနေတဲ့ ဘက်ထရီ တစ်လုံးလိုပဲ ဘယ်အချိန်မှာ ပေါက်ကွဲပြီး ကိုယ့်ကိုယ်ကိုယ် ပြန်သတ်မလဲ ဆိုတာကိုပဲ စောင့်ကြည့်နေရတဲ့ အပေါစား ပစ္စည်းတစ်ခုပဲ မင်းဟာ ကောင်းကင်ယံက လျှပ်စီးလက်တာကို မြင်ပြီး တုန်လှုပ်နေတဲ့ တွင်းအောင်း သတ္တဝါ တစ်ကောင်ရဲ့ ကြောက်စိတ်ကို ဆဲဆိုခြင်း ဆိုတဲ့ အသံနဲ့ ဖုံးကွယ်ဖို့ ကြိုးစားနေတာ အတိုင်းသား မြင်နေရတယ် မင်းရဲ့ နှလုံးသားက သံတိုသံစ စုပုံထားတဲ့ နေရာမှာ ကျန်ရစ်ခဲ့တဲ့ သံချေးတက် နာရီ တစ်လုံးလိုပဲ အချိန်နဲ့ အမျှ အသုံးမကျဖြစ်နေတာ အမှန်တရားပဲ",
    "ငါကရွှံ့ထဲမှာ နစ်နေရင်တောင် တန်ဖိုးမပျက်တဲ့ ပတ္တမြားခဲကြီးတစ်တုံးဆိုရင်မင်းကရွှေရောင်သုတ်ထားပေမဲ့ အနံ့အသက်မကောင်းတဲ့ ရွံနွံ့ တစ်ခုပဲငါ့ရဲ့ flow တေကို မင်းကအတုခိုးပြီး ဝင့်ကြွားချင်ပေမဲ့မင်းရဲ့ မူလဇာတိက ညံ့ဖျင်းလွန်း တော့ ဘယ်လိုမှ ပြင်လို့မရဘူး",
    "ကိတ်ခြောက်စားပြီးစိတ်ခြောက်ခြားနေရင်မင်းမိဘပေးဘု",
    "ခွေးဟောင်လို့လမင်းမနွမ်းခွေးသာပမ်း၏",
    "စောက်ရူးဟိတ်ကောင် ဘယ်ခြေကိုရွေ့ပြီးညာခြေနဲ့အားပြုကိုက်တာလား",
    "ငါလိုးမသားလေးမင်းရဲ့မသန်မစွမ်းဖစ်နေတဲ့ခန္ဓာကိုယ်ကို ငါရဲ့သံလက်သီးနဲ့နှစ်ချက်လောက်ဆင့်ထိုးပီးအရိုးတေကျိုးကျေသွားအောင်လုပ်ပေးရမလား",
    "ရိုက်ဖားကြီးငါရိုက်တာခံနေရတာလားရိုက်ဖားခိုင်းနွားငါခိုင်းရင်တန်းလုပ်အခုဆဲလေရိုက်ဖားလေးဘာစောက်သုံးကျ၁ပြီး၂လာတာပဲသိတဲ့ရွာသားလားဘောမ",
    "မင်းအမေစပတ်ကိုမော်တာတပ်လိုးပြီးစပိုက်တာမန်းလိုကြိုးဆွဲလိုးမှာငါလိုးမဖာသယ်မဖာအိုမဖာပျက်မခွေးမနွားမသား",
    "အူကြောင်ကြားမလုပ်နဲ့တပည့်ပိတ်ကန်လိုက်လို့ရှေ့သွား ၅ ချောင်းလောက်အထစ်လိုက်ပြုတ်ကျကုန်မယ်",
    "မင်းကအခြောက်လားစောက်စကားပြောတာအိညောင်အိညောင်နဲ့ငါလိုးမဂေး",
    "ဒီထပ်နည်းနည်းပိုအားထည့်ကိုက်နိုင်ရင် လည်ပတ်အသစ်ဝယ်ပေးမယ်",
    "မင်းမေစဖုတ်ကို ခရမ်းလွန်ရောင်ခြည်နဲ့ မီးကင်ပစ်မယ်ခွေးမသား",
    "အိမ်ကခွေးလီးနဲ့ပေးတီးလိုက်လို့မျက်ဖြူပါစိုက်နေမယ် မအေလိူး"
]

# ==========================================
# 🗄 DATABASE (TURSO)
# ==========================================
db_lock = threading.Lock()

def get_conn():
    return libsql.connect(database=TURSO_URL, auth_token=TURSO_TOKEN)

def init_db():
    with db_lock:
        conn = get_conn()
        conn.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)")
        conn.commit()
        conn.close()

init_db()

def get_kv(key):
    with db_lock:
        conn = get_conn()
        cur = conn.execute("SELECT value FROM kv WHERE key = ?", (key,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

def set_kv(key, value):
    with db_lock:
        conn = get_conn()
        conn.execute("INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()
        conn.close()

def delete_kv(key):
    with db_lock:
        conn = get_conn()
        conn.execute("DELETE FROM kv WHERE key = ?", (key,))
        conn.commit()
        conn.close()

def list_keys(prefix):
    with db_lock:
        conn = get_conn()
        cur = conn.execute("SELECT key FROM kv WHERE key LIKE ?", (prefix + '%',))
        rows = cur.fetchall()
        conn.close()
        return [row[0] for row in rows]

def get_all_savage_texts():
    custom = get_kv("custom_texts")
    custom_list = custom.split("\n") if custom else []
    custom_list = [t.strip() for t in custom_list if t.strip()]
    return custom_list + savage_texts

# ------------------------------------------
# 🔑 PERMISSION CHECK
# ------------------------------------------
def is_auth(user_id):
    if user_id == OWNER_ID:
        return True
    return get_kv(f"auth_{user_id}") == "true"

# ------------------------------------------
# 🎨 TEXT FORMATTING HELPER
# ------------------------------------------
def format_text_with_mention(chat_id, user_id, user_name, text):
    mention = f'<a href="tg://user?id={user_id}">{user_name}</a>'
    return text.replace("{username}", mention)

# ------------------------------------------
# 🖼️ MEDIA SENDER HELPER
# ------------------------------------------
def send_media(chat_id, media_type, file_id, caption=None, parse_mode=None):
    try:
        if media_type == 'photo':
            return bot.send_photo(chat_id, file_id, caption=caption, parse_mode=parse_mode)
        elif media_type == 'video':
            return bot.send_video(chat_id, file_id, caption=caption, parse_mode=parse_mode)
        elif media_type == 'sticker':
            return bot.send_sticker(chat_id, file_id)
        elif media_type == 'animation':
            return bot.send_animation(chat_id, file_id, caption=caption, parse_mode=parse_mode)
        elif media_type == 'document':
            return bot.send_document(chat_id, file_id, caption=caption, parse_mode=parse_mode)
        else:
            return None
    except Exception as e:
        logger.error(f"Media send error: {e}")
        return None

# ==========================================
# 🔥 SPAM LOOP (Speed-controlled)
# ==========================================
def spam_loop_worker(chat_id, target_id):
    try:
        member = bot.get_chat_member(chat_id, target_id)
        target_name = member.user.first_name
    except:
        target_name = str(target_id)

    all_texts = get_all_savage_texts()
    if not all_texts:
        all_texts = savage_texts

    while True:
        active_target = get_kv(f"spam_target_{chat_id}")
        if not active_target or active_target != str(target_id):
            break

        text = random.choice(all_texts)
        mention = f'<a href="tg://user?id={target_id}">{target_name}</a> {text}'

        try:
            bot.send_message(chat_id, mention, parse_mode="HTML")
        except Exception as e:
            err = str(e)
            if "429" in err:
                time.sleep(2)
            elif "403" in err or "400" in err:
                delete_kv(f"spam_target_{chat_id}")
                break

        # Speed check – speed "0" means no sleep (fastest)
        delay_str = get_kv("spam_speed") or "0"
        if delay_str == "0":
            continue
        try:
            delay = max(0.3, int(delay_str) / 1000.0)
        except:
            delay = 0.3
        time.sleep(delay)

# ==========================================
# 💬 COMMAND HANDLERS
# ==========================================
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    is_group = message.chat.type != "private"

    if not is_group:
        set_kv(f"user_{user_id}", "true")
    else:
        set_kv(f"group_{chat_id}", message.chat.title or "Group")

    if is_auth(user_id):
        welcome_txt = (
            "ကြိုဆိုပါတယ် bot ကိုအသုံး​ပြု့ရန် admin full permission ပေးထားပါ\n\n"
            "📌 <b>Commands များ</b>\n"
            "├ /lock [user_id] - စတင်ဆဲမယ်\n"
            "├ /speed - Spamမယ့် Speed ပြောင်းမယ်\n"
            "├ /info [user_id] - User အချက်အလက်ကြည့်မယ်\n"
            "├ /listtext - Spamစာသားစာရင်းကြည့်မယ်\n"
            "└ ရပ်တော့ - Spamတာရပ်မယ်\n\n"
            "👑 Owner - @Sir_Tokegiy"
        )
        bot.send_message(chat_id, welcome_txt, parse_mode="HTML")
    else:
        mention = f'<a href="tg://user?id={user_id}">{message.from_user.first_name}</a>'
        msg_text = (
            f"({user_id}) {mention}\n"
            f"မင်းမှာ Bot ကိုအသုံးပြု့ခွင့်မရှိဘူး✍\n"
            f"Bot ကိုအသုံးပြု့ချင်ရင် @Sir_Tokegiy ဆီမှာ ခွင့်တောင်းပါ"
        )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Ownerကိုဆက်သွယ်ရန်", url=f"tg://resolve?domain=Sir_Tokegiy"))
        bot.send_message(chat_id, msg_text, parse_mode="HTML", reply_markup=kb)

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_txt = (
        "🤖 <b>Bot လုပ်ဆောင်ချက်များ</b>\n\n"
        "• /start - Bot ကို စတင်အသက်သွင်းခြင်း\n"
        "• /lock [user_id] - အသုံးပြုသူအား ဆဲစာစတင်ပို့ရန်\n"
        "• /speed - ဆဲစာပို့နှုန်း ချိန်ညှိရန်\n"
        "• /info [user_id] - User အချက်အလက်ကြည့်ရန်\n"
        "• /listtext - ဆဲစာသားစာရင်း\n"
        "• ရပ်တော့ - ဆဲနေသည်ကိုရပ်ရန်\n\n"
        "📌 <b>Group စီမံချက်များ</b>\n"
        "• /setwelcome [စာသား] - Welcome Message (စာသား သို့မဟုတ် media ကို reply လုပ်)\n"
        "• /setgoodbye [စာသား] - Goodbye Message\n"
        "• /deleteword add/remove/list [စာလုံး]\n"
        "• /deletecmd on/off - '/' command ဖျက်ခြင်း\n\n"
        "⚠️ botကိုအသုံး​ ပြု့ခွင့်မရှိပါက လုပ်ဆောင်ချက်အများစုကို အသုံးမပြုနိုင်ပါ။"
    )
    bot.send_message(message.chat.id, help_txt, parse_mode="HTML")

# Owner commands
@bot.message_handler(func=lambda m: m.from_user.id == OWNER_ID, commands=['per', 'unper', 'add', 'knowall', 'addtext', 'listtext'])
def handle_owner_commands(message):
    chat_id = message.chat.id
    text = message.text

    if text.startswith("/per "):
        target = text.split(" ")[1]
        set_kv(f"auth_{target}", "true")
        bot.send_message(chat_id, f"✅ User {target} ကို အသုံးပြုခွင့် ပေးလိုက်ပါပြီ။")
    elif text.startswith("/unper "):
        target = text.split(" ")[1]
        delete_kv(f"auth_{target}")
        bot.send_message(chat_id, f"❌ User {target} ကို အသုံးပြုခွင့် ပိတ်လိုက်ပါပြီ။")
    elif text.startswith("/add "):
        bc_text = text.replace("/add ", "")
        bot.send_message(chat_id, "📢 ကြော်ငြာစာ ပို့ရန် စတင်နေပါပြီ...")
        users = list_keys("user_")
        groups = list_keys("group_")
        count = 0
        for u in users:
            try:
                bot.send_message(u.replace("user_", ""), bc_text)
                count += 1
            except:
                pass
        for g in groups:
            try:
                bot.send_message(g.replace("group_", ""), bc_text)
                count += 1
            except:
                pass
        bot.send_message(chat_id, f"✅ ကြော်ငြာကို စုစုပေါင်း နေရာ {count} ခုသို့ ပို့ပြီးပါပြီ။")
    elif text == "/knowall":
        users = list_keys("user_")
        auths = list_keys("auth_")
        groups = list_keys("group_")
        stats = (
            f"📊 <b>Bot စာရင်းဇယားများ</b>\n\n"
            f"👤 /start နှိပ်ထားသူ: {len(users)} ဦး\n"
            f"👑 ပါမစ်ရထားသူ: {len(auths)} ဦး\n"
            f"👥 ရောက်နေသော Group: {len(groups)} ခု"
        )
        bot.send_message(chat_id, stats, parse_mode="HTML")
    elif text.startswith("/addtext "):
        new_text = text.replace("/addtext ", "").strip()
        if new_text:
            existing = get_kv("custom_texts") or ""
            updated = existing + "\n" + new_text if existing else new_text
            set_kv("custom_texts", updated)
            bot.send_message(chat_id, f"✅ Spamစာသားအသစ် ထည့်ပြီးပါပြီ။\n\n📝 {new_text}")
        else:
            bot.send_message(chat_id, "⚠️ စာသားအလွတ် မထည့်ရပါ။ /addtext [စာသား] ပုံစံသုံးပါ။")
    elif text == "/listtext":
        all_texts = get_all_savage_texts()
        if not all_texts:
            bot.send_message(chat_id, "📝 Spamစာသားမရှိပါ။")
            return
        chunks = [all_texts[i:i+20] for i in range(0, len(all_texts), 20)]
        for idx, chunk in enumerate(chunks):
            result = f"📝 Spamစာသားများ (စာမျက်နှာ {idx+1}/{len(chunks)})\n\n"
            for i, t in enumerate(chunk, 1):
                result += f"{i}. {t[:50]}...\n" if len(t) > 50 else f"{i}. {t}\n"
            bot.send_message(chat_id, result)

# Authorized user commands
@bot.message_handler(func=lambda m: is_auth(m.from_user.id), commands=[
    'lock', 'speed', 'info', 'setwelcome', 'setgoodbye', 'deleteword', 'deletecmd'
])
def handle_auth_commands(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    parts = text.split(" ", 2)
    cmd = parts[0]

    if cmd == "/lock" and len(parts) > 1:
        try:
            target_id = int(parts[1])
            if target_id == OWNER_ID:
                bot.send_message(chat_id, "ငါ့ရဲ့ဖန်ဆင်းရှင်ကို Spamလုပ် ဖို့မင်းမှာအဲ့လောက်သတ္တိတွေရှိနေသလားခွေးမသား")
            else:
                if get_kv(f"spam_target_{chat_id}"):
                    bot.send_message(chat_id, "⚠️ လက်ရှိ Spamနေတဲ့ Target ရှိနေပါတယ်။ 'ရပ်တော့' အရင်လုပ်ပါ။")
                    return
                set_kv(f"spam_target_{chat_id}", target_id)
                set_kv(f"spam_owner_{chat_id}", user_id)
                bot.send_message(chat_id, f"🔥 Target {target_id} ကို စတင် ဖင်လိုးပါပြီ...")
                t = threading.Thread(target=spam_loop_worker, args=(chat_id, target_id))
                t.daemon = True
                t.start()
        except:
            bot.send_message(chat_id, "⚠️ Invalid User ID")

    elif cmd == "/speed":
        kb = InlineKeyboardMarkup(row_width=3)
        kb.add(
            InlineKeyboardButton("0 (အမြန်ဆုံး)", callback_data="spd_0"),
            InlineKeyboardButton("1", callback_data="spd_300"),
            InlineKeyboardButton("2", callback_data="spd_500"),
            InlineKeyboardButton("3", callback_data="spd_1000"),
            InlineKeyboardButton("4", callback_data="spd_2000"),
            InlineKeyboardButton("5", callback_data="spd_3000")
        )
        bot.send_message(chat_id, "⚡ Spam အရှိန် ရွေးချယ်ပါ:", reply_markup=kb)

    elif cmd == "/info" and len(parts) > 1:
        try:
            target_id = int(parts[1])
            try:
                chat = bot.get_chat(target_id)
                info_text = (
                    f"👤 <b>User Information</b>\n\n"
                    f"🆔 <b>User ID:</b> {chat.id}\n"
                    f"📛 <b>First Name:</b> {chat.first_name or 'N/A'}\n"
                    f"🏠 <b>Last Name:</b> {chat.last_name or 'N/A'}\n"
                    f"🔖 <b>Username:</b> @{chat.username if chat.username else 'N/A'}\n"
                )
                bot.send_message(chat_id, info_text, parse_mode="HTML")
            except:
                info_text = (
                    f"👤 <b>User Information</b>\n\n"
                    f"🆔 <b>User ID:</b> {target_id}\n"
                    f"📌 <b>Status:</b> Bot နဲ့ စကားမပြောရသေးပါ\n"
                )
                bot.send_message(chat_id, info_text, parse_mode="HTML")
        except:
            bot.send_message(chat_id, "⚠️ /info [user_id] ပုံစံသုံးပါ။")

    # --- Welcome / Goodbye (with media support) ---
    elif cmd in ["/setwelcome", "/setgoodbye"]:
        prefix = "welcome" if cmd == "/setwelcome" else "goodbye"
        if message.reply_to_message and message.reply_to_message.content_type in ['photo', 'video', 'sticker', 'animation', 'document']:
            media = message.reply_to_message
            if media.content_type == 'photo':
                file_id = media.photo[-1].file_id
            elif media.content_type == 'video':
                file_id = media.video.file_id
            elif media.content_type == 'sticker':
                file_id = media.sticker.file_id
            elif media.content_type == 'animation':
                file_id = media.animation.file_id
            elif media.content_type == 'document':
                file_id = media.document.file_id
            else:
                file_id = None

            if file_id:
                set_kv(f"{prefix}_media_{chat_id}", f"{media.content_type}|{file_id}")
                cap = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else ""
                if cap:
                    set_kv(f"{prefix}_caption_{chat_id}", cap)
                else:
                    delete_kv(f"{prefix}_caption_{chat_id}")
                bot.send_message(chat_id, f"✅ {prefix} media သတ်မှတ်ပြီး။")
            else:
                bot.send_message(chat_id, "⚠️ Media မထောက်ပံ့ပါ။")
        else:
            welcome_text = text.split(" ", 1)[1] if len(text.split(" ", 1)) > 1 else ""
            if welcome_text:
                set_kv(f"{prefix}_{chat_id}", welcome_text)
                delete_kv(f"{prefix}_media_{chat_id}")
                bot.send_message(chat_id, f"✅ {prefix} text သတ်မှတ်ပြီး။")
            else:
                bot.send_message(chat_id, "⚠️ စာသား သို့မဟုတ် media ကို reply လုပ်ပြီး ပေးပါ။")

    # --- Delete Word Management ---
    elif cmd == "/deleteword":
        if len(parts) < 2:
            bot.send_message(chat_id, "⚠️ /deleteword add/remove/list [စာလုံး]")
            return
        action = parts[1].lower()
        word = parts[2] if len(parts) > 2 else ""
        raw = get_kv(f"forbidden_{chat_id}") or ""
        words = [w.strip() for w in raw.split("\n") if w.strip()]
        if action == "add" and word:
            if word in words:
                bot.send_message(chat_id, "⚠️ ထိုစာလုံးရှိပြီးသားဖြစ်သည်။")
            else:
                words.append(word)
                set_kv(f"forbidden_{chat_id}", "\n".join(words))
                bot.send_message(chat_id, f"✅ '{word}' ကို ဖျက်ရန်စာရင်းထဲထည့်ပြီး။")
        elif action == "remove" and word:
            if word in words:
                words.remove(word)
                set_kv(f"forbidden_{chat_id}", "\n".join(words))
                bot.send_message(chat_id, f"✅ '{word}' ကို စာရင်းမှဖယ်ရှားပြီး။")
            else:
                bot.send_message(chat_id, "⚠️ ထိုစာလုံးမရှိပါ။")
        elif action == "list":
            if words:
                bot.send_message(chat_id, "📋 ဖျက်ရန်စာလုံးများ:\n" + "\n".join(words))
            else:
                bot.send_message(chat_id, "📋 ဖျက်ရန်စာလုံးမရှိသေးပါ။")
        else:
            bot.send_message(chat_id, "⚠️ အသုံးပြုပုံ: /deleteword add/remove [စာလုံး]")

    # --- Toggle Delete Commands ---
    elif cmd == "/deletecmd":
        if len(parts) < 2:
            bot.send_message(chat_id, "⚠️ /deletecmd on သို့မဟုတ် /deletecmd off")
            return
        action = parts[1].lower()
        if action == "on":
            set_kv(f"deletecmd_{chat_id}", "true")
            bot.send_message(chat_id, "✅ '/' command များကို အလိုအလျောက်ဖျက်ရန် ဖွင့်ထားပါပြီ။")
        elif action == "off":
            set_kv(f"deletecmd_{chat_id}", "false")
            bot.send_message(chat_id, "❌ '/' command ဖျက်ခြင်းကို ပိတ်ထားပါပြီ။")
        else:
            bot.send_message(chat_id, "⚠️ on သို့မဟုတ် off သာထည့်ပါ။")

# --- TEXT MESSAGES (ရပ်တော့) ---
@bot.message_handler(func=lambda m: m.text == "ရပ်တော့")
def handle_stop(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_auth(user_id):
        bot.send_message(chat_id, "⚠️မင်းကဘာကောင်မို့လို့ငါ့ကိုလာရပ်ခိုင်းနေတာလည်း ငါ့ကိုခိုင်းထားတာမင်းမဟုတ်ဘူး ငါ့ကိုမင်းစောက်ဆင့်နဲ့လာရပ်လို့မရဘူးခွေးမသား")
        return

    active_target = get_kv(f"spam_target_{chat_id}")
    if active_target:
        spam_owner = get_kv(f"spam_owner_{chat_id}")
        if str(user_id) == str(spam_owner) or user_id == OWNER_ID:
            delete_kv(f"spam_target_{chat_id}")
            bot.send_message(chat_id, "✅ဆရာကြီး ပြောတဲ့အတိုင်းရပ်လိုက်ပါပီ ဟိုခွေးသားတွေဆရာကြီးကို​ရိုသေစမ်းပါ")
        else:
            bot.send_message(chat_id, "⚠️ မင်း Lock လုပ်ထားတာ မဟုတ်တဲ့အတွက် ရပ်လို့မရပါဘူး။")
    else:
        bot.send_message(chat_id, "⚠️ လက်ရှိ Spam နေတဲ့ Target မရှိပါဘူး။")

# --- GROUP JOIN / LEAVE (with media support) ---
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_members(message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            continue
        media_data = get_kv(f"welcome_media_{chat_id}")
        if media_data:
            try:
                mtype, file_id = media_data.split("|", 1)
                cap = get_kv(f"welcome_caption_{chat_id}")
                if cap:
                    cap = format_text_with_mention(chat_id, member.id, member.first_name, cap)
                send_media(chat_id, mtype, file_id, caption=cap, parse_mode="HTML" if cap else None)
            except Exception as e:
                logger.error(f"Welcome media error: {e}")
        else:
            welcome_text = get_kv(f"welcome_{chat_id}")
            if welcome_text:
                msg = format_text_with_mention(chat_id, member.id, member.first_name, welcome_text)
                try:
                    bot.send_message(chat_id, msg, parse_mode="HTML")
                except:
                    pass

    adder = message.from_user.first_name or str(message.from_user.id)
    title = message.chat.title
    link = f"@{message.chat.username}" if message.chat.username else f"ID: {chat_id}"
    alert = (
        f"📣 <b>Bot Group အသစ်ရောက်ပါပြီ</b>\n\n"
        f"🔹 <b>Group:</b> {title}\n"
        f"🔗 <b>Link/ID:</b> {link}\n"
        f"👤 <b>ထည့်သူ:</b> <a href='tg://user?id={message.from_user.id}'>{adder}</a>"
    )
    bot.send_message(OWNER_ID, alert, parse_mode="HTML")

@bot.message_handler(content_types=['left_chat_member'])
def handle_left_chat_member(message):
    chat_id = message.chat.id
    member = message.left_chat_member
    if member.id == bot.get_me().id:
        return
    media_data = get_kv(f"goodbye_media_{chat_id}")
    if media_data:
        try:
            mtype, file_id = media_data.split("|", 1)
            cap = get_kv(f"goodbye_caption_{chat_id}")
            if cap:
                cap = format_text_with_mention(chat_id, member.id, member.first_name, cap)
            send_media(chat_id, mtype, file_id, caption=cap, parse_mode="HTML" if cap else None)
        except Exception as e:
            logger.error(f"Goodbye media error: {e}")
    else:
        goodbye_text = get_kv(f"goodbye_{chat_id}")
        if goodbye_text:
            msg = format_text_with_mention(chat_id, member.id, member.first_name, goodbye_text)
            try:
                bot.send_message(chat_id, msg, parse_mode="HTML")
            except:
                pass

# ==========================================
# 🔗 LINK PROTECTION + WORD FILTER + COMMAND DELETE (Unified)
# ==========================================
LINK_PATTERN = re.compile(r'(https?://[^\s]+|t\.me/[^\s]+|telegram\.me/[^\s]+|www\.[^\s]+)')

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_message_filters(message):
    if message.chat.type == "private":
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        is_admin = chat_member.status in ['administrator', 'creator']
    except:
        is_admin = False

    if user_id == bot.get_me().id:
        return

    text = message.text or message.caption or ""

    # 1. Link Protection
    has_link = bool(LINK_PATTERN.search(text))
    if not is_admin and has_link:
        try:
            bot.delete_message(chat_id, message.message_id)
            mention = f'<a href="tg://user?id={user_id}">{message.from_user.first_name}</a>'
            group_name = message.chat.title or "ဒီ Group"
            warning = bot.send_message(
                chat_id,
                f"🚫{mention}ရေ {group_name}ထဲမှာ link လာမချနဲ့။\n"
                f"link ချချင်ရင် အုံနာနဲ့ Admin တွေဆီ ခွင့်တောင်းပါ။✅",
                parse_mode="HTML"
            )
            
            return
        except Exception as e:
            logger.error(f"Link protection error: {e}")

    # 2. Forbidden Word Filter
    if not is_admin:
        raw_words = get_kv(f"forbidden_{chat_id}") or ""
        if raw_words:
            forbidden_list = [w.strip() for w in raw_words.split("\n") if w.strip()]
            for word in forbidden_list:
                if word.lower() in text.lower():
                    try:
                        bot.delete_message(chat_id, message.message_id)
                    except:
                        pass
                    break

    # 3. Delete Commands (starting with '/')
    delete_cmd_enabled = get_kv(f"deletecmd_{chat_id}") == "true"
    if not is_admin and delete_cmd_enabled and text.startswith("/"):
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass

# ==========================================
# 🎛 BUTTON CALLBACK HANDLER
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data.startswith("spd_"))
def handle_speed_callback(call):
    speed = call.data.replace("spd_", "")
    set_kv("spam_speed", speed)
    
    speed_names = {
        "0": "အမြန်ဆုံး (No Limit)",
        "300": "၁",
        "500": "၂",
        "1000": "၃",
        "2000": "၄",
        "3000": "၅"
    }
    
    bot.answer_callback_query(call.id, text=f"Speed ပြောင်းပြီး")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Speed ကို <b>{speed_names.get(speed, speed)}</b> သတ်မှတ်ပြီးပါပြီ။",
        parse_mode="HTML"
    )

# ==========================================
# 🚀 START BOT (POLLING)
# ==========================================
logger.info("bot run နေပါပီ telegram တွင်သွားစမ်းပါ✅...")
try:
    bot.delete_webhook()
except:
    pass


bot.infinity_polling(timeout=10, long_polling_timeout=5)
