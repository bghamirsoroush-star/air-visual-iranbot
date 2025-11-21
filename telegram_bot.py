from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

TOKEN = "PUT-YOUR-BOT-TOKEN"
API_URL = "https://YOUR-SERVER-IP:5000/aqi"   # لینک API خودت

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دریافت شاخص آلودگی هوا دستور /aqi را بزن.")

async def get_aqi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get(API_URL, timeout=10)
        data = r.json()

        now = data.get("now", {})
        daily = data.get("daily", {})

        text = f"""
📍 *شاخص کیفیت هوای تهران*

🌬 شاخص لحظه‌ای: *{now.get('aqi')}*
📌 وضعیت: {now.get('status')}

🕒 شاخص ۲۴ ساعته: *{daily.get('aqi')}*
📌 وضعیت ۲۴ ساعته: {daily.get('status')}
"""
        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("❌ خطا در دریافت اطلاعات از سرور")

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aqi", get_aqi))

    print("Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
