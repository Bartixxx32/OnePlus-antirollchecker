import logging
import os
import json
import requests
import time
from collections import defaultdict
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

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
                chat_info = f"\n📍 Chat: `{update.effective_chat.id}`"
            if update.effective_user:
                user_info = f"\n👤 User: {update.effective_user.first_name} (`{update.effective_user.id}`)"
        
        admin_msg = (
            f"🚨 *Bot Error Alert*\n\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"{chat_info}{user_info}\n\n"
            f"❌ `{error_text[:500]}`"
        )
        await context.bot.send_message(chat_id=ADMIN_USER_ID, text=admin_msg, parse_mode="Markdown")
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
        text="Hello! Send /check <firmware_url> to analyze a firmware file."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available commands and usage."""
    msg = (
        "🤖 *OnePlus ARB Checker Bot*\n\n"
        "*Available Commands:*\n\n"
        "🔍 /check `<url>` — Analyze a firmware file\n"
        "   _Send a direct download link to a OnePlus firmware .zip_\n\n"
        "ℹ️ /about — Bot info, version & uptime\n"
        "❓ /help — Show this message\n\n"
        "*How it works:*\n"
        "1. Send /check with a firmware URL\n"
        "2. Bot triggers analysis via GitHub Actions\n"
        "3. Status updates appear in real-time\n"
        "4. Results are posted as a reply\n\n"
        "📋 _Rate limit: 2 checks per minute_"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

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
        [f"  {i+1}. {u[1]['name']} — {u[1]['count']}" for i, u in enumerate(sorted_users)]
    ) or "  No data yet"
    
    msg = (
        f"📊 *Bot Statistics*\n\n"
        f"🔢 Total checks: *{data.get('total_checks', 0)}*\n"
        f"❌ Total errors: *{data.get('total_errors', 0)}*\n"
        f"📅 Today: *{today_count}*\n"
        f"📆 Since: {data.get('first_check', 'N/A')}\n\n"
        f"👥 *Top Users:*\n{top_users_text}"
    )
    
    await update.message.reply_text(msg, parse_mode="Markdown")

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
        await update.message.reply_text("❌ Usage: /check <firmware_url>")
        return

    firmware_url = context.args[0]
    
    # URL Validation
    if not firmware_url.startswith(("http://", "https://")) or " " in firmware_url:
        await update.message.reply_text("❌ Invalid URL. Please provide a valid Direct Download Link starting with http:// or https://")
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
    status_msg = await update.message.reply_text(f"🚀 Initiating check...", reply_to_message_id=message_id)

    # Trigger GitHub Action
    success = trigger_github_workflow(firmware_url, request_chat_id, message_id, user_mention, status_msg.message_id)

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

def trigger_github_workflow(url, chat_id, message_id, user_mention, status_message_id):
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
        response = requests.post(
            f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{WORKFLOW_ID}/dispatches",
            headers=headers,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        
        if response.status_code == 204:
            logging.info("Workflow triggered successfully.")
            return True
        else:
            logging.error(f"Failed to trigger workflow: {response.status_code} {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
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
    
    application.add_error_handler(error_handler)
    
    print(f"Bot v{BOT_VERSION} is running...")
    application.run_polling(poll_interval=1.0, timeout=30)
