import logging
import os
import json
import time
import asyncio
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
BOT_VERSION = "1.1.3"
BOT_START_TIME = time.time()

# Paths
STATS_FILE = os.environ.get("STATS_FILE", "/data/stats.json")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

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

def record_dm_user(user_id, username):
    """Record a DM user in stats."""
    stats = load_stats()
    if "dm_users" not in stats:
        stats["dm_users"] = {}
    
    uid = str(user_id)
    if uid not in stats["dm_users"]:
        stats["dm_users"][uid] = {"name": username, "first_seen": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
    else:
        stats["dm_users"][uid]["name"] = username
    
    save_stats(stats)

async def delete_messages_delayed(chat_id, message_ids, delay, bot):
    await asyncio.sleep(delay)
    for msg_id in message_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass

async def reject_info_command_in_group(update, context, command_name):
    user = update.effective_user
    mention = f"@{user.username}" if user.username else user.first_name
    bot_username = context.bot.username
    warning_msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        message_thread_id=update.effective_message.message_thread_id if update.effective_message else None,
        text=f"Hello {mention}, please use informational commands like `{command_name}` in my private messages (DM): @{bot_username} to keep this group clean.",
        parse_mode="Markdown"
    )
    
    msgs_to_del = [warning_msg.message_id]
    if update.message:
        msgs_to_del.append(update.message.message_id)
    elif update.callback_query and update.callback_query.message:
        msgs_to_del.append(update.callback_query.message.message_id)
        
    asyncio.create_task(delete_messages_delayed(
        update.effective_chat.id, 
        msgs_to_del, 
        300, 
        context.bot
    ))


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
    for attempt in range(3):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(DB_URL, timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            logging.warning(f"Database fetch attempt {attempt+1} failed: {e}")
        if attempt < 2:
            await asyncio.sleep(2)
    logging.error("Failed to fetch database.json after 3 attempts.")
    return None

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📱 Device Status", callback_data="cmd_status"), InlineKeyboardButton("🔥 Latest Firmwares", callback_data="cmd_latest")],
        [InlineKeyboardButton("📥 Download Links", callback_data="cmd_download")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def is_user_allowed_in_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is allowed to use informational commands in a group."""
    if update.effective_chat.type == 'private':
        return True
    
    user_id = update.effective_user.id
    if user_id == ADMIN_USER_ID:
        return True
        
    try:
        chat_member = await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        if chat_member.status in ['administrator', 'creator']:
            return True
    except Exception as e:
        logging.warning(f"Could not fetch chat member: {e}")
        
    return False

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
                name = html_mod.escape(str(name)) if name else "Unknown"
                user_info = f"\n👤 User: {name} (<code>{update.effective_user.id}</code>)"
        
        error_text_esc = html_mod.escape(error_text[:500])
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
    user = update.effective_user
    logging.info(f"User {user.id} ({user.username}) executed /start")
    if update.effective_chat.type == 'private':
        user = update.effective_user
        user_mention = f"@{user.username}" if user.username else user.first_name
        record_dm_user(user.id, user_mention)
        await update.message.reply_text(
            "Hello! Welcome to the OnePlus ARB Checker Bot.\n"
            "You can use commands like /latest and /devicestatus directly here to avoid cluttering the main group.",
            reply_markup=get_main_keyboard()
        )
        return

    
    bot_username = context.bot.username
    keyboard = [[InlineKeyboardButton("🤖 Use Bot in DM", url=f"https://t.me/{bot_username}")]]
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        message_thread_id=update.effective_message.message_thread_id if update.effective_message else None,
        text="Hello! Send `/check https://example.com/firmware.zip` to analyze a firmware file, or use my DM for informational commands.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available commands and usage."""
    user = update.effective_user
    logging.info(f"User {user.id} ({user.username}) executed /help")
    if not await is_user_allowed_in_group(update, context):
        await reject_info_command_in_group(update, context, "/help")
        return
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
        "1. Bot resolves device name → fetches firmware URL from Oxygen Updater API\n"
        "2. Triggers ARB analysis via GitHub Actions\n"
        "3. Posts download link + ARB results as replies\n\n"
        "📋 _Rate limit: 2 checks per minute_"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    logging.info(f"User {user.id} ({user.username}) clicked button: {query.data}")
    await query.answer()
    
    if query.data == "cmd_status":
        if not await is_user_allowed_in_group(update, context):
            await reject_info_command_in_group(update, context, "Device Status button")
            return
        await query.message.reply_text("📱 Usage: /devicestatus <device_name_or_model>\nExample: /devicestatus OnePlus 12")
    elif query.data == "cmd_latest":
        if not await is_user_allowed_in_group(update, context):
            await reject_info_command_in_group(update, context, "Latest Firmwares button")
            return
        await latest(update, context, is_callback=True)
    elif query.data == "cmd_download":
        if update.effective_chat.type == 'private':
            await query.message.reply_text("❌ DM downloads are not allowed.\nPlease use the group: https://t.me/oneplusarbchecker")
            return
        await download_cmd(update, context, is_callback=True)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot info, version, and uptime."""
    user = update.effective_user
    logging.info(f"User {user.id} ({user.username}) executed /about")
    if not await is_user_allowed_in_group(update, context):
        await reject_info_command_in_group(update, context, "/about")
        return
    data = load_stats()
    uptime = format_uptime()
    
    msg = (
        f"ℹ️ *OnePlus ARB Checker Bot*\n\n"
        f"📦 *Version:* `{BOT_VERSION}`\n"
        f"⏱️ *Uptime:* {uptime}\n"
        f"🔢 *Total checks:* {data.get('total_checks', 0)}\n\n"
        f"🔗 [GitHub Repository](https://github.com/{GITHUB_REPO})\n"
        f"💬 [Support Group](https://t.me/oneplusarbchecker)\n"
        f"🌐 [OOS Downloader API](https://oosdownloader-gui.fly.dev/) (Powered by [Oxygen Updater](https://play.google.com/store/apps/details?id=com.arjanvlek.oxygenupdater))\n\n"
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
        [f"  {i+1}. {html_mod.escape(str(u[1]['name']))} — {u[1]['count']}" for i, u in enumerate(sorted_users)]
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


async def dm_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of DM subscribers (admin only)."""
    user = update.effective_user
    
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ This command is restricted to the bot admin.")
        return
    
    data = load_stats()
    dm_users = data.get("dm_users", {})
    
    if not dm_users:
        await update.message.reply_text("👥 <b>DM Subscribers:</b>\n\nNo subscribers yet.", parse_mode="HTML")
        return
        
    text = f"👥 <b>DM Subscribers ({len(dm_users)} total):</b>\n\n"
    for uid, info in dm_users.items():
        name = html_mod.escape(str(info.get('name', 'Unknown')))
        date = info.get('first_seen', 'Unknown')
        text += f"• {name} (ID: <code>{uid}</code>) - Since: {date}\n"
        
    if len(text) > 4000:
        for i in range(0, len(text), 4000):
            await update.message.reply_text(text[i:i+4000], parse_mode="HTML")
    else:
        await update.message.reply_text(text, parse_mode="HTML")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logging.info(f"User {user.id} ({user.username}) executed /devicestatus with args: {context.args}")
    if not await is_user_allowed_in_group(update, context):
        await reject_info_command_in_group(update, context, "/devicestatus")
        return
    
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id=update.effective_message.message_thread_id, text="📱 Usage: /devicestatus <device_name_or_model>\nExample: /devicestatus OnePlus 12")
        return
        
    query = " ".join(context.args).lower().strip()
    data = await fetch_database()
    if not data:
        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id=update.effective_message.message_thread_id, text="❌ Failed to fetch database. Try again later.")
        return
        
    found_models = []
    for model, details in data.items():
        if query in model.lower() or query in details.get("device_name", "").lower():
            found_models.append((model, details))
            
    if not found_models:
        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id=update.effective_message.message_thread_id, text=f"❌ No data found for '{query}'.")
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
        
    await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id=update.effective_message.message_thread_id, text=text, parse_mode="Markdown")

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    user = update.effective_user
    logging.info(f"User {user.id} ({user.username}) executed /latest (callback={is_callback})")
    if not is_callback and not await is_user_allowed_in_group(update, context):
        await reject_info_command_in_group(update, context, "/latest")
        return
    data = await fetch_database()
    if not data:
        msg = "❌ Failed to fetch database."
        if is_callback:
            await update.callback_query.message.reply_text(msg)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id=update.effective_message.message_thread_id, text=msg)
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
        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id=update.effective_message.message_thread_id, text=text, parse_mode="Markdown")

# --- Device Resolution Helpers ---
MAPPING_URL = "https://oparb.pages.dev/mapping.json"

async def fetch_mappings():
    for attempt in range(3):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(MAPPING_URL, timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            logging.warning(f"Mapping fetch attempt {attempt+1} failed: {e}")
        if attempt < 2:
            await asyncio.sleep(2)
    logging.error("Failed to fetch mapping.json after 3 attempts.")
    return None

OOS_API_BASE = "https://oosdownloader-gui.fly.dev/api"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def resolve_device(query: str, device_metadata: dict):
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
    for did, meta in device_metadata.items():
        if search_query == did.lower():
            region = region_hint or next((r for r in ["GLO", "EU", "IN", "NA", "CN"] if r in meta["models"]), None)
            return did, meta["name"], region
    
    # 2. Try device name match (e.g., "oneplus 15", "oneplus nord 4")
    for did, meta in device_metadata.items():
        if search_query in meta["name"].lower() or meta["name"].lower() in search_query:
            region = region_hint or next((r for r in ["GLO", "EU", "IN", "NA", "CN"] if r in meta["models"]), None)
            return did, meta["name"], region
    
    # 3. Try model number match (e.g., "CPH2747")
    for did, meta in device_metadata.items():
        for reg, model in meta["models"].items():
            if search_query == model.lower():
                region = region_hint or reg
                return did, meta["name"], region
    
    return None, None, None

async def fetch_firmware_oos(device_id: str, region: str, oos_mapping: dict) -> dict:
    """Fetch the latest firmware download URL from OOS API."""
    mapped_id = oos_mapping.get(device_id, f"oneplus_{device_id.lower().replace(' ', '_')}")
    brand = "oneplus"
    url = f"{OOS_API_BASE}/{brand}/{mapped_id}/{region}/full/info"
    
    for attempt in range(3):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "download_url" in data and data["download_url"]:
                            return {
                                "url": data["download_url"],
                                "version": data.get("version_number", "Unknown"),
                                "md5": data.get("md5sum")
                            }
        except Exception as e:
            logging.warning(f"OOS API error attempt {attempt+1}: {e}")
        if attempt < 2:
            await asyncio.sleep(2)
    logging.error("Failed to fetch from OOS API after 3 attempts.")
    return None

SPRINGER_API_URL = "https://roms.danielspringer.at/index.php?view=ota"

async def fetch_firmware_springer(device_id: str, region: str, oos_mapping: dict, spring_mapping: dict) -> dict:
    """Fetch firmware download URL from Springer API (roms.danielspringer.at). Used for CN."""
    mapped_id = oos_mapping.get(device_id, f"oneplus_{device_id.lower().replace(' ', '_')}")
    springer_name = spring_mapping.get(mapped_id)
    if not springer_name:
        return None
    
    headers = {"User-Agent": USER_AGENT}
    
    for attempt in range(3):
        try:
            async with aiohttp.ClientSession() as session:
                # Step 1: GET the page to find available versions
                async with session.get(SPRINGER_API_URL, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status != 200:
                        continue
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
                
                async with session.post(SPRINGER_API_URL, data=form_data, headers=post_headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status != 200:
                        continue
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
            logging.warning(f"Springer API error attempt {attempt+1}: {e}")
        if attempt < 2:
            await asyncio.sleep(2)
    logging.error("Failed to fetch from Springer API after 3 attempts.")
    return None

async def fetch_firmware_url(device_id: str, region: str, mappings: dict) -> dict:
    """Try OOS API first, then fall back to Springer API."""
    oos_mapping = mappings.get("OOS_MAPPING", {})
    spring_mapping = mappings.get("SPRING_MAPPING", {})
    
    # For CN, skip OOS and go straight to Springer
    if region != "CN":
        result = await fetch_firmware_oos(device_id, region, oos_mapping)
        if result:
            return result
    
    # Fallback to Springer (works for CN and as backup for others)
    result = await fetch_firmware_springer(device_id, region, oos_mapping, spring_mapping)
    if result:
        return result
    
    # If CN failed on Springer, try OOS as last resort
    if region == "CN":
        result = await fetch_firmware_oos(device_id, region, oos_mapping)
        if result:
            return result
    
    return None

async def download_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False):
    """Fetch the latest firmware for a device and trigger an ARB check."""
    user = update.effective_user
    args_str = context.args if context.args else []
    logging.info(f"User {user.id} ({user.username}) executed /download with args: {args_str} (callback={is_callback})")
    ALLOWED_GROUP_ID = -1003662409203
    
    if update.effective_chat.type == 'private':
        await update.message.reply_text(f"❌ DM downloads are not allowed.\nPlease use the group: https://t.me/oneplusarbchecker")
        return

    if update.effective_chat.id != ALLOWED_GROUP_ID:
        await update.message.reply_text(f"❌ This command is only authorized for the OnePlus ARB Checker group.")
        return

    if is_callback:
        msg_target = update.callback_query.message
    else:
        try:
            await update.message.delete()
        except:
            pass
        msg_target = update.message
    
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_mention = f"@{user.username}" if user.username else user.first_name
    
    if not context.args and not is_callback:
        await context.bot.send_message(
            chat_id=chat_id,
            message_thread_id=update.effective_message.message_thread_id,
            text="📥 **Download & Check Firmware**\n\n"
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
    
    mappings = await fetch_mappings()
    if not mappings:
        await context.bot.send_message(chat_id=chat_id, message_thread_id=update.effective_message.message_thread_id, text="❌ Failed to fetch mappings. Try again later.")
        return
        
    device_id, device_name, region = resolve_device(query, mappings.get("DEVICE_METADATA", {}))
    
    if not device_id:
        await context.bot.send_message(chat_id=chat_id, message_thread_id=update.effective_message.message_thread_id, text=f"❌ Device not found: `{query}`\n\nTry: `/download OnePlus 15` or `/download CPH2747`", parse_mode="Markdown")
        return
    
    if not region:
        await context.bot.send_message(chat_id=chat_id, message_thread_id=update.effective_message.message_thread_id, text=f"❌ No region found for {device_name}. Try: `/download {device_name} EU`", parse_mode="Markdown")
        return
    
    # Send a status message
    status_msg = await context.bot.send_message(
        chat_id=chat_id,
        message_thread_id=update.effective_message.message_thread_id,
        text=f"🔍 Fetching latest firmware for **{device_name}** ({region})...",
        parse_mode="Markdown"
    )
    
    # Fetch firmware URL from OOS API
    firmware = await fetch_firmware_url(device_id, region, mappings)
    
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
    user = update.effective_user
    args_str = context.args if context.args else []
    logging.info(f"User {user.id} ({user.username}) executed /check with args: {args_str}")
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
        await update.message.reply_text(f"❌ This command is only authorized for the OnePlus ARB Checker group.")
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

    try:
        await update.message.delete()
    except Exception as e:
        pass

    # Reply immediately
    status_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=f"🚀 Initiating check...",
        message_thread_id=message_thread_id
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
    
    for attempt in range(3):
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
                        resp_text = await response.text()
                        logging.warning(f"Failed to trigger workflow attempt {attempt+1}: {response.status} {resp_text}")
        except Exception as e:
            logging.warning(f"Network error triggering workflow attempt {attempt+1}: {e}")
        if attempt < 2:
            await asyncio.sleep(2)
    return False


if __name__ == '__main__':
    if not TELEGRAM_BOT_TOKEN or not GITHUB_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN and GITHUB_PAT environment variables must be set.")
        exit(1)

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('check', check))
    application.add_handler(CommandHandler('stats', stats))
    application.add_handler(CommandHandler('subs', dm_subs))
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
