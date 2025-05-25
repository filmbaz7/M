import logging
import sqlite3
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

app = Flask(__name__)

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def fetch_discounts():
    url = "https://www.jdsports.ir/"  # لینک صفحه تخفیف‌ها رو درست بذار
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    discounts = []
    for product in soup.find_all(class_="product"):
        title_tag = product.find(class_="product-title")
        discount_tag = product.find(class_="discount")

        if title_tag and discount_tag:
            title = title_tag.text.strip()
            discount_text = discount_tag.text.strip()
            try:
                discount_percent = int(discount_text.replace("% OFF", "").strip())
                if discount_percent > 30:
                    discounts.append((title, discount_percent))
            except:
                continue
    return discounts

def save_discounts_to_db(discounts):
    conn = sqlite3.connect("discounts.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS discounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            discount INTEGER
        )
    ''')
    c.execute('DELETE FROM discounts')
    c.executemany('INSERT INTO discounts (product_name, discount) VALUES (?, ?)', discounts)
    conn.commit()
    conn.close()

def discounts_command(update, context):
    discounts = fetch_discounts()
    save_discounts_to_db(discounts)
    if not discounts:
        context.bot.send_message(chat_id=update.effective_chat.id, text="هیچ تخفیف بالای ۳۰ درصدی پیدا نشد.")
        return

    msg = "تخفیف‌های بالای ۳۰٪ سایت JD Sports:\n\n"
    for title, discount in discounts:
        msg += f"{title}: {discount}% تخفیف\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

dispatcher.add_handler(CommandHandler("discounts", discounts_command))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return "OK", 200
    else:
        abort(403)

@app.route("/")
def index():
    return "JD Sports Discount Telegram Bot is running!"

if __name__ == "__main__":
    # برای توسعه محلی میتونی بدون SSL اجرا کنی، ولی برای وب‌هوک روی سرور باید HTTPS باشه
    app.run(host="0.0.0.0", port=5000)
