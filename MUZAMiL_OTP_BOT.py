#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MUZAMiL OTP BOT — NumberPanel + Admin Panel + Premium Emojis
"""
import os, re, json, time, sqlite3, asyncio, hashlib, html as html_mod
from datetime import datetime
from io import BytesIO
import requests
import phonenumbers
from phonenumbers import geocoder, region_code_for_number

from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, BotCommand
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler, ChatMemberHandler
)
try:
    from telegram import CopyTextButton
except ImportError:
    CopyTextButton = None


# ==================== PREMIUM EMOJIS ====================
APP_EMOJI_ID = {
    "whatsapp":  "5334998226636390258",
    "telegram":  "5330237710655306682",
    "instagram": "5319160079465857105",
    "facebook":  "5323261730283863478",
    "google":    "5359758030198031389",
    "gmail":     "5359758030198031389",
    "twitter":   "5330337435500951363",
    "tiktok":    "5327982530702359565",
    "snapchat":  "5330248916224983855",
    "binance":   "5359437015752401733",
    "bybit":     "5359437015752401733",
    "discord":   "5373026167722876724",
    "netflix":   "5373026167722876724",
    "amazon":    "5373026167722876724",
    "paypal":    "5373026167722876724",
    "spotify":   "5373026167722876724",
    "DEFAULT":   "5373026167722876724",
}

COUNTRY_EMOJI_ID = {
    "UA": "5222250679371839695", "UA_2": "5280587278828193324",
    "US": "5224321781321442532", "PL": "5224670399521892983",
    "KZ": "5222276376161171525", "AZ": "5224426544163728284",
    "EU": "5222108911091331711", "UN": "5451772687993031127",
    "AM": "5224369957969603463", "RU": "5280582975270963511",
    "CN": "5224435456220868088", "UZ": "5222404546575219535",
    "DE": "5222165617544542414", "JP": "5222390089715299207",
    "TR": "5224601903383457698", "BY": "5280820319458707404",
    "BY_2": "5222398507851199882", "GB": "5224518800061245598",
    "IN": "5222300011366200403", "BR": "5224688610183228070",
    "ZM": "5224646626877911277", "YE": "5222300655611294950",
    "VI": "5224395882392201810", "VN": "5222359651282071925",
    "VA": "5222420266155520507", "VU": "5222126748090512778",
    "UY": "5222466849370813232", "AE": "5224565851427976312",
    "US_2": "5222253007244113340", "UG": "5222464040462200940",
    "TM": "5224256935905208951", "TN": "5221991375016310330",
    "TT": "5224391883777651050", "TG": "5222408051268532030",
    "TH": "5224638530864556281", "TZ": "5224397364155923150",
    "TJ": "5222217865821696536", "CH": "5224707263226194753",
    "SE": "5222201098269373561", "SZ": "5224269666188274723",
    "SR": "5224567367551428669", "SD": "5224372990216514135",
    "ES": "5222024776976970940", "LK": "5224277294050192388",
    "SS": "5224618146949773268", "KR": "5222345550904439270",
    "ZA": "5224696216570309138", "SO": "5222370504664428325",
    "SI": "5224660718665607511", "SK": "5222401879400528047",
    "SG": "5224194023224257181", "SL": "5224420995065983217",
    "SC": "5224467496676896871", "RS": "5222145396838512729",
    "SN": "5224358988623130949", "SA": "5224698145010624573",
    "ST": "5221953304426198315", "WS": "5224660353593387686",
    "VC": "5224541228380467535", "LC": "5222000927023577045",
    "PS": "5222041677673282461", "PS_2": "5222370620628546719",
    "RW": "5222449197055227754", "RO": "5222273794885826118",
    "QA": "5222225596762830469", "PR": "5224220115150582423",
    "PT": "5224404094369672274", "PH": "5222065042295376892",
    "PE": "5224482026551258766", "PY": "5222152565138929235",
    "PG": "5224500164198149905", "PA": "5222111719999945107",
    "PK": "5224637061985742245", "OM": "5222396686785066306",
    "NO": "5224465228934163949", "NG": "5224723614166691638",
    "NE": "5222099049846420864", "NZ": "5224573595254009705",
    "NL": "5224516489368841614", "NP": "5222444378101925267",
    "NA": "5224690826386351746", "MZ": "5222470388423864826",
    "MA": "5224530035695693965", "ME": "5224463399278096980",
    "MN": "5224192257992701543", "MC": "5221937224068640464",
    "MD": "5224216473018314447", "FM": "5222280486444873367",
    "MX": "5221971386238514431", "MU": "5224238347286752315",
    "MH": "5224538449536624503", "MY": "5224312886444174057",
    "KE": "5222089648163009103", "KE_2": "5222279743415531561",
    "MG": "5222042605386217334", "MK": "5222470435668505656",
    "LU": "5224499567197700690", "LT": "5224245902134226386",
    "LY": "5222194286451242896", "LR": "5221998371518034740",
    "LS": "5224245850594619415", "LB": "5222244425899455269",
    "LV": "5224401229626484931", "LA": "5224200843632324642",
    "KG": "5224388147156102493", "KW": "5221949726718442491",
    "XK": "5222197129719592160", "KI": "5224652244695134610",
    "JO": "5222292177345853436", "JM": "5222007034467074185",
    "IE": "5224257017509588818", "IE_2": "5222233374948602940",
    "IT": "5222460101977190141", "IL": "5224720599099648709",
    "IQ": "5221980268230882832", "IR": "5224374154152653367",
    "ID": "5224405893960969756", "IS": "5222063229819172521",
    "HU": "5224691998912427164", "HN": "5222229234600130045",
    "HN_2": "5222434624231191289", "HT": "5224683146984831315",
    "GY": "5224570532942329532", "GW": "5224705704153066489",
    "GN": "5222337588035073000", "GT": "5222128302868672826",
    "GD": "5222234560359577687", "GR": "5222463490706389920",
    "GH": "5224511339703056124", "GE": "5222152195771742239",
    "GM": "5221949872747330159", "GA": "5224669733801963467",
    "FR": "5222029789203804982", "FI": "5224282903277482188",
    "FJ": "5221962676044838178", "ET": "5224467805914542024",
    "EE": "5222195463272281351", "GQ": "5222172811614762423",
    "SV": "5224337131534559907", "EG": "5222161185138292290",
    "EC": "5224191188545840926", "TL": "5224515905253291409",
    "DO": "5224286412265763450", "DM": "5222337489250824921",
    "DJ": "5224203012590810589", "DK": "5222297215342490217",
    "CY": "5222431454545327055", "HR": "5221967765581085099",
    "CR": "5222453801260168022", "CG": "5222104268231684600",
    "CD": "5224398158724871677", "KM": "5222398735484466247",
    "CO": "5224455152940886669", "CL": "5222350726340032308",
    "CZ": "5222073533445714675", "TD": "5222060468155204001",
    "CF": "5222073662294733523", "CV": "5222347737042792258",
    "CA": "5222001124592071204", "CM": "5222270788408717651",
    "KH": "5224189882875785448", "BI": "5224490444687158452",
    "BF": "5222356541725749790", "BG": "5222092074819530668",
    "BN": "5224435958732042406", "BW": "5224288456670196085",
    "BA": "5224496092569155254", "BO": "5224675484763170798",
    "BT": "5224541065171710147", "BJ": "5222024115552009151",
    "BZ": "5224316292353241916", "BE": "5224513182244024630",
    "BB": "5222156533688712094", "BD": "5224407289825340729",
    "BH": "5224492892818518587", "BS": "5224504167107668172",
    "AT": "5224520754271366661", "AU": "5224659803837574114",
    "AR": "5221980461504411710", "AG": "5224544866217765554",
    "AO": "5224379767674907895", "AD": "5221987861733061751",
    "DZ": "5224260376174015500", "AL": "5224312057515486246",
    "AF": "5222096009009575868", "ZW": "5222060442385397848",
    "VE": "5294476442854247878", "FO": "5280985770188885026",
    "MQ": "5281027792148909351",
    "DEFAULT": "5222250679371839695",
}

# ✅ FULL PREMIUM UI EMOJI MAP (aapke diye IDs)
UI_EMOJI = {
    "🚀": "5316571734604790521",
    "😈": "6336780965968353744",
    "😌": "6325594444473045337",
    "✅": "6147565374289220368",
    "👑": "6235252066554484059",
    "⚠️": "6242010768825391425",
    "❤️‍🔥": "6235582469798630291",
    "🔔": "6314420734865185420",
    "💯": "6312139458690948101",
    "🗑": "6314398126157340467",
    "🚫": "6312235051778056164",
    "📊": "6129801569941592173",
    "🚨": "6240152061598504832",
    "👍": "6303012090546232688",
    "🏴‍☠️": "6188243318787284938",
    "🥂": "5260567255145539253",
    "🍁": "6060130594740768832"
}


def pe(emoji_id, fallback):
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'


def uie(emoji, fallback=None):
    eid = UI_EMOJI.get(emoji)
    return pe(eid, fallback or emoji) if eid else emoji


def service_emoji_tag(service):
    k = re.sub(r"[^a-z0-9]", "", str(service or "").lower())
    if not k:
        return pe(APP_EMOJI_ID["DEFAULT"], "📱")
    if k in APP_EMOJI_ID and k != "DEFAULT":
        return pe(APP_EMOJI_ID[k], "📱")
    for name, eid in APP_EMOJI_ID.items():
        if name == "DEFAULT": continue
        if name in k or (len(k) >= 3 and k in name):
            return pe(eid, "📱")
    return pe(APP_EMOJI_ID["DEFAULT"], "📱")


def country_emoji_tag(iso):
    iso = (iso or "UN").upper()
    eid = COUNTRY_EMOJI_ID.get(iso) or COUNTRY_EMOJI_ID.get("DEFAULT")
    flag = flag_emoji(iso)
    return pe(eid, flag) if eid else flag


def premiumize(text):
    if not text or "<tg-emoji" in text:
        return text
    for emoji, eid in UI_EMOJI.items():
        if emoji in text:
            text = text.replace(emoji, f'<tg-emoji emoji-id="{eid}">{emoji}</tg-emoji>')
    return text


def strip_premium(text):
    return re.sub(r'<tg-emoji[^>]*>(.*?)</tg-emoji>', r'\1', text or '')


def B(text, cb=None, url=None, style=None, copy=None, icon=None):
    """Premium-only: icon_custom_emoji_id + clean text (no rough emoji in label)."""
    kwargs = {}
    extra = {}
    if cb:
        kwargs["callback_data"] = cb
    if url:
        kwargs["url"] = url
    if icon is None and text:
        for em in sorted(UI_EMOJI.keys(), key=len, reverse=True):
            if text.startswith(em):
                icon = em
                text = text[len(em):].lstrip(" -–—|")
                break
    if icon:
        eid = UI_EMOJI.get(icon) if not str(icon).isdigit() else str(icon)
        if eid:
            kwargs["icon_custom_emoji_id"] = str(eid)
    if copy is not None:
        extra["copy_text"] = {"text": str(copy)}
    if style:
        extra["style"] = style
    try:
        if copy is not None and CopyTextButton is not None:
            kwargs["copy_text"] = CopyTextButton(text=str(copy))
            api = {k: v for k, v in extra.items() if k != "copy_text"}
            if api:
                return InlineKeyboardButton(text, api_kwargs=api, **kwargs)
            return InlineKeyboardButton(text, **kwargs)
    except Exception:
        pass
    if extra:
        try:
            return InlineKeyboardButton(text, api_kwargs=extra, **kwargs)
        except TypeError:
            pass
    try:
        return InlineKeyboardButton(text, **kwargs)
    except TypeError:
        kwargs.pop("icon_custom_emoji_id", None)
        return InlineKeyboardButton(text, **kwargs)



# ==================== CONFIG ====================
BOT_TOKEN = "9264639954:AAE78shP5futRLgfpSvQzJU0wKM5HLYI_XQ"
OWNER_ID = 8962273150
OTP_GROUP_ID = -1003914635353
API_URL = "https://numberpanel.tech/api/otp?count=200"
POLL_INTERVAL = 10
DB_PATH = "botfile.db"
NUMBERS_CHANNEL = "https://t.me/MuzamilxBotz"
OTP_GROUP_LINK = "https://t.me/muzamilxotps"
DEFAULT_NUMBERS_PER_USER = 3

(AWAIT_TXT, AWAIT_SERVICE, AWAIT_FORCE_ID, AWAIT_BAN, AWAIT_UNBAN,
 AWAIT_BROADCAST, AWAIT_WELCOME, AWAIT_OTP_GROUP, AWAIT_BTN_NUMBERS,
 AWAIT_BTN_OTP, AWAIT_NUM_LIMIT) = range(11)


# ==================== DB ====================
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    c = db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT,
        is_banned INTEGER DEFAULT 0, join_date TEXT);
    CREATE TABLE IF NOT EXISTS numbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT UNIQUE, country TEXT,
        iso TEXT, service TEXT, added_by INTEGER, added_at TEXT, active INTEGER DEFAULT 1);
    CREATE TABLE IF NOT EXISTS force_joins (
        id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id TEXT UNIQUE,
        title TEXT, link TEXT, kind TEXT DEFAULT 'channel');
    CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE IF NOT EXISTS seen_otps (uid TEXT PRIMARY KEY);
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, number TEXT,
        service TEXT, assigned_at TEXT);
    CREATE TABLE IF NOT EXISTS otp_stats (
        service TEXT, iso TEXT, country TEXT, cnt INTEGER DEFAULT 0,
        PRIMARY KEY (service, iso));
    """)
    defaults = {
        "welcome": "🌐 <b>Welcome to MUZAMiL OTP BOT</b>\n\nGet temporary numbers & receive OTPs instantly.",
        "numbers_channel": NUMBERS_CHANNEL,
        "otp_group_link": OTP_GROUP_LINK,
        "otp_group_id": "-1003791317242",
        "numbers_per_show": str(DEFAULT_NUMBERS_PER_USER),
        "otp_btn_name": "🔔 OTP GROUP",
        "numbers_btn_name": "🚀 CHANNEL",
        "methods_link": "https://youtube.com",
        "methods_btn_name": "🥂 METHODS",
    }
    for k, v in defaults.items():
        c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
    c.commit()
    c.close()


def get_setting(key, default=""):
    c = db()
    row = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    c.close()
    return row["value"] if row else default


def set_setting(key, value):
    c = db()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    c.commit()
    c.close()


def is_owner(uid): return uid == OWNER_ID


def is_banned(uid):
    c = db()
    row = c.execute("SELECT is_banned FROM users WHERE user_id=?", (uid,)).fetchone()
    c.close()
    return row and row["is_banned"] == 1


def ensure_user(u):
    c = db()
    c.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name, join_date) VALUES (?,?,?,?)",
        (u.id, u.username or "", u.first_name or "", datetime.utcnow().isoformat()))
    c.commit()
    c.close()


# ==================== HELPERS ====================
def detect_country(number: str):
    n = number if number.startswith("+") else "+" + number
    try:
        parsed = phonenumbers.parse(n)
        region = region_code_for_number(parsed) or "UN"
        name = geocoder.description_for_number(parsed, "en") or region
        return name, region
    except Exception:
        return "Unknown", "UN"


def country_icon_id(iso: str) -> str:
    iso = (iso or "UN").upper()
    return COUNTRY_EMOJI_ID.get(iso) or COUNTRY_EMOJI_ID.get("DEFAULT") or "5222250679371839695"

def service_icon_id(service: str) -> str:
    k = re.sub(r"[^a-z0-9]", "", str(service or "").lower())
    # exact
    if k in APP_EMOJI_ID and k != "DEFAULT":
        return str(APP_EMOJI_ID[k])
    # aliases
    aliases = {
        "wa": "whatsapp", "whatsapp": "whatsapp", "wapp": "whatsapp",
        "tg": "telegram", "tele": "telegram", "telegram": "telegram",
        "ig": "instagram", "insta": "instagram", "instagram": "instagram",
        "fb": "facebook", "facebook": "facebook",
        "x": "twitter", "twitter": "twitter",
        "tt": "tiktok", "tiktok": "tiktok",
        "sc": "snapchat", "snap": "snapchat", "snapchat": "snapchat",
        "google": "google", "gmail": "gmail", "mail": "gmail",
        "binance": "binance", "bybit": "bybit",
        "discord": "discord", "netflix": "netflix",
        "amazon": "amazon", "paypal": "paypal", "spotify": "spotify",
    }
    if k in aliases:
        return str(APP_EMOJI_ID.get(aliases[k], APP_EMOJI_ID["DEFAULT"]))
    for name, eid in APP_EMOJI_ID.items():
        if name == "DEFAULT":
            continue
        if name in k or (len(k) >= 3 and k in name):
            return str(eid)
    return str(APP_EMOJI_ID.get("DEFAULT") or "5373026167722876724")

def flag_emoji(iso: str) -> str:
    iso = (iso or "UN").upper()
    if len(iso) != 2 or not iso.isalpha():
        return "🏳️"
    return chr(ord(iso[0]) + 127397) + chr(ord(iso[1]) + 127397)


def mask_number(num: str) -> str:
    digits = re.sub(r"\D", "", str(num))
    if len(digits) <= 6:
        return "+" + digits
    if len(digits) >= 10:
        return f"+{digits[:2]}***{digits[-5:]}"
    return f"+{digits[:2]}***{digits[-4:]}"


def extract_otp(msg: str):
    m = re.search(r"\d{3}[-\s]?\d{3,4}|\d{4,8}", msg or "")
    return m.group(0) if m else None


# ==================== FORCE JOIN ====================
async def missing_force_joins(bot, user_id):
    """Return list of force-join channels the user has NOT joined."""
    c = db()
    rows = c.execute("SELECT chat_id, title, link FROM force_joins").fetchall()
    c.close()
    missing = []
    for r in rows:
        try:
            m = await bot.get_chat_member(int(r["chat_id"]), user_id)
            if m.status in ("left", "kicked"):
                missing.append(r)
        except Exception:
            # if cannot check, treat as missing so user must join
            missing.append(r)
    return missing


async def force_join_ok(bot, user_id) -> bool:
    return len(await missing_force_joins(bot, user_id)) == 0


async def force_join_keyboard(bot, user_id=None):
    """Show ONLY channels user has not joined yet."""
    if user_id is not None:
        rows = await missing_force_joins(bot, user_id)
    else:
        c = db()
        rows = c.execute("SELECT chat_id, title, link FROM force_joins").fetchall()
        c.close()
    kb = []
    for r in rows:
        link = r["link"] or ""
        if not link and r["chat_id"]:
            link = f"https://t.me/c/{str(r['chat_id']).replace('-100','')}"
        title = r["title"] or r["chat_id"]
        if link:
            kb.append([B(f"🚀 Join {title}", url=link, style="primary")])
    kb.append([B("✅ I Joined — Check", "fj_check", style="success")])
    return InlineKeyboardMarkup(kb)


async def log_event(bot, text: str):
    """Send activity log to owner logs channel if set."""
    gid = get_setting("logs_channel_id", "").strip()
    if not gid:
        return
    try:
        await bot.send_message(int(gid), text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        print("log_event fail", e)


# ==================== OTP TEMPLATE (ROUGH EMOJIS REMOVED) ====================
# OLD: 💬 → ❤️‍🔥   |   🌐 → 🥂   |   🔐 → 🔔   (all premium-available)
DEFAULT_OTP_TEMPLATE = (
    "{service}\n"
    "{flag} {iso} ⬥ <code>{number}</code>\n"
    "🥂 {language}\n"
    "🔔 OTP ⬥ <code>{otp}</code>\n\n"
    "❤️‍🔥 FULL MESSAGE\n"
    "<blockquote>{message}</blockquote>"
)
STYLE_PRESETS = ['{service}\n{flag} {iso} ⬥ <code>{number}</code>\n🥂 {language}\n🔔 OTP ⬥ <code>{otp}</code>\n\n❤️\u200d🔥 FULL MESSAGE\n<blockquote>{message}</blockquote>', '━━━━ OTP ━━━━\n{service}\n{flag} {iso} | <code>{number}</code>\nLanguage: {language}\nCode: <code>{otp}</code>\n━━━━━━━━━━\n<blockquote>{message}</blockquote>', '• Service: {service}\n• Country: {flag} {iso}\n• Number: <code>{number}</code>\n• Lang: {language}\n• OTP: <code>{otp}</code>\n\n<blockquote>{message}</blockquote>', '{flag} <b>{country}</b> | {service}\n<code>{number}</code>\nOTP → <code>{otp}</code> ({language})\n\n<blockquote>{message}</blockquote>', '🔔 <b>NEW OTP</b>\n{service_emoji}{service} · {flag}{iso}\n📱 <code>{number}</code>\n🔑 <code>{otp}</code>\n\n<blockquote>{message}</blockquote>', '╔══════════════╗\n║ {service}\n║ {flag} {iso} · <code>{number}</code>\n║ OTP: <code>{otp}</code>\n╚══════════════╝\n<blockquote>{message}</blockquote>', '✨ {service}\n{flag} {country} ({iso})\nNumber: <code>{number}</code>\nOTP: <b><code>{otp}</code></b>\n\n<blockquote>{message}</blockquote>', '{flag} {iso} — {service}\n<code>{number}</code>\n▶ <code>{otp}</code>\n\n<blockquote>{message}</blockquote>', '📌 {service} OTP\n{flag} {iso} · <code>{number}</code>\nCode: <code>{otp}</code> · {language}\n\n<blockquote>{message}</blockquote>', '{service} | {flag}{iso}\n<code>{number}</code>\n🔐 <code>{otp}</code>\n\n<blockquote>{message}</blockquote>']

TEMPLATE_HELP = (
    "<code>{service}</code> — service name (with premium emoji)\n"
    "<code>{flag}</code> — premium country flag\n"
    "<code>{iso}</code> — country code\n"
    "<code>{country}</code> — country name\n"
    "<code>{number}</code> — masked number\n"
    "<code>{language}</code> — language\n"
    "<code>{otp}</code> — OTP code\n"
    "<code>{message}</code> — full SMS\n"
    "<code>{time}</code> — time (UTC)"
)


def render_otp_text(service, num, msg, lang="English", otp_override=None):
    country, iso = detect_country(str(num))
    otp = extract_otp(str(msg)) or otp_override or "—"
    vals = {
        "service": f'{service_emoji_tag(service)} {html_mod.escape(str(service))}',
        "flag": country_emoji_tag(iso),
        "iso": iso,
        "country": html_mod.escape(str(country)),
        "number": mask_number(str(num)),
        "language": lang,
        "otp": html_mod.escape(str(otp)),
        "message": html_mod.escape(str(msg)),
        "time": datetime.utcnow().strftime("%H:%M:%S"),
    }
    tpl = get_setting("otp_template", DEFAULT_OTP_TEMPLATE) or DEFAULT_OTP_TEMPLATE
    tpl = premiumize(tpl)
    for k, v in vals.items():
        tpl = tpl.replace("{" + k + "}", v)
    # Force FULL MESSAGE body as quote if not already blockquote
    if "<blockquote>" not in tpl and vals.get("message"):
        # if raw message still present as plain, wrap last occurrence of escaped message
        msg = vals["message"]
        if msg and msg in tpl:
            tpl = tpl.replace(msg, f"<blockquote>{msg}</blockquote>", 1)
    return tpl


def otp_keyboard_raw(otp, with_style=True, with_copy=True):
    def st(btn, style=None):
        if with_style and style:
            btn["style"] = style
        return btn
    rows = []
    if otp:
        digits = re.sub(r"\D", "", str(otp)) or str(otp)
        btn = {"text": str(otp), "icon_custom_emoji_id": UI_EMOJI.get("✅") or "6147565374289220368"}
        if with_copy:
            btn["copy_text"] = {"text": digits}
        rows.append([st(btn, "success")])
    def clean_label(name, fallback):
        t = re.sub(r"^[^\w]*", "", (name or fallback)).strip()
        return t or fallback
    ch = {
        "text": clean_label(get_setting("numbers_btn_name", "CHANNEL"), "CHANNEL"),
        "url": get_setting("numbers_channel", NUMBERS_CHANNEL),
        "icon_custom_emoji_id": UI_EMOJI.get("🚀") or "5316571734604790521",
    }
    og = {
        "text": clean_label(get_setting("otp_btn_name", "OTP GROUP"), "OTP GROUP"),
        "url": get_setting("otp_group_link", OTP_GROUP_LINK),
        "icon_custom_emoji_id": UI_EMOJI.get("🔔") or "6314420734865185420",
    }
    md = {
        "text": clean_label(get_setting("methods_btn_name", "METHODS"), "METHODS"),
        "url": get_setting("methods_link", "https://youtube.com"),
        "icon_custom_emoji_id": UI_EMOJI.get("🥂") or "5260567255145539253",
    }
    rows.append([st(ch, "danger"), st(og, "primary")])
    rows.append([st(md, "success")])
    return {"inline_keyboard": rows}



def _raw_send(chat_id, text, markup):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML",
              "disable_web_page_preview": True, "reply_markup": markup},
        timeout=20,
    )
    j = r.json()
    if not j.get("ok"):
        raise RuntimeError(j.get("description", "sendMessage failed"))
    return j


async def send_otp_raw(chat_id, text, otp):
    attempts = [(True, True), (False, True), (False, False)]
    last = None
    for with_style, with_copy in attempts:
        try:
            return await asyncio.to_thread(_raw_send, chat_id, text, otp_keyboard_raw(otp, with_style, with_copy))
        except Exception as e:
            last = e
            emsg = str(e).lower()
            if any(x in emsg for x in ("emoji", "entity", "parse entities", "custom")):
                break
            if "chat not found" in emsg or "forbidden" in emsg or "blocked" in emsg:
                break
    try:
        return await asyncio.to_thread(_raw_send, chat_id, strip_premium(text), otp_keyboard_raw(otp, False, False))
    except Exception as e:
        raise last or e


# ==================== KEYBOARDS ====================
def with_admin_btn(kb, user_id):
    if not is_owner(user_id):
        return kb
    rows = [list(r) for r in kb.inline_keyboard]
    rows.append([B(get_setting("btn_admin", "⚙️ Admin Panel"), "admin", style="danger")])
    return InlineKeyboardMarkup(rows)


def main_user_kb():
    return InlineKeyboardMarkup([
        [B(get_setting("btn_get_number", "📱 GET NUMBER"), "get_number", style="primary")],
        [B(get_setting("btn_high_traffic", "🔥 High Traffic"), "high_traffic", style="danger")],
        [B(get_setting("methods_btn_name", "🎬 METHODS"), url=get_setting("methods_link", "https://youtube.com"), style="success")],
        [B(get_setting("btn_help", "🆘 Help"), "help", style="primary")],
    ])


def owner_kb():
    return InlineKeyboardMarkup([
        [B(get_setting("btn_add_nums", "📥 Add Numbers (.txt)"), "adm_add_nums", style="success"),
         B(get_setting("btn_rm_nums", "🗑 Remove Numbers"), "adm_rm_nums", style="danger")],
        [B(get_setting("btn_list_nums", "📋 List Numbers"), "adm_list_nums", style="primary"),
         B(get_setting("btn_num_limit", "🔢 Numbers Limit"), "adm_num_limit", style="primary")],
        [B(get_setting("btn_fj_add", "➕ Force Join Add"), "adm_fj_add", style="success"),
         B(get_setting("btn_fj_rm", "➖ Force Join Remove"), "adm_fj_rm", style="danger")],
        [B(get_setting("btn_fj_list", "📋 Force Join List"), "adm_fj_list", style="primary")],
        [B(get_setting("btn_ban", "🚫 Ban User"), "adm_ban", style="danger"),
         B(get_setting("btn_unban", "✅ Unban User"), "adm_unban", style="success")],
        [B(get_setting("btn_broadcast", "📣 Broadcast"), "adm_broadcast", style="primary"),
         B(get_setting("btn_stats", "📊 Statistics"), "adm_stats", style="primary")],
        [B(get_setting("btn_otp_group", "📬 OTP Group ID"), "adm_otp_group", style="primary"),
         B(get_setting("btn_welcome", "📝 Welcome Msg"), "adm_welcome", style="primary")],
        [B(get_setting("btn_link_numbers", "🔗 Numbers Channel Link"), "adm_btn_numbers", style="primary"),
         B(get_setting("btn_link_otp", "🔗 OTP Group Link"), "adm_btn_otp", style="primary")],
        [B(get_setting("btn_backup", "💾 Backup DB"), "adm_backup", style="success"),
         B(get_setting("btn_restore", "♻️ Restore DB"), "adm_restore", style="danger")],
        [B("📋 Logs Channel", "adm_logs_channel", style="primary"),
         B("🎨 OTP Styles", "adm_otp_styles", style="primary"),
         B(get_setting("btn_test_otp", "🧪 Test OTP"), "adm_test_otp", style="success"),
         B("🧩 CUSTOM OTP MSG", "adm_otp_custom", style="success"),
         B("✏️ Rename Buttons", "adm_rename", style="primary")],
        [B("🎬 Set Methods Link", "adm_methods_link", style="success")],
        [B(get_setting("btn_close", "🔙 Close"), "close", style="primary")],
    ])


# ==================== HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    ensure_user(u)
    if is_banned(u.id):
        await update.message.reply_text(f"{uie('🚫')} You are banned.", parse_mode=ParseMode.HTML)
        return
    if not is_owner(u.id) and not await force_join_ok(context.bot, u.id):
        kb = await force_join_keyboard(context.bot)
        await update.message.reply_text(
            f"{uie('🚨')} <b>Access Locked</b>\n\nJoin all required channels/groups first, then tap Check.",
            parse_mode=ParseMode.HTML, reply_markup=kb)
        return
    welcome = premiumize(get_setting("welcome"))
    kb = with_admin_btn(main_user_kb(), u.id)
    await update.message.reply_text(welcome, parse_mode=ParseMode.HTML, reply_markup=kb)


async def cb_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    u = q.from_user
    data = q.data
    ensure_user(u)

    if is_banned(u.id) and not is_owner(u.id):
        await q.edit_message_text(f"{uie('🚫')} You are banned.", parse_mode=ParseMode.HTML)
        return

    if data == "fj_check":
        if await force_join_ok(context.bot, u.id):
            welcome = premiumize(get_setting("welcome"))
            kb = with_admin_btn(main_user_kb(), u.id)
            await q.edit_message_text(welcome + f"\n\n{uie('✅')} Verified!", parse_mode=ParseMode.HTML, reply_markup=kb)
        else:
            kb = await force_join_keyboard(context.bot, u.id)
            try:
                await q.edit_message_text(
                    "⚠️ <b>Still missing channels</b>\n\nJoin the channels below, then tap <b>I Joined — Check</b> again.\nOtherwise you cannot use this bot.",
                    parse_mode=ParseMode.HTML, reply_markup=kb)
            except Exception:
                await q.answer("Still not joined all channels!", show_alert=True)
        return

    if data == "admin" and is_owner(u.id):
        await q.edit_message_text(f"{uie('👑')} <b>Admin Panel</b>", parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data == "close":
        await q.edit_message_text("Closed.")
        return

    if data == "help":
        await q.edit_message_text(
            premiumize("🆘 <b>Help</b>\n\n1. Tap GET NUMBER\n2. Choose service\n3. Copy a number\n4. Wait for OTP in OTP Group"),
            parse_mode=ParseMode.HTML, reply_markup=with_admin_btn(main_user_kb(), u.id))
        return

    if data == "high_traffic":
        c = db()
        rows = c.execute("SELECT service, country, iso, cnt FROM otp_stats ORDER BY cnt DESC LIMIT 20").fetchall()
        if not rows:
            rows = c.execute("SELECT service, country, iso, COUNT(*) as cnt FROM numbers WHERE active=1 GROUP BY service, country, iso ORDER BY cnt DESC LIMIT 20").fetchall()
        c.close()
        if not rows:
            text = premiumize("🚫 <b>High Traffic</b>\n\nNo traffic yet. OTPs aane ke baad yahan dikhega.")
        else:
            lines = [premiumize("🔥 <b>High Traffic</b>\n\nMost active service + country:\n")]
            for r in rows:
                lines.append(f"{country_emoji_tag(r['iso'])} <b>{r['country']}</b> — {service_emoji_tag(r['service'])} {r['service']}  •  {r['cnt']} OTPs")
            text = "\n".join(lines)
        await q.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=with_admin_btn(main_user_kb(), u.id))
        return

    if data == "get_number":
        if not is_owner(u.id) and not await force_join_ok(context.bot, u.id):
            kb = await force_join_keyboard(context.bot)
            await q.edit_message_text(f"{uie('🚨')} Join required channels first.", parse_mode=ParseMode.HTML, reply_markup=kb)
            return
        c = db()
        services = c.execute("SELECT DISTINCT service FROM numbers WHERE active=1 ORDER BY service").fetchall()
        c.close()
        if not services:
            await q.edit_message_text(
                premiumize("🚫 No numbers available yet. Owner must add numbers."),
                parse_mode=ParseMode.HTML, reply_markup=with_admin_btn(main_user_kb(), u.id))
            return
        kb = []
        for s in services:
            kb.append([B(s["service"], f"svc_{s['service']}", style="primary", icon=service_icon_id(s["service"]))])
        kb.append([B("🔙 Back", "back_main", style="primary")])
        await q.edit_message_text(
            f"{uie('👍')} <b>Select Service</b>",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("svc_"):
        service = data[4:]
        c = db()
        countries = c.execute(
            "SELECT country, iso, COUNT(*) as cnt FROM numbers WHERE active=1 AND service=? GROUP BY country, iso ORDER BY cnt DESC",
            (service,)).fetchall()
        c.close()
        if not countries:
            await q.edit_message_text(
                premiumize("🚫 No numbers for this service."),
                parse_mode=ParseMode.HTML, reply_markup=with_admin_btn(main_user_kb(), u.id))
            return
        kb = []
        for r in countries:
            kb.append([B(f"{r['country']} ({r['cnt']})", f"cty_{service}|{r['iso']}", style="primary", icon=country_icon_id(r["iso"]))])
        kb.append([B("🔙 Back", "get_number", style="primary")])
        await q.edit_message_text(
            f"{service_emoji_tag(service)} <b>{service}</b> — Select Country",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("cty_"):
        rest = data[4:]
        if "|" not in rest: return
        service, iso = rest.split("|", 1)
        limit = int(get_setting("numbers_per_show", DEFAULT_NUMBERS_PER_USER))
        c = db()
        rows = c.execute(
            "SELECT number, country, iso FROM numbers WHERE active=1 AND service=? AND iso=? ORDER BY RANDOM() LIMIT ?",
            (service, iso, limit)).fetchall()
        for r in rows:
            c.execute("INSERT INTO assignments (user_id, number, service, assigned_at) VALUES (?,?,?,?)",
                      (u.id, r["number"], service, datetime.utcnow().isoformat()))
        c.commit()
        c.close()
        if not rows:
            await q.edit_message_text(
                premiumize("🚫 No numbers for this country."),
                parse_mode=ParseMode.HTML, reply_markup=with_admin_btn(main_user_kb(), u.id))
            return
        lines = [f"{service_emoji_tag(service)} <b>{service}</b> — {country_emoji_tag(iso)} numbers\n\n"
                 f"{uie('🔔')} OTP ine pe aaye to aapko DM + group dono me milega.\n"]
        kb_rows = []
        for r in rows:
            lines.append(f"{country_emoji_tag(r['iso'])} <code>{r['number']}</code>")
            kb_rows.append([B(str(r["number"]), style="success", copy=r["number"], icon="✅")])
        kb_rows.append([
            B(get_setting("numbers_btn_name", "📦 Numbers Channel"), url=get_setting("numbers_channel", NUMBERS_CHANNEL), style="danger"),
            B(get_setting("otp_btn_name", "📢 OTP Group"), url=get_setting("otp_group_link", OTP_GROUP_LINK), style="primary"),
        ])
        kb_rows.append([B(get_setting("methods_btn_name", "🎬 METHODS"), url=get_setting("methods_link", "https://youtube.com"), style="success")])
        kb_rows.append([B("NEW NUMBERS", f"newnum_{service}|{iso}", style="success", icon="👑")])
        kb_rows.append([B("🔙 Back", f"svc_{service}", style="primary")])
        await q.edit_message_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb_rows))
        return

    if data.startswith("newnum_"):
        rest = data[len("newnum_"):]
        if "|" not in rest: return
        service, iso = rest.split("|", 1)
        limit = int(get_setting("numbers_per_show", DEFAULT_NUMBERS_PER_USER))
        c = db()
        rows = c.execute(
            "SELECT number, country, iso FROM numbers WHERE active=1 AND service=? AND iso=? ORDER BY RANDOM() LIMIT ?",
            (service, iso, limit)).fetchall()
        for r in rows:
            c.execute("INSERT INTO assignments (user_id, number, service, assigned_at) VALUES (?,?,?,?)",
                      (u.id, r["number"], service, datetime.utcnow().isoformat()))
        c.commit()
        c.close()
        if not rows:
            await q.answer("No more numbers available!", show_alert=True)
            return
        lines = [f"{service_emoji_tag(service)} <b>{service}</b> — {country_emoji_tag(iso)} New Numbers\n\n"
                 f"{uie('🔔')} OTP ine pe aaye to aapko DM + group dono me milega.\n"]
        kb_rows = []
        for r in rows:
            lines.append(f"{country_emoji_tag(r['iso'])} <code>{r['number']}</code>")
            kb_rows.append([B(str(r["number"]), style="success", copy=r["number"], icon="✅")])
        kb_rows.append([
            B(get_setting("numbers_btn_name", "📦 Numbers Channel"), url=get_setting("numbers_channel", NUMBERS_CHANNEL), style="danger"),
            B(get_setting("otp_btn_name", "📢 OTP Group"), url=get_setting("otp_group_link", OTP_GROUP_LINK), style="primary"),
        ])
        kb_rows.append([B(get_setting("methods_btn_name", "🎬 METHODS"), url=get_setting("methods_link", "https://youtube.com"), style="success")])
        kb_rows.append([B("NEW NUMBERS", f"newnum_{service}|{iso}", style="success", icon="👑")])
        kb_rows.append([B("🔙 Back", f"svc_{service}", style="primary")])
        await q.edit_message_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb_rows))
        return

    if data == "noop": return

    if data == "back_main":
        welcome = premiumize(get_setting("welcome"))
        kb = with_admin_btn(main_user_kb(), u.id)
        await q.edit_message_text(welcome, parse_mode=ParseMode.HTML, reply_markup=kb)
        return

    if not is_owner(u.id): return

    if data == "adm_add_nums":
        context.user_data["state"] = "await_txt"
        await q.edit_message_text(
            premiumize("📥 Send a <b>.txt</b> file with numbers (one per line).\n\nAfter upload I will ask for <b>Service name</b> (e.g. WhatsApp)."),
            parse_mode=ParseMode.HTML)
        return

    if data == "adm_rm_nums":
        c = db()
        services = c.execute("SELECT DISTINCT service FROM numbers WHERE active=1 ORDER BY service").fetchall()
        c.close()
        if not services:
            await q.edit_message_text(premiumize("🚫 No active numbers in DB."),
                                     parse_mode=ParseMode.HTML, reply_markup=owner_kb())
            return
        kb = []
        for s in services:
            kb.append([B(f"🗑 {s['service']}", f"rm_svc_{s['service']}", style="danger")])
        kb.append([B("🔙 Back", "admin", style="primary")])
        await q.edit_message_text(
            premiumize("🗑 <b>Remove Numbers</b>\n\nSelect <b>Service</b> to remove numbers from:"),
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("rm_svc_"):
        service = data[len("rm_svc_"):]
        c = db()
        countries = c.execute(
            "SELECT country, iso, COUNT(*) as cnt FROM numbers WHERE active=1 AND service=? GROUP BY country, iso ORDER BY cnt DESC",
            (service,)).fetchall()
        c.close()
        if not countries:
            await q.edit_message_text(premiumize("🚫 No numbers for this service."),
                                     parse_mode=ParseMode.HTML, reply_markup=owner_kb())
            return
        kb = []
        for r in countries:
            kb.append([B(f"{flag_emoji(r['iso'])} {r['country']} — {r['cnt']} numbers",
                         f"rm_cty_{service}|{r['iso']}", style="danger")])
        kb.append([B("🗑 Remove ALL from this service", f"rm_all_svc_{service}", style="danger")])
        kb.append([B("🔙 Back", "adm_rm_nums", style="primary")])
        await q.edit_message_text(
            f"{service_emoji_tag(service)} <b>{service}</b> — Select Country to remove:\n\n<i>Tap a country to delete all its numbers, or remove the whole service.</i>",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("rm_cty_"):
        rest = data[len("rm_cty_"):]
        if "|" not in rest: return
        service, iso = rest.split("|", 1)
        c = db()
        c.execute("UPDATE numbers SET active=0 WHERE service=? AND iso=?", (service, iso))
        n = c.total_changes
        c.commit()
        c.close()
        await q.edit_message_text(
            premiumize(f"✅ Removed <b>{n}</b> numbers\nService: <b>{service}</b> | Country: <b>{iso}</b>"),
            parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data.startswith("rm_all_svc_"):
        service = data[len("rm_all_svc_"):]
        c = db()
        c.execute("UPDATE numbers SET active=0 WHERE service=?", (service,))
        n = c.total_changes
        c.commit()
        c.close()
        await q.edit_message_text(
            premiumize(f"✅ Removed all <b>{n}</b> numbers for service <b>{service}</b>"),
            parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data == "adm_list_nums":
        c = db()
        rows = c.execute("SELECT service, country, iso, COUNT(*) as cnt FROM numbers WHERE active=1 GROUP BY service, country, iso ORDER BY service").fetchall()
        total = c.execute("SELECT COUNT(*) as c FROM numbers WHERE active=1").fetchone()["c"]
        c.close()
        lines = [premiumize(f"📊 <b>Numbers</b> — total active: {total}\n")]
        for r in rows[:40]:
            lines.append(f"{country_emoji_tag(r['iso'])} {r['country']} | {service_emoji_tag(r['service'])} {r['service']}: {r['cnt']}")
        await q.edit_message_text("\n".join(lines) or "Empty", parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data == "adm_num_limit":
        context.user_data["state"] = "await_limit"
        await q.edit_message_text(premiumize(f"Current limit: <b>{get_setting('numbers_per_show')}</b>\nSend new number:"),
                                 parse_mode=ParseMode.HTML)
        return

    if data == "adm_fj_add":
        context.user_data["state"] = "await_fj"
        await q.edit_message_text(premiumize("➕ Send channel/group ID or @username\nBot must be admin there."),
                                 parse_mode=ParseMode.HTML)
        return

    if data == "adm_fj_rm":
        context.user_data["state"] = "await_fj_rm"
        await q.edit_message_text(premiumize("➖ Send force-join chat_id to remove:"), parse_mode=ParseMode.HTML)
        return

    if data == "adm_fj_list":
        c = db()
        rows = c.execute("SELECT * FROM force_joins").fetchall()
        c.close()
        if not rows:
            text = premiumize("📊 No force-join channels.")
        else:
            text = premiumize("📊 <b>Force Join List</b>\n\n") + "\n".join(
                f"• {r['title'] or '?'} — <code>{r['chat_id']}</code>" for r in rows)
        await q.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data == "adm_ban":
        context.user_data["state"] = "await_ban"
        await q.edit_message_text(premiumize("🚫 Send user ID to ban:"), parse_mode=ParseMode.HTML)
        return

    if data == "adm_unban":
        context.user_data["state"] = "await_unban"
        await q.edit_message_text(premiumize("✅ Send user ID to unban:"), parse_mode=ParseMode.HTML)
        return

    if data == "adm_broadcast":
        context.user_data["state"] = "await_broadcast"
        await q.edit_message_text(premiumize("📣 Send message to broadcast to all users:"), parse_mode=ParseMode.HTML)
        return

    if data == "adm_stats":
        c = db()
        users = c.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
        banned = c.execute("SELECT COUNT(*) as c FROM users WHERE is_banned=1").fetchone()["c"]
        nums = c.execute("SELECT COUNT(*) as c FROM numbers WHERE active=1").fetchone()["c"]
        fj = c.execute("SELECT COUNT(*) as c FROM force_joins").fetchone()["c"]
        c.close()
        text = (
            f"{uie('📊')} <b>Statistics</b>\n\n"
            f"👥 Users: {users}\n"
            f"{uie('🚫')} Banned: {banned}\n"
            f"📱 Active numbers: {nums}\n"
            f"🔒 Force-join: {fj}\n"
            f"📬 OTP Group: <code>{get_setting('otp_group_id')}</code>"
        )
        await q.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data == "adm_otp_group":
        context.user_data["state"] = "await_otp_gid"
        await q.edit_message_text(
            premiumize(f"Current OTP Group ID: <code>{get_setting('otp_group_id')}</code>\n\nSend new group ID:"),
            parse_mode=ParseMode.HTML)
        return

    if data == "adm_welcome":
        context.user_data["state"] = "await_welcome"
        await q.edit_message_text(premiumize("📝 Send new welcome message (HTML allowed):"), parse_mode=ParseMode.HTML)
        return

    if data == "adm_btn_numbers":
        context.user_data["state"] = "await_btn_numbers"
        await q.edit_message_text(premiumize(f"Current: {get_setting('numbers_channel')}\nSend new Numbers Channel URL:"),
                                 parse_mode=ParseMode.HTML)
        return

    if data == "adm_btn_otp":
        context.user_data["state"] = "await_btn_otp"
        await q.edit_message_text(premiumize(f"Current: {get_setting('otp_group_link')}\nSend new OTP Group URL:"),
                                 parse_mode=ParseMode.HTML)
        return

    if data == "adm_methods_link":
        context.user_data["state"] = "await_methods_link"
        cur = get_setting("methods_link", "https://youtube.com")
        await q.edit_message_text(
            premiumize(f"🎬 <b>Set Methods Link</b>\n\nCurrent: <code>{cur}</code>\n\nSend new YouTube (or any) link:"),
            parse_mode=ParseMode.HTML)
        return

    if data == "adm_backup":
        if os.path.exists(DB_PATH):
            await context.bot.send_document(u.id, document=InputFile(DB_PATH), caption="💾 DB Backup")
            await q.answer("Backup sent")
        else:
            await q.answer("No DB", show_alert=True)
        return

    if data == "adm_rename":
        keys = [
            ("btn_get_number", "User: GET NUMBER"),
            ("btn_high_traffic", "User: High Traffic"),
            ("btn_help", "User: Help"),
            ("btn_admin", "User: Admin Panel"),
            ("btn_add_nums", "Admin: Add Numbers"),
            ("btn_rm_nums", "Admin: Remove Numbers"),
            ("btn_list_nums", "Admin: List Numbers"),
            ("btn_num_limit", "Admin: Numbers Limit"),
            ("btn_fj_add", "Admin: Force Join Add"),
            ("btn_fj_rm", "Admin: Force Join Remove"),
            ("btn_fj_list", "Admin: Force Join List"),
            ("btn_ban", "Admin: Ban User"),
            ("btn_unban", "Admin: Unban User"),
            ("btn_broadcast", "Admin: Broadcast"),
            ("btn_stats", "Admin: Statistics"),
            ("btn_otp_group", "Admin: OTP Group ID"),
            ("btn_welcome", "Admin: Welcome Msg"),
            ("btn_link_numbers", "Admin: Numbers Channel Link"),
            ("btn_link_otp", "Admin: OTP Group Link"),
            ("btn_backup", "Admin: Backup DB"),
            ("btn_restore", "Admin: Restore DB"),
            ("btn_test_otp", "Admin: Test OTP"),
            ("btn_close", "Admin: Close"),
            ("numbers_btn_name", "Link btn: Numbers Channel"),
            ("otp_btn_name", "Link btn: OTP Group"),
            ("methods_btn_name", "Link btn: METHODS"),
        ]
        lines = [premiumize("✏️ <b>Rename Buttons</b>\n\nSend the <b>number</b> of the button to rename:\n")]
        for i, (k, label) in enumerate(keys, 1):
            cur = get_setting(k, label)
            lines.append(f"{i}. {label}\n   Current: <code>{cur}</code>")
        context.user_data["rename_keys"] = keys
        context.user_data["state"] = "await_rename_num"
        await q.edit_message_text("\n".join(lines), parse_mode=ParseMode.HTML)
        return

    
    if data == "adm_otp_styles" or data.startswith("adm_otp_styles_page_"):
        page = 0
        if data.startswith("adm_otp_styles_page_"):
            try:
                page = int(data.split("_")[-1])
            except Exception:
                page = 0
        page = max(0, page)
        start = page * 5
        chunk = STYLE_PRESETS[start:start+5]
        if not chunk:
            page = 0
            start = 0
            chunk = STYLE_PRESETS[0:5]
        lines = ["🎨 <b>OTP Message Styles</b>\n\nPick a number (send the number):\n"]
        for i, st in enumerate(chunk, start + 1):
            preview = st.replace("{service}", "WhatsApp").replace("{flag}", "🇩🇪").replace("{iso}", "DE").replace("{number}", "+49***57047").replace("{language}", "English").replace("{otp}", "61215").replace("{message}", "Telegram code: 61215").replace("{country}", "Germany").replace("{service_emoji}", "")
            lines.append(f"<b>{i}.</b>\n<code>{html_mod.escape(preview[:180])}...</code>\n")
        context.user_data["state"] = "await_style_pick"
        context.user_data["style_page"] = page
        kb_rows = []
        if start + 5 < len(STYLE_PRESETS):
            kb_rows.append([B("⏭ Next 5 Styles", f"adm_otp_styles_page_{page+1}", style="primary")])
        if page > 0:
            kb_rows.append([B("⏮ Previous", f"adm_otp_styles_page_{page-1}", style="primary")])
        kb_rows.append([B("🔙 Back", "admin", style="primary")])
        await q.edit_message_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb_rows))
        return

    if data == "adm_otp_custom":
        cur = get_setting("otp_template", DEFAULT_OTP_TEMPLATE)
        context.user_data["state"] = "await_otp_tpl"
        await q.edit_message_text(
            "🧩 <b>CUSTOM OTP MESSAGE</b>\n\n<b>Current:</b>\n<pre>" + html_mod.escape(cur[:500]) + "</pre>\n\n"
            "<b>Placeholders:</b>\n" + TEMPLATE_HELP + "\n\n"
            "Send your full custom template now (HTML ok).",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[B("🔙 Back", "admin", style="primary")]]),
        )
        return

    
    if data == "adm_logs_channel":
        cur = get_setting("logs_channel_id", "not set")
        context.user_data["state"] = "await_logs_channel"
        await q.edit_message_text(
            f"📋 <b>Logs Channel</b>\\n\\nCurrent: <code>{cur}</code>\\n\\n"
            "Bot must be <b>admin</b> in that channel/group.\\n"
            "Send channel/group ID (e.g. <code>-100123...</code>) or @username:",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[B("🔙 Back", "admin", style="primary")]]),
        )
        return

    if data == "adm_test_otp":
        gid = int(get_setting("otp_group_id", OTP_GROUP_ID))
        service = "Telegram"
        num = "+4915568557047"
        msg = "Telegram code: 61215\n\nYou can also tap on this link to log in:\nhttps://t.me/login/61215\n\noLeq9AcOZkT"
        otp = extract_otp(msg)
        box = render_otp_text(service, num, msg, "English")
        try:
            await send_otp_raw(gid, box, otp or "61215")
            await q.answer("✅ Test OTP sent to group")
            await q.edit_message_text(premiumize("✅ Test OTP sent to OTP group.\n\nCheck the group."),
                                     parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        except Exception as e:
            await q.answer(f"Fail: {e}", show_alert=True)
            await q.edit_message_text(
                premiumize(f"🚨 Could not send to group <code>{gid}</code>\n\nError: {e}\n\nMake bot admin in that group."),
                parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data == "adm_otp_tpl":
        cur = get_setting("otp_template", DEFAULT_OTP_TEMPLATE)
        kb = InlineKeyboardMarkup([
            [B("♻️ Reset to Default", "adm_otp_tpl_reset", style="danger")],
            [B("🔙 Back", "admin", style="primary")],
        ])
        context.user_data["state"] = "await_otp_tpl"
        await q.edit_message_text(
            "🧩 <b>OTP Message Format</b>\n\n<b>Current:</b>\n<pre>" + html_mod.escape(cur) + "</pre>\n"
            "<b>Placeholders:</b>\n" + TEMPLATE_HELP + "\n\n"
            "HTML allowed.\n👉 Send the <b>new format</b> now:",
            parse_mode=ParseMode.HTML, reply_markup=kb)
        return

    if data == "adm_otp_tpl_reset":
        set_setting("otp_template", DEFAULT_OTP_TEMPLATE)
        context.user_data.clear()
        await q.edit_message_text(premiumize("✅ OTP message format reset to default."),
                                 parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if data == "adm_restore":
        context.user_data["state"] = "await_restore"
        await q.edit_message_text(premiumize("♻️ Send the .db backup file to restore:"), parse_mode=ParseMode.HTML)
        return


async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    if not is_owner(u.id): return
    state = context.user_data.get("state")
    text = (update.message.text or "").strip()

    if state == "await_service":
        service = text
        pending = context.user_data.get("pending_numbers") or []
        if not pending:
            await update.message.reply_text(premiumize("No pending numbers."), parse_mode=ParseMode.HTML)
            context.user_data.clear()
            return
        c = db()
        added = 0
        for num in pending:
            country, iso = detect_country(num)
            try:
                c.execute(
                    "INSERT INTO numbers (number, country, iso, service, added_by, added_at, active) VALUES (?,?,?,?,?,?,1) "
                    "ON CONFLICT(number) DO UPDATE SET "
                    "country=excluded.country, iso=excluded.iso, service=excluded.service, "
                    "added_by=excluded.added_by, added_at=excluded.added_at, active=1",
                    (num, country, iso, service, u.id, datetime.utcnow().isoformat()))
                added += 1
            except Exception:
                pass
        c.commit()
        c.close()
        context.user_data.clear()
        await update.message.reply_text(
            premiumize(f"✅ Added <b>{added}</b> numbers for service {service_emoji_tag(service)} <b>{service}</b>"),
            parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    
    
    if state == "await_logs_channel":
        raw = text.strip()
        chat_id = raw
        try:
            if raw.startswith("@"):
                chat = await context.bot.get_chat(raw)
                chat_id = str(chat.id)
            else:
                chat_id = str(int(raw))
            set_setting("logs_channel_id", chat_id)
            await context.bot.send_message(int(chat_id), "✅ <b>Logs channel connected</b>\\nBot will post activity here.", parse_mode=ParseMode.HTML)
            context.user_data.clear()
            await update.message.reply_text(
                f"✅ Logs channel set: <code>{chat_id}</code>",
                parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        except Exception as e:
            await update.message.reply_text(f"❌ Failed: {e}\\nMake bot admin and send correct ID.")
        return

    if state == "await_style_pick":
        if not text.isdigit():
            await update.message.reply_text("Send a style number from the list.")
            return
        n = int(text)
        if not (1 <= n <= len(STYLE_PRESETS)):
            await update.message.reply_text(f"Send 1-{len(STYLE_PRESETS)}")
            return
        chosen = STYLE_PRESETS[n - 1]
        set_setting("otp_template", chosen)
        context.user_data.clear()
        try:
            preview = render_otp_text("WhatsApp", "+84912396510", "Your WhatsApp code 927-002", "English")
            await update.message.reply_text("✅ Style <b>%d</b> applied.\n\nPreview:\n%s" % (n, preview), parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        except Exception as e:
            await update.message.reply_text(f"✅ Style {n} saved. Preview error: {e}", reply_markup=owner_kb())
        return

    if state == "await_otp_tpl":
        old = get_setting("otp_template", DEFAULT_OTP_TEMPLATE)
        set_setting("otp_template", update.message.text_html or text)
        try:
            preview = render_otp_text("WhatsApp", "+84912396510", "Your WhatsApp code 927-002", "English")
            await update.message.reply_text(premiumize("❤️‍🔥 <b>Preview:</b>\n\n") + preview, parse_mode=ParseMode.HTML)
        except Exception as e:
            set_setting("otp_template", old)
            await update.message.reply_text(f"🚨 Invalid HTML format, not saved.\n{e}\n\nSend again:")
            return
        context.user_data.clear()
        await update.message.reply_text(premiumize("✅ OTP message format saved."),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_methods_link":
        if text.startswith("http"):
            set_setting("methods_link", text)
            context.user_data.clear()
            await update.message.reply_text(
                premiumize(f"✅ Methods link updated:\n<code>{text}</code>"),
                parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        else:
            await update.message.reply_text("Send a valid URL starting with http:// or https://")
        return

    if state == "await_limit":
        if text.isdigit() and 1 <= int(text) <= 20:
            set_setting("numbers_per_show", text)
            await update.message.reply_text(premiumize(f"✅ Limit set to {text}"),
                                            parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        else:
            await update.message.reply_text("Send a number 1-20")
            return
        context.user_data.clear()
        return

    if state == "await_fj":
        raw = text
        title = raw
        link = ""
        chat_id = raw
        try:
            if raw.startswith("@"):
                chat = await context.bot.get_chat(raw)
                chat_id = str(chat.id)
                title = chat.title or raw
                if chat.username:
                    link = f"https://t.me/{chat.username}"
            else:
                chat = await context.bot.get_chat(int(raw))
                chat_id = str(chat.id)
                title = chat.title or str(chat.id)
                if getattr(chat, "username", None):
                    link = f"https://t.me/{chat.username}"
        except Exception as e:
            await update.message.reply_text(f"🚨 Could not resolve chat: {e}")
            return
        c = db()
        c.execute("INSERT OR REPLACE INTO force_joins (chat_id, title, link) VALUES (?,?,?)", (chat_id, title, link))
        c.commit()
        c.close()
        context.user_data.clear()
        await update.message.reply_text(
            premiumize(f"✅ Force-join added: {title} (<code>{chat_id}</code>)"),
            parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_fj_rm":
        c = db()
        c.execute("DELETE FROM force_joins WHERE chat_id=?", (text,))
        n = c.total_changes
        c.commit()
        c.close()
        context.user_data.clear()
        await update.message.reply_text(premiumize(f"Removed: {n}"),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_ban":
        if text.isdigit():
            c = db()
            c.execute("INSERT OR IGNORE INTO users (user_id, join_date) VALUES (?,?)",
                      (int(text), datetime.utcnow().isoformat()))
            c.execute("UPDATE users SET is_banned=1 WHERE user_id=?", (int(text),))
            c.commit()
            c.close()
            await log_event(context.bot, f"🚫 <b>BAN</b>\nAdmin banned <code>{text}</code>")
            await update.message.reply_text(premiumize(f"🚫 Banned {text}"),
                                            parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        context.user_data.clear()
        return

    if state == "await_unban":
        if text.isdigit():
            c = db()
            c.execute("UPDATE users SET is_banned=0 WHERE user_id=?", (int(text),))
            c.commit()
            c.close()
            await update.message.reply_text(premiumize(f"✅ Unbanned {text}"),
                                            parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        context.user_data.clear()
        return

    if state == "await_broadcast":
        c = db()
        users = c.execute("SELECT user_id FROM users WHERE is_banned=0").fetchall()
        c.close()
        ok = fail = 0
        for r in users:
            try:
                await context.bot.send_message(r["user_id"], text, parse_mode=ParseMode.HTML)
                ok += 1
            except Exception:
                fail += 1
            await asyncio.sleep(0.05)
        context.user_data.clear()
        await update.message.reply_text(premiumize(f"📣 Sent: {ok} | Fail: {fail}"),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_welcome":
        set_setting("welcome", text)
        context.user_data.clear()
        await update.message.reply_text(premiumize("✅ Welcome updated"),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_otp_gid":
        set_setting("otp_group_id", text)
        context.user_data.clear()
        await update.message.reply_text(premiumize(f"✅ OTP Group ID set to <code>{text}</code>"),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_btn_numbers":
        set_setting("numbers_channel", text)
        context.user_data.clear()
        await update.message.reply_text(premiumize("✅ Numbers channel link updated"),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_btn_otp":
        set_setting("otp_group_link", text)
        context.user_data.clear()
        await update.message.reply_text(premiumize("✅ OTP group link updated"),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_rename_num":
        keys = context.user_data.get("rename_keys") or []
        if not text.isdigit() or not (1 <= int(text) <= len(keys)):
            await update.message.reply_text(f"Send a number 1-{len(keys)}")
            return
        idx = int(text) - 1
        key, label = keys[idx]
        context.user_data["rename_key"] = key
        context.user_data["state"] = "await_rename_name"
        await update.message.reply_text(
            f"Current: <code>{get_setting(key)}</code>\n\nSend <b>new name</b> for:\n{label}",
            parse_mode=ParseMode.HTML)
        return

    if state == "await_rename_name":
        key = context.user_data.get("rename_key")
        if not key:
            context.user_data.clear()
            return
        set_setting(key, text)
        context.user_data.clear()
        await update.message.reply_text(premiumize(f"✅ Button renamed to:\n<code>{text}</code>"),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return


async def doc_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    if not is_owner(u.id): return
    state = context.user_data.get("state")
    doc = update.message.document
    if not doc: return

    if state == "await_restore":
        f = await doc.get_file()
        await f.download_to_drive(DB_PATH)
        context.user_data.clear()
        await update.message.reply_text(premiumize("✅ DB restored. Restart recommended."),
                                        parse_mode=ParseMode.HTML, reply_markup=owner_kb())
        return

    if state == "await_txt" or (doc.file_name or "").endswith(".txt"):
        f = await doc.get_file()
        bio = BytesIO()
        await f.download_to_memory(bio)
        content = bio.getvalue().decode("utf-8", errors="ignore")
        nums = []
        for line in content.splitlines():
            line = line.strip()
            if not line: continue
            digits = re.sub(r"[^\d+]", "", line)
            if len(re.sub(r"\D", "", digits)) >= 8:
                if not digits.startswith("+"):
                    digits = "+" + re.sub(r"\D", "", digits)
                nums.append(digits)
        if not nums:
            await update.message.reply_text("No valid numbers found in file.")
            return
        context.user_data["pending_numbers"] = nums
        context.user_data["state"] = "await_service"
        await update.message.reply_text(
            premiumize(f"📊 Found <b>{len(nums)}</b> numbers.\n\nNow send <b>Service name</b> (e.g. WhatsApp, Telegram, Instagram):"),
            parse_mode=ParseMode.HTML)
        return


# ==================== OTP POLLER ====================
async def otp_poller(app: Application):
    await asyncio.sleep(3)
    bot = app.bot
    print("🚀 OTP poller started")
    try:
        r = requests.get(API_URL, timeout=15)
        data = r.json() if r.ok else []
        c = db()
        if isinstance(data, list):
            for item in data:
                if isinstance(item, (list, tuple)) and len(item) >= 4:
                    uid = f"{item[0]}_{item[1]}_{item[3]}"
                    c.execute("INSERT OR IGNORE INTO seen_otps (uid) VALUES (?)", (uid,))
            c.commit()
        c.close()
        print("📦 Seeded seen OTPs")
    except Exception as e:
        print("seed error", e)

    while True:
        try:
            r = requests.get(API_URL, timeout=15)
            data = r.json() if r.ok else []
            if not isinstance(data, list):
                await asyncio.sleep(POLL_INTERVAL)
                continue
            c = db()
            gid = int(get_setting("otp_group_id", OTP_GROUP_ID))
            for item in reversed(data):
                if not isinstance(item, (list, tuple)) or len(item) < 4:
                    continue
                service, num, msg, ts = item[0], item[1], item[2], item[3]
                uid = f"{service}_{num}_{ts}"
                row = c.execute("SELECT 1 FROM seen_otps WHERE uid=?", (uid,)).fetchone()
                if row: continue
                c.execute("INSERT OR IGNORE INTO seen_otps (uid) VALUES (?)", (uid,))
                c.commit()
                country, iso = detect_country(str(num))
                try:
                    c.execute(
                        "INSERT INTO otp_stats (service, iso, country, cnt) VALUES (?,?,?,1) ON CONFLICT(service, iso) DO UPDATE SET cnt = cnt + 1, country=excluded.country",
                        (str(service), iso, country))
                    c.commit()
                except Exception as _e:
                    print("stats", _e)
                otp = extract_otp(str(msg))
                masked = mask_number(str(num))
                lang = "English"
                msg_s = str(msg)
                if re.search(r"[\u0600-\u06FF]", msg_s): lang = "Arabic"
                elif re.search(r"[\u0400-\u04FF]", msg_s): lang = "Russian"
                elif re.search(r"[\u4e00-\u9fff]", msg_s): lang = "Chinese"
                box = render_otp_text(service, num, msg_s, lang)
                try:
                    await send_otp_raw(gid, box, otp)
                    print(f"✅ OTP {masked} {service} -> {gid}")
                except Exception as e:
                    print(f"❌ send otp fail gid={gid}: {e}")
                    alt = gid
                    s = str(gid)
                    if not s.startswith("-100") and s.lstrip("-").isdigit():
                        alt = int("-100" + s.lstrip("-"))
                        try:
                            await send_otp_raw(alt, box, otp)
                            print(f"✅ OTP via alt gid {alt}")
                            set_setting("otp_group_id", str(alt))
                        except Exception as e2:
                            print(f"❌ alt gid fail {alt}: {e2}")
                try:
                    digits = re.sub(r"\D", "", str(num))
                    assigned = c.execute(
                        "SELECT DISTINCT user_id FROM assignments WHERE REPLACE(REPLACE(number,'+',''),'-','') LIKE ? ORDER BY id DESC LIMIT 20",
                        (f"%{digits[-8:]}%",)).fetchall()
                    for ar in assigned:
                        try:
                            await send_otp_raw(ar["user_id"], box, otp)
                            print(f"📩 DM OTP to {ar['user_id']}")
                        except Exception as de:
                            print("dm fail", de)
                except Exception as ae:
                    print("assign lookup", ae)
                await asyncio.sleep(0.4)
            c.close()
        except Exception as e:
            print("poll error", e)
        await asyncio.sleep(POLL_INTERVAL)



async def on_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Notify when user leaves a force-join channel."""
    try:
        cmu = update.chat_member
        if not cmu:
            return
        chat = cmu.chat
        user = cmu.new_chat_member.user
        old_s = cmu.old_chat_member.status
        new_s = cmu.new_chat_member.status
        if new_s not in ("left", "kicked"):
            return
        if old_s in ("left", "kicked"):
            return
        c = db()
        row = c.execute("SELECT 1 FROM force_joins WHERE chat_id=?", (str(chat.id),)).fetchone()
        c.close()
        if not row:
            return
        uname = f"@{user.username}" if user.username else "—"
        title = chat.title or str(chat.id)
        # Notify user
        try:
            kb = await force_join_keyboard(context.bot, user.id)
            await context.bot.send_message(
                user.id,
                f"⚠️ <b>You left a required channel</b>\\n\\n"
                f"Channel: <b>{html_mod.escape(title)}</b>\\n\\n"
                f"Please join again the force-join channel(s), otherwise you <b>cannot use this bot</b>.",
                parse_mode=ParseMode.HTML,
                reply_markup=kb,
            )
        except Exception as e:
            print("leave notify user fail", e)
        await log_event(
            context.bot,
            f"🚪 <b>FORCE JOIN LEFT</b>\\n👤 {html_mod.escape(user.first_name or '')}\\n"
            f"🆔 <code>{user.id}</code>\\n📱 {uname}\\n📢 {html_mod.escape(title)} (<code>{chat.id}</code>)",
        )
    except Exception as e:
        print("on_chat_member", e)


async def post_init(app: Application):
    try:
        await app.bot.set_my_commands([BotCommand("start", "Start bot")])
    except Exception:
        pass
    asyncio.get_event_loop().create_task(otp_poller(app))


def main():
    init_db()
    set_setting("otp_group_id", "-1003791317242")
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(on_chat_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(CallbackQueryHandler(cb_router))
    app.add_handler(MessageHandler(filters.Document.ALL, doc_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    print("✨ MUZAMiL OTP BOT starting...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
