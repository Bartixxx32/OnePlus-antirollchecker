#!/usr/bin/env python3
import argparse
import requests
import sys

def send_telegram_message(token, chat_id, message, reply_to=None, message_thread_id=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    if message_thread_id:
        payload["message_thread_id"] = message_thread_id

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        sys.exit(1)

def delete_telegram_message(token, chat_id, message_id):
    url = f"https://api.telegram.org/bot{token}/deleteMessage"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Telegram message {message_id} deleted successfully.")
    except Exception as e:
        print(f"Failed to delete Telegram message: {e}")
        # Do not exit with error, as deletion is secondary

def escape_markdown(text):
    """Helper to escape Markdown special characters."""
    if not text:
        return text
    # Escape characters that have special meaning in Markdown
    # We are using "Markdown" (V1) mode, which is less strict than V2 but still sensitive to _, *, `
    escape_chars = ['_', '*', '`', '[', ']']
    for char in escape_chars:
        text = text.replace(char, f"\\{char}")
    return text

def main():
    parser = argparse.ArgumentParser(description="Send Telegram notification for new firmware.")
    parser.add_argument("--token", required=True, help="Telegram Bot Token")
    parser.add_argument("--chat-id", required=True, help="Telegram Chat ID")
    parser.add_argument("--device", required=True, help="Device Name")
    parser.add_argument("--variant", help="Device Variant (Optional)")
    parser.add_argument("--version", required=True, help="Firmware Version")
    parser.add_argument("--arb", required=True, help="ARB Index")
    parser.add_argument("--md5", help="MD5 Checksum")
    parser.add_argument("--url", help="Download URL")
    
    # New arguments for interactive bot
    parser.add_argument("--reply-to", help="Message ID to reply to")
    parser.add_argument("--user-mention", help="User name to mention (e.g. @username)")
    parser.add_argument("--delete-message-id", help="Message ID to delete after sending")

    # Extended metadata
    parser.add_argument("--product", help="Product Name")
    parser.add_argument("--security-patch", help="Security Patch Level")
    parser.add_argument("--build-id", help="Build ID")
    
    # Error handling
    parser.add_argument("--error", help="Error message to send instead of result")

    args = parser.parse_args()

    # Parse chat_id for thread_id
    chat_id = args.chat_id
    message_thread_id = None
    if "_" in chat_id:
        try:
            parts = chat_id.rsplit("_", 1)
            if len(parts) == 2:
                chat_id = parts[0]
                message_thread_id = parts[1]
        except:
            pass

    # Construct the message
    message = ""
    # Mention is usually a username/link, we don't escape it strictly or we break it?
    # User mention @username works in Markdown. If user name has underscores... usually handled by Telegram?
    # Let's escape user mention just in case if it's not a link.
    # Actually @username is safe. content like "Hello @user_name" works.
    
    if args.user_mention:
        message += f"Hello {args.user_mention}, "
    
    if args.error:
        # Error message usually plain text, but let's escape just in case
        safe_error = escape_markdown(args.error)
        message += f"an error occurred during the check:\n\n{safe_error}"
        send_telegram_message(args.token, chat_id, message, args.reply_to, message_thread_id)
        if args.delete_message_id:
            delete_telegram_message(args.token, chat_id, args.delete_message_id)
        return

    if args.user_mention:
        message += "here is your result:\n\n"

    # Escape all variable content
    safe_device = escape_markdown(args.device)
    safe_product = escape_markdown(args.product) if args.product else None
    safe_variant = escape_markdown(args.variant) if args.variant else None
    safe_version = escape_markdown(args.version)
    safe_patch = escape_markdown(args.security_patch) if args.security_patch else None
    # Build ID is used in code block, no need to escape inside code block usually, but backticks inside?
    safe_build = args.build_id.replace("`", "\\`") if args.build_id else None
    safe_arb = escape_markdown(args.arb)
    safe_md5 = args.md5 # Used in code block
    
    message += (
        f"✨ *Firmware Analysis Result* ✨\n\n"
        f"📱 *Device:* {safe_device}\n"
    )

    if safe_product:
         message += f"📦 *Product:* {safe_product}\n"

    if safe_variant:
        message += f"🌍 *Variant:* {safe_variant}\n"

    message += f"🚀 *Version:* {safe_version}\n"

    if safe_patch:
        message += f"🔒 *Security Patch:* {safe_patch}\n"
    
    if safe_build:
        message += f"🏗️ *Build ID:* `{safe_build}`\n"

    message += f"🛡️ *ARB Index:* {safe_arb}\n"

    if safe_md5:
        message += f"🔑 *MD5:* `{safe_md5}`\n"
    
    if args.url:
        # URL needs to be safe? Standard Markdown link [text](url).
        # We don't escape URL itself usually.
        message += f"\n⬇️ [Download Link]({args.url})"

    send_telegram_message(args.token, chat_id, message, args.reply_to, message_thread_id)

    if args.delete_message_id:
        delete_telegram_message(args.token, chat_id, args.delete_message_id)

if __name__ == "__main__":
    main()
