# telegram_bot.py
# -----------------------
from telegram.ext import Updater, CommandHandler
import requests

TOKEN = "PUT-YOUR-TELEGRAM-BOT-TOKEN-HERE"   # ← توکن ربات
API_URL = "https://YOUR-REPLIT-APP-URL/aqi"  # ← لینک API که ساختی

def start(update, context):
    update.message.reply_text("سلام! برای گرفتن شاخص آلودگی هوای تهران بنویس /aqi")

def get_aqi(update, context):
    try:
        r = requests.get(API_URL)
        data = r.json()

        if "error" in data:
            update.message.reply_text("❌ خطا در دریافت اطلاعات")
            return

        aqi = data["aqi"]
        status = data["status"]

        msg = f"""
📍 *شاخص کیفیت هوای تهران*
AQI: *{aqi}*
وضعیت: *{status}*
        """
        update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        update.message.reply_text("❌ خطا در اتصال به سرور")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("aqi", get_aqi))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
