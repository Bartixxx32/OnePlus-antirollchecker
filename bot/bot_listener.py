import logging
import os
import json
import time
import aiohttp
import html as html_mod
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime, timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_PAT")
GITHUB_REPO = "Bartixxx32/OnePlus-antirollchecker"
WORKFLOW_ID = "telegram_check.yml"
ADMIN_USER_ID = 277390840  # Bartixxx32's Telegram user ID
BOT_VERSION = "1.1.0"
BOT_START_TIME = time.time()

# Paths
STATS_FILE = os.environ.get("STATS_FILE", "/data/stats.json")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Stats Management ---
def load_stats():
    """Load stats from JSON file."""
    try:
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "total_checks": 0,
            "total_errors": 0,
            "users": {},
            "daily": {},
            "first_check": None
        }

def save_stats(stats):
    """Save stats to JSON file."""
    try:
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save stats: {e}")

def record_check(user_id, username):
    """Record a check in stats."""
    stats = load_stats()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    stats["total_checks"] += 1
    
    uid = str(user_id)
    if uid not in stats["users"]:
        stats["users"][uid] = {"name": username, "count": 0}
    stats["users"][uid]["count"] += 1
    stats["users"][uid]["name"] = username  # Update name in case it changed
    
    if today not in stats["daily"]:
        stats["daily"][today] = 0
    stats["daily"][today] += 1

    if not stats["first_check"]:
        stats["first_check"] = today
    
    save_stats(stats)

def record_error():
    """Record an error in stats."""
    stats = load_stats()
    stats["total_errors"] += 1
    save_stats(stats)

# --- Rate Limiting ---
user_requests = defaultdict(list)
RATE_LIMIT_COUNT = 2
RATE_LIMIT_WINDOW = 60  # seconds

# --- Helpers ---
def format_uptime():
    """Format bot uptime as human-readable string."""
    elapsed = int(time.time() - BOT_START_TIME)
    days, remainder = divmod(elapsed, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)

DB_URL = "https://oparb.pages.dev/database.json"

async def fetch_database():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DB_URL, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
    except Exception as e:
        logging.error(f"Failed to fetch database.json: {e}")
    return None

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📱 Device Status", callback_data="cmd_status"), InlineKeyboardButton("🔥 Latest Firmwares", callback_data="cmd_latest")],
        [InlineKeyboardButton("📥 Download Links", callback_data="cmd_download")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Handlers ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error, notify user, and DM admin with details."""
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    record_error()
    
    if isinstance(update, Update) and update.effective_message:
         await update.effective_message.reply_text("❌ An internal error occurred. Please try again later.")
    
    # DM admin with error details
    try:
        error_text = str(context.error) if context.error else "Unknown error"
        chat_info = ""
        user_info = ""
        if isinstance(update, Update):
            if update.effective_chat:
                chat_info = f"\n📍 Chat: <code>{update.effective_chat.id}</code>"
            if update.effective_user:
                name = update.effective_user.first_name
                name = html.escape(str(name)) if name else "Unknown"
                user_info = f"\n👤 User: {name} (<code>{update.effective_user.id}</code>)"
        
        error_text_esc = html.escape(error_text[:500])
        admin_msg = (
            f"🚨 <b>Bot Error Alert</b>\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"{chat_info}{user_info}\n\n"
            f"❌ <code>{error_text_esc}</code>"
        )
        await context.bot.send_message(chat_id=ADMIN_USER_ID, text=admin_msg, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Failed to notify admin: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == 'private':
        await update.message.reply_text(
            "❌ This bot operates in the OnePlus ARB Checker group only.\n"
            "👉 Join here: https://t.me/oneplusarbchecker"
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! Send /check https://example.com/firmware.zip to analyze a firmware file.",
        reply_markup=get_main_keyboard()
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available commands and usage."""
    msg = (
        "🤖 *OnePlus ARB Checker Bot*\n\n"
        "*Available Commands:*\n\n"
        "🔍 /check `<url>` — Analyze a firmware file\n"
        "   _Send a direct download link to a OnePlus firmware .zip_\n\n"
        "📥 /download `<device>` `[region]` — Fetch latest firmware & auto-check ARB\n"
        "   _Example: /download OnePlus 15 EU_\n\n"
        "📱 /devicestatus `<device>` — Show current firmware & ARB info\n"
        "   _Example: /devicestatus OnePlus 12_\n\n"
        "🔥 /latest — Show the 5 most recently discovered firmwares\n\n"
        "ℹ️ /about — Bot info, version & uptime\n"
        "❓ /help — Show this message\n\n"
        "*How /download works:*\n"
        "1. Bot resolves device name → fetches firmware URL from API\n"
        "2. Triggers ARB analysis via GitHub Actions\n"
        "3. Posts download link + ARB results as replies\n\n"
        "📋 _Rate limit: 2 checks per minute_"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "cmd_status":
        await query.message.reply_text("📱 Usage: /devicestatus <device_name_or_model>\nExample: /devicestatus OnePlus 12")
    elif query.data == "cmd_latest":
        await latest(update, context, is_callback=True)
    elif query.data == "cmd_download":
        await download_cmd(update, context, is_callback=True)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot info, version, and uptime."""
    data = load_stats()
    uptime = format_uptime()
    
    msg = (
        f"ℹ️ *OnePlus ARB Checker Bot*\n\n"
        f"📦 *Version:* `{BOT_VERSION}`\n"
        f"⏱️ *Uptime:* {uptime}\n"
        f"🔢 *Total checks:* {data.get('total_checks', 0)}\n\n"
        f"🔗 [GitHub Repository](https://github.com/{GITHUB_REPO})\n"
        f"💬 [Support Group](https://t.me/oneplusarbchecker)\n\n"
        f"_Made with ❤️ by @Bartixxx32_"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=True)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics (admin only)."""
    user = update.effective_user
    
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ This command is restricted to the bot admin.")
        return
    
    data = load_stats()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_count = data.get("daily", {}).get(today, 0)
    
    # Top 5 users
    sorted_users = sorted(data.get("users", {}).items(), key=lambda x: x[1]["count"], reverse=True)[:5]
    
    top_users_text = "\n".join(
        [f"  {i+1}. {html.escape(str(u[1]['name']))} — {u[1]['count']}" for i, u in enumerate(sorted_users)]
    ) or "  No data yet"
    
    msg = (
        f"📊 <b>Bot Statistics</b>\n\n"
        f"🔢 Total checks: <b>{data.get('total_checks', 0)}</b>\n"
        f"❌ Total errors: <b>{data.get('total_errors', 0)}</b>\n"
        f"📅 Today: <b>{today_count}</b>\n"
        f"📆 Since: {data.get('first_check', 'N/A')}\n\n"
        f"👥 <b>Top Users:</b>\n{top_users_text}"
    )
    
    await update.message.reply_text(msg, parse_mode="HTML")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == 'private':
        return
    
    if not context.args:
        await update.message.reply_text("📱 Usage: /devicestatus <device_name_or_model>\nExample: /devicestatus OnePlus 12")
        return
        
    query = " ".join(context.args).lower().strip()
    data = await fetch_database()
    if not data:
        await update.message.reply_text("❌ Failed to fetch database. Try again later.")
        return
        
    found_models = []
    for model, details in data.items():
        if query in model.lower() or query in details.get("device_name", "").lower():
            found_models.append((model, details))
            
    if not found_models:
        await update.message.reply_text(f"❌ No data found for '{query}'.")
        return
        
    text = f"📱 **Search results for '{query}':**\n\n"
    for model, details in found_models[:10]:
        device_name = details.get("device_name", model)
        text += f"*{device_name}* (`{model}`)\n"
        versions = details.get("versions", {})
        if not versions:
            text += "  No firmwares known.\n"
        else:
            current_versions = [v for v, v_det in versions.items() if v_det.get('status') == 'current']
            if not current_versions:
                current_versions = list(versions.keys())[-3:]
            for v in current_versions:
                v_det = versions[v]
                is_hardcoded = v_det.get('is_hardcoded', False)
                if is_hardcoded:
                    arb_display = "?"
                    status_icon = "⚠️"
                else:
                    arb = v_det.get('arb', '?')
                    arb_display = arb
                    status_icon = "🟢" if arb == 0 else "🔴"
                md5 = v_det.get('md5', 'N/A')
                regions = ", ".join(v_det.get('regions', []))
                text += f"  • `{v}` ({regions}) - ARB: {arb_display} {status_icon}\n    MD5: `{md5}`\n"
        text += "\n"
        
    if len(found_models) > 10:
        text += f"_...and {len(found_models)-10} more models._\n"
        
    await update.message.reply_text(text, parse_mode="Markdown")

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    data = await fetch_database()
    if not data:
        msg = "❌ Failed to fetch database."
        if is_callback:
            await update.callback_query.message.reply_text(msg)
        else:
            await update.message.reply_text(msg)
        return
        
    all_fw = []
    for model, details in data.items():
        dev_name = details.get('device_name', model)
        for v_name, v_det in details.get('versions', {}).items():
            if v_det.get('status') == 'current':
                # Use a default old date if first_seen is missing to push it to the bottom
                first_seen = v_det.get('first_seen') or '2000-01-01'
                all_fw.append((first_seen, dev_name, v_name, v_det))
                
    # Sort by first_seen (descending), then by version name (descending) as tie breaker
    all_fw.sort(key=lambda x: (x[0], x[2]), reverse=True)
    
    text = "🔥 **Latest Discovered Firmwares:**\n\n"
    for first_seen, dev_name, v_name, v_det in all_fw[:5]:
        is_hardcoded = v_det.get('is_hardcoded', False)
        if is_hardcoded:
            arb_display = "?"
            status_icon = "⚠️"
        else:
            arb = v_det.get('arb', '?')
            arb_display = arb
            status_icon = "🟢" if arb == 0 else "🔴"
        
        regions = ", ".join(v_det.get('regions', []))
        
        date_str = ""
        if first_seen != '2000-01-01':
            date_str = f" 📅 `{first_seen}`"
            
        text += f"📱 *{dev_name}*\n  • `{v_name}` ({regions}) - ARB: {arb_display} {status_icon}{date_str}\n\n"
        
    if is_callback:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")

# --- Device Resolution Helpers ---
# Device metadata mappings (embedded from config.py for bot autonomy)
DEVICE_METADATA = {
    "15": {"name": "OnePlus 15", "models": {"GLO": "CPH2747", "EU": "CPH2747", "IN": "CPH2745", "CN": "PLK110"}},
    "15R": {"name": "OnePlus 15R", "models": {"GLO": "CPH2769", "EU": "CPH2769", "IN": "CPH2767"}},
    "13": {"name": "OnePlus 13", "models": {"GLO": "CPH2653", "EU": "CPH2653", "IN": "CPH2649", "NA": "CPH2655", "CN": "PJZ110"}},
    "13R": {"name": "OnePlus 13R", "models": {"GLO": "CPH2645", "EU": "CPH2645", "IN": "CPH2691"}},
    "12": {"name": "OnePlus 12", "models": {"GLO": "CPH2581", "EU": "CPH2581", "IN": "CPH2573", "NA": "CPH2583", "CN": "PJD110"}},
    "12R": {"name": "OnePlus 12R", "models": {"GLO": "CPH2609", "EU": "CPH2609", "IN": "CPH2585", "NA": "CPH2611"}},
    "11": {"name": "OnePlus 11", "models": {"GLO": "CPH2449", "EU": "CPH2449", "IN": "CPH2447", "NA": "CPH2451"}},
    "11R": {"name": "OnePlus 11R", "models": {"IN": "CPH2487"}},
    "10 Pro": {"name": "OnePlus 10 Pro", "models": {"GLO": "NE2213", "EU": "NE2213", "IN": "NE2211", "NA": "NE2215", "CN": "NE2210"}},
    "10T": {"name": "OnePlus 10T", "models": {"GLO": "CPH2415", "EU": "CPH2415", "IN": "CPH2413", "NA": "CPH2417"}},
    "9 Pro": {"name": "OnePlus 9 Pro", "models": {"NA": "LE2125", "EU": "LE2123", "IN": "LE2121"}},
    "9": {"name": "OnePlus 9", "models": {"NA": "LE2115", "EU": "LE2113", "IN": "LE2111"}},
    "Open": {"name": "OnePlus Open", "models": {"EU": "CPH2551", "IN": "CPH2551", "NA": "CPH2551"}},
    "Nord 5": {"name": "OnePlus Nord 5", "models": {"GLO": "CPH2709", "EU": "CPH2709", "IN": "CPH2707"}},
    "Nord 4": {"name": "OnePlus Nord 4", "models": {"GLO": "CPH2663", "EU": "CPH2663", "IN": "CPH2661"}},
    "Ace 6T": {"name": "OnePlus Ace 6T", "models": {"CN": "PLR110"}},
    "Ace 6": {"name": "OnePlus Ace 6", "models": {"CN": "PLQ110"}},
    "Ace 5 Pro": {"name": "OnePlus Ace 5 Pro", "models": {"CN": "PKR110"}},
    "Ace 5": {"name": "OnePlus Ace 5", "models": {"CN": "PKG110"}},
    "Ace 3 Pro": {"name": "OnePlus Ace 3 Pro", "models": {"CN": "PJX110"}},
    "Ace 3V": {"name": "OnePlus Ace 3V", "models": {"CN": "PJF110"}},
    "Ace 3": {"name": "OnePlus Ace 3", "models": {"CN": "PJE110"}},
    "Pad 3": {"name": "OnePlus Pad 3", "models": {"GLO": "OPD2415", "EU": "OPD2415"}},
    "Pad 2 Pro": {"name": "OnePlus Pad 2 Pro", "models": {"CN": "OPD2413"}},
    "Pad 2": {"name": "OnePlus Pad 2", "models": {"GLO": "OPD2403", "EU": "OPD2403", "IN": "OPD2403"}},
}

OOS_MAPPING = {
    "15": "oneplus_15", "15R": "oneplus_15r",
    "13": "oneplus_13", "13R": "oneplus_13r",
    "12": "oneplus_12", "12R": "oneplus_12r",
    "11": "oneplus_11", "11R": "oneplus_11r",
    "10 Pro": "oneplus_10_pro", "10T": "oneplus_10t",
    "9 Pro": "oneplus_9_pro", "9": "oneplus_9",
    "Open": "oneplus_open",
    "Nord 5": "oneplus_nord_5", "Nord 4": "oneplus_nord_4",
    "Ace 6T": "oneplus_ace_6t", "Ace 6": "oneplus_ace_6",
    "Ace 5": "oneplus_ace_5", "Ace 5 Pro": "oneplus_ace_5_pro",
    "Ace 3 Pro": "oneplus_ace_3_pro", "Ace 3V": "oneplus_ace_3v", "Ace 3": "oneplus_ace_3",
    "Pad 3": "oneplus_pad_3", "Pad 2": "oneplus_pad_2", "Pad 2 Pro": "oneplus_pad2_pro",
}

# Springer API (roms.danielspringer.at) for CN variants
SPRINGER_API_URL = "https://roms.danielspringer.at/index.php?view=ota"
SPRING_MAPPING = {
    "oneplus_15": "OP 15", "oneplus_15r": "OP 15R",
    "oneplus_13": "OP 13", "oneplus_13r": "OP 13R",
    "oneplus_12": "OP 12", "oneplus_12r": "OP ACE 3",
    "oneplus_11": "OP 11", "oneplus_11r": "OP 11R",
    "oneplus_10_pro": "OP 10 PRO",
    "oneplus_ace_6t": "OP ACE 6T", "oneplus_ace_6": "OP ACE 6",
    "oneplus_ace_5": "OP ACE 5", "oneplus_ace_5_pro": "OP ACE 5 PRO",
    "oneplus_ace_3_pro": "OP ACE 3 PRO", "oneplus_ace_3v": "OP ACE 3V", "oneplus_ace_3": "OP ACE 3",
    "oneplus_pad2_pro": "OP PAD2 PRO", "oneplus_pad_3": "OP PAD3", "oneplus_pad_2": "OP PAD2",
    "oneplus_open": "OP OPEN",
    "oneplus_nord_5": "OP NORD 5", "oneplus_nord_4": "OP NORD 4",
}

OOS_API_BASE = "https://oosdownloader-gui.fly.dev/api"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def resolve_device(query: str):
    """Resolve a user query (name, model number, or short ID) to a device_id and region."""
    query_lower = query.lower().strip()
    
    # Try to extract region suffix (e.g., "oneplus 15 eu")
    parts = query_lower.rsplit(" ", 1)
    region_hint = None
    search_query = query_lower
    known_regions = {"glo", "eu", "in", "na", "cn", "visible"}
    if len(parts) > 1 and parts[-1].upper() in {r.upper() for r in known_regions}:
        region_hint = parts[-1].upper()
        search_query = parts[0].strip()
    
    # 1. Try direct device_id match (e.g., "15", "13R", "Nord 4")
    for did, meta in DEVICE_METADATA.items():
        if search_query == did.lower():
            region = region_hint or next((r for r in ["GLO", "EU", "IN", "NA", "CN"] if r in meta["models"]), None)
            return did, meta["name"], region
    
    # 2. Try device name match (e.g., "oneplus 15", "oneplus nord 4")
    for did, meta in DEVICE_METADATA.items():
        if search_query in meta["name"].lower() or meta["name"].lower() in search_query:
            region = region_hint or next((r for r in ["GLO", "EU", "IN", "NA", "CN"] if r in meta["models"]), None)
            return did, meta["name"], region
    
    # 3. Try model number match (e.g., "CPH2747")
    for did, meta in DEVICE_METADATA.items():
        for reg, model in meta["models"].items():
            if search_query == model.lower():
                region = region_hint or reg
                return did, meta["name"], region
    
    return None, None, None

async def fetch_firmware_oos(device_id: str, region: str) -> dict:
    """Fetch the latest firmware download URL from OOS API."""
    mapped_id = OOS_MAPPING.get(device_id, f"oneplus_{device_id.lower().replace(' ', '_')}")
    brand = "oneplus"
    url = f"{OOS_API_BASE}/{brand}/{mapped_id}/{region}/full/info"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                if "download_url" in data and data["download_url"]:
                    return {
                        "url": data["download_url"],
                        "version": data.get("version_number", "Unknown"),
                        "md5": data.get("md5sum")
                    }
    except Exception as e:
        logging.error(f"OOS API error: {e}")
    return None

async def fetch_firmware_springer(device_id: str, region: str) -> dict:
    """Fetch firmware download URL from Springer API (roms.danielspringer.at). Used for CN."""
    mapped_id = OOS_MAPPING.get(device_id, f"oneplus_{device_id.lower().replace(' ', '_')}")
    springer_name = SPRING_MAPPING.get(mapped_id)
    if not springer_name:
        return None
    
    headers = {"User-Agent": USER_AGENT}
    
    try:
        async with aiohttp.ClientSession() as session:
            # Step 1: GET the page to find available versions
            async with session.get(SPRINGER_API_URL, headers=headers, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return None
                page_html = await resp.text()
            
            soup = BeautifulSoup(page_html, 'html.parser')
            device_select = soup.find('select', {'id': 'device'})
            if not device_select:
                return None
            
            devices_json = device_select.get('data-devices')
            if not devices_json:
                return None
            
            devices_data = json.loads(html_mod.unescape(devices_json))
            
            # Resolve device name (fuzzy match)
            device_name = springer_name
            if device_name not in devices_data:
                found = False
                for d in devices_data:
                    if device_name.upper() == d.upper() or d.upper().startswith(device_name.upper() + " "):
                        device_name = d
                        found = True
                        break
                if not found:
                    return None
            
            if region not in devices_data[device_name]:
                return None
            
            versions = devices_data[device_name][region]
            if not versions:
                return None
            
            found_version_name = versions[0]  # Latest version is first
            
            # Step 2: POST form to get signed URL
            form_data = {
                'device': device_name,
                'region': region,
                'version_index': '0',
            }
            post_headers = {
                'User-Agent': USER_AGENT,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': SPRINGER_API_URL,
            }
            
            async with session.post(SPRINGER_API_URL, data=form_data, headers=post_headers, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return None
                result_html = await resp.text()
            
            soup = BeautifulSoup(result_html, 'html.parser')
            result_div = soup.find('div', {'id': 'resultBox'})
            
            if result_div and result_div.get('data-url'):
                download_url = html_mod.unescape(result_div.get('data-url'))
                return {
                    "url": download_url,
                    "version": found_version_name,
                    "md5": None
                }
    except Exception as e:
        logging.error(f"Springer API error: {e}")
    return None

async def fetch_firmware_url(device_id: str, region: str) -> dict:
    """Try OOS API first, then fall back to Springer API."""
    # For CN, skip OOS and go straight to Springer
    if region != "CN":
        result = await fetch_firmware_oos(device_id, region)
        if result:
            return result
    
    # Fallback to Springer (works for CN and as backup for others)
    result = await fetch_firmware_springer(device_id, region)
    if result:
        return result
    
    # If CN failed on Springer, try OOS as last resort
    if region == "CN":
        result = await fetch_firmware_oos(device_id, region)
        if result:
            return result
    
    return None

async def download_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    """Fetch the latest firmware for a device and trigger an ARB check."""
    ALLOWED_GROUP_ID = -1003662409203
    
    if is_callback:
        msg_target = update.callback_query.message
    else:
        msg_target = update.message
    
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_mention = f"@{user.username}" if user.username else user.first_name
    
    if not context.args and not is_callback:
        await msg_target.reply_text(
            "📥 **Download & Check Firmware**\n\n"
            "Usage: `/download <device> [region]`\n"
            "Example: `/download OnePlus 15 EU`\n\n"
            "This will fetch the latest firmware and automatically run an ARB check!",
            parse_mode="Markdown"
        )
        return
    
    if is_callback:
        await msg_target.reply_text(
            "📥 **Download & Check Firmware**\n\n"
            "Usage: `/download <device> [region]`\n"
            "Example: `/download OnePlus 15 EU`\n\n"
            "This will fetch the latest firmware and automatically run an ARB check!",
            parse_mode="Markdown"
        )
        return
    
    query = " ".join(context.args)
    device_id, device_name, region = resolve_device(query)
    
    if not device_id:
        await msg_target.reply_text(f"❌ Device not found: `{query}`\n\nTry: `/download OnePlus 15` or `/download CPH2747`", parse_mode="Markdown")
        return
    
    if not region:
        await msg_target.reply_text(f"❌ No region found for {device_name}. Try: `/download {device_name} EU`", parse_mode="Markdown")
        return
    
    # Send a status message
    status_msg = await msg_target.reply_text(
        f"🔍 Fetching latest firmware for **{device_name}** ({region})...",
        parse_mode="Markdown"
    )
    
    # Fetch firmware URL from OOS API
    firmware = await fetch_firmware_url(device_id, region)
    
    if not firmware:
        await status_msg.edit_text(
            f"❌ Could not fetch firmware for **{device_name}** ({region}).\n"
            f"The OOS API may not have this device/region.\n\n"
            f"💡 Try manually: [OOS Downloader](https://oosdownloader-gui.fly.dev/)",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return
    
    fw_url = firmware["url"]
    fw_version = firmware["version"]
    
    await status_msg.edit_text(
        f"✅ Found firmware for **{device_name}** ({region})\n"
        f"📦 Version: `{fw_version}`\n"
        f"🚀 Triggering ARB check...",
        parse_mode="Markdown"
    )
    
    # Trigger GitHub Actions workflow (same as /check)
    message_id = update.message.message_id
    message_thread_id = update.effective_message.message_thread_id
    request_chat_id = str(chat_id)
    if message_thread_id:
        request_chat_id = f"{chat_id}_{message_thread_id}"
    
    record_check(user.id, user_mention)
    success = await trigger_github_workflow(fw_url, request_chat_id, message_id, user_mention, status_msg.message_id)
    
    if success:
        await status_msg.edit_text(
            f"✅ ARB check started for **{device_name}** ({region})\n"
            f"📦 Version: `{fw_version}`\n"
            f"⏳ Waiting for GitHub Actions runner...",
            parse_mode="Markdown"
        )
        # Send a separate message with the download link (won't be deleted by workflow)
        message_thread_id = update.effective_message.message_thread_id
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📥 **Direct firmware download link:**\n[{device_name} ({region}) - {fw_version}]({fw_url})",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            message_thread_id=message_thread_id
        )
    else:
        record_error()
        await status_msg.edit_text(
            f"❌ Failed to trigger ARB check for **{device_name}**.\n"
            f"You can try `/check` manually.",
            parse_mode="Markdown"
        )
        message_thread_id = update.effective_message.message_thread_id
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📥 **Direct firmware download link:**\n[{device_name} ({region}) - {fw_version}]({fw_url})",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            message_thread_id=message_thread_id
        )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != ADMIN_USER_ID:
        return
        
    if not context.args:
        await update.message.reply_text("❌ Usage: /broadcast <message>")
        return
        
    message = " ".join(context.args)
    ALLOWED_GROUP_ID = -1003662409203
    try:
        await context.bot.send_message(
            chat_id=ALLOWED_GROUP_ID,
            text=f"📢 **Announcement**\n\n{message}",
            parse_mode="Markdown"
        )
        if update.effective_chat.id != ALLOWED_GROUP_ID:
            await update.message.reply_text("✅ Broadcast sent successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to send broadcast: {e}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Configuration
    ALLOWED_GROUP_ID = -1003662409203

    chat_id = update.effective_chat.id
    user = update.effective_user
    user_id = user.id
    user_mention = f"@{user.username}" if user.username else user.first_name

    # 0. Rate Limiting
    now = time.time()
    user_requests[user_id] = [t for t in user_requests[user_id] if now - t < RATE_LIMIT_WINDOW]
    
    if len(user_requests[user_id]) >= RATE_LIMIT_COUNT:
        wait_time = int(RATE_LIMIT_WINDOW - (now - user_requests[user_id][0]))
        await update.message.reply_text(f"⚠️ Rate limit exceeded. Please wait {wait_time} seconds before making another request.")
        return
    
    user_requests[user_id].append(now)

    # 1. Restrict DMs
    if update.effective_chat.type == 'private':
        await update.message.reply_text(f"❌ DM checks are not allowed.\nPlease use the group: https://t.me/oneplusarbchecker")
        return

    # 2. Strict Group Check
    if chat_id != ALLOWED_GROUP_ID:
        await update.message.reply_text(f"❌ This bot is only authorized for the OnePlus ARB Checker group.")
        return

    if not context.args:
        try:
            await update.message.delete()
        except Exception as e:
            logging.error(f"Failed to delete message: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{user_mention}, ❌ Usage: /check https://..."
        )
        return

    firmware_url = context.args[0].strip('<>')
    
    # URL Validation
    if not firmware_url.startswith(("http://", "https://")) or " " in firmware_url:
        try:
            await update.message.delete()
        except Exception as e:
            logging.error(f"Failed to delete message: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{user_mention}, ❌ Invalid URL format.\nUsage: /check https://example.com/firmware.zip"
        )
        return

    # Record stats
    record_check(user_id, user_mention)

    message_id = update.message.message_id
    message_thread_id = update.effective_message.message_thread_id

    # Dynamic Thread Handling
    request_chat_id = str(chat_id)
    if message_thread_id:
        request_chat_id = f"{chat_id}_{message_thread_id}"

    # Reply immediately
    status_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=f"🚀 Initiating check...",
        message_thread_id=message_thread_id,
        reply_to_message_id=message_id
    )

    # Trigger GitHub Action
    success = await trigger_github_workflow(firmware_url, request_chat_id, message_id, user_mention, status_msg.message_id)

    if success:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text=f"✅ Check started! Waiting for GitHub Actions runner..."
        )
    else:
        record_error()
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text=f"❌ Failed to trigger GitHub Action. Check logs/credentials."
        )

async def trigger_github_workflow(url, chat_id, message_id, user_mention, status_message_id):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
    }
    data = {
        "ref": "main",
        "inputs": {
            "firmware_url": url,
            "request_chat_id": str(chat_id),
            "request_message_id": str(message_id),
            "request_user_name": user_mention,
            "request_status_message_id": str(status_message_id)
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{WORKFLOW_ID}/dispatches",
                headers=headers,
                json=data,
                timeout=30
            ) as response:
                
                if response.status == 204:
                    logging.info("Workflow triggered successfully.")
                    return True
                else:
                    text = await response.text()
                    logging.error(f"Failed to trigger workflow: {response.status} {text}")
                    return False
            
    except Exception as e:
        logging.error(f"Network error triggering workflow: {e}")
        return False


if __name__ == '__main__':
    if not TELEGRAM_BOT_TOKEN or not GITHUB_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN and GITHUB_PAT environment variables must be set.")
        exit(1)

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('check', check))
    application.add_handler(CommandHandler('stats', stats))
    application.add_handler(CommandHandler('help', help_cmd))
    application.add_handler(CommandHandler('about', about))
    
    # New commands
    application.add_handler(CommandHandler('devicestatus', status_cmd))
    application.add_handler(CommandHandler('latest', latest))
    application.add_handler(CommandHandler('download', download_cmd))
    application.add_handler(CommandHandler('broadcast', broadcast))
    
    # Callback Query Handler for Inline Keyboards
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.add_error_handler(error_handler)
    
    print(f"Bot v{BOT_VERSION} is running...")
    application.run_polling(poll_interval=1.0, timeout=30)
