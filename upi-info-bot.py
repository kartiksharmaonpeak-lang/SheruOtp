import logging, html, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "apna-token-lga-ke-run karna nhi to tum bologe kam nhi kar raha hai"
API_URL = "https://dg-drift-apis.onrender.com/upi-info"
API_KEY = "dg"

logging.basicConfig(level=logging.INFO)
WAITING_FOR_UPI = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Wᴇʟᴄᴏᴍᴇ, {user.full_name}!\n"
        "💳 UPI Iɴғᴏ Bᴏᴛ\n"
        "📩 Sᴇɴᴅ Yᴏᴜʀ UPI ID\n"
        "E.xᴀᴍᴘʟᴇ: drift@upi\n"
        "━─━────༺༻────━─━ 🔎"
    )
    return WAITING_FOR_UPI


async def fetch_upi_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    upi_id = update.message.text.strip()

    if "@" not in upi_id:
        await update.message.reply_text("❌ Iɴᴠᴀʟɪᴅ UPI ID. E.xᴀᴍᴘʟᴇ: name@bank")
        return WAITING_FOR_UPI

    msg = await update.message.reply_text("⏳ Pʟᴇᴀsᴇ Wᴀɪᴛ • 📡 Vᴇʀɪғʏɪɴɢ Uᴘɪ Dᴇᴛᴀɪʟs...")

    try:
        r = requests.get(API_URL, params={"key": API_KEY, "upi": upi_id}, timeout=20)
        r.raise_for_status()
        result = r.json()
    except Exception:
        await msg.edit_text("⚠️ API Eʀʀᴏʀ. Tʀʏ Aɢᴀɪɴ Lᴀᴛᴇʀ.")
        return ConversationHandler.END

    if not result.get("success"):
        await msg.edit_text("❌ API Eʀʀᴏʀ. Cʜᴇᴄᴋ UPI ID.")
        return ConversationHandler.END

    d = result.get("data", {})
    c = result.get("credit", {})
    owner = html.escape(c.get("owner", "@DG_DRIFT"))

    if not d.get("valid"):
        await msg.edit_text(
            "━─━────༺༻────━─━\n\n"
            "❌ Uᴘɪ Iɴғᴏ Nᴏᴛ Fᴏᴜɴᴅ\n\n"
            f"💳 Uᴘɪ: <code>{html.escape(d.get('upi', upi_id))}</code>\n"
            f"📡 Sᴛᴀᴛᴜs: <code>{html.escape(d.get('status', 'failed'))}</code>\n\n"
            "━─━────༺༻────━─━\n"
            f"👑 Oᴡɴᴇʀ: {owner}\n"
            "━─━────༺༻────━─━",
            parse_mode="HTML",
        )
        return ConversationHandler.END

    text = (
        "━─━────༺༻────━─━\n\n"
        "✅ Uᴘɪ Iɴғᴏ Fᴏᴜɴᴅ\n\n"
        f"👤 Nᴀᴍᴇ: <code>{html.escape(d.get('account_holder', 'N/A'))}</code>\n"
        f"💳 Uᴘɪ: <code>{html.escape(d.get('upi', upi_id))}</code>\n"
        f"🏦 Aᴄᴄᴏᴜɴᴛ: <code>{html.escape(d.get('account_type', 'N/A'))}</code>\n"
        f"🏛️ Bᴀɴᴋ: <code>{html.escape(d.get('bank', 'N/A'))}</code>\n"
        f"🏪 Mᴇʀᴄʜᴀɴᴛ: <code>{'Yes' if d.get('is_merchant') else 'No'}</code>\n"
        f"✔️ Vᴀʟɪᴅ: <code>{'Yes' if d.get('valid') else 'No'}</code>\n"
        f"📱 Vᴘᴀ: <code>{html.escape(d.get('raw_response', {}).get('recipientVpa', 'N/A'))}</code>\n"
        f"📡 Sᴛᴀᴛᴜs: <code>{html.escape(d.get('status', 'N/A'))}</code>\n\n"
        "━─━────༺༻────━─━\n"
        f"👑 Oᴡɴᴇʀ: {owner}\n"
        "━─━────༺༻────━─━"
    )
    await msg.edit_text(text, parse_mode="HTML")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Cᴀɴᴄᴇʟʟᴇᴅ.")
    return ConversationHandler.END


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={WAITING_FOR_UPI: [MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_upi_info)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    ))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()