import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# 🔹 توکن ربات
TOKEN = "8169426404:AAGo7RX86y1lhglVLSu8HDRlP6D4X2mcfLY"
bot = telebot.TeleBot(TOKEN)

# 🔹 لینک پرداخت شما در زرین پال
ZARINPAL_LINK = "https://zarinp.al/676109"

# ✅ ایجاد منوی اصلی
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_buy = KeyboardButton("📖 خرید داستان نرگس")
    btn_verify = KeyboardButton("✅ تأیید پرداخت")
    markup.add(btn_buy, btn_verify)
    return markup

# ✅ دستور /start برای نمایش منو
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "سلام! لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=main_menu())

# ✅ ارسال دکمه پرداخت
@bot.message_handler(func=lambda message: message.text == "📖 خرید داستان نرگس")
def send_payment_button(message):
    markup = InlineKeyboardMarkup()
    btn_pay = InlineKeyboardButton("💳 پرداخت 500,000 ریال", url=ZARINPAL_LINK)
    markup.add(btn_pay)
    bot.send_message(message.chat.id, "💳 برای خرید، روی دکمه زیر کلیک کنید و پرداخت را انجام دهید.\nپس از پرداخت، کد پیگیری را ارسال کنید.", reply_markup=markup)

# ✅ تأیید پرداخت و ارسال PDF
@bot.message_handler(func=lambda message: message.text == "✅ تأیید پرداخت")
def ask_for_transaction_code(message):
    bot.send_message(message.chat.id, "📌 لطفاً **کد پیگیری تراکنش** خود را ارسال کنید.")

@bot.message_handler(func=lambda message: message.text.isdigit())  # بررسی اینکه پیام فقط عدد باشد
def verify_payment(message):
    CONFIRMED_PAYMENTS = ["123456", "789012"]  # لیست کدهای تستی
    if message.text in CONFIRMED_PAYMENTS:
        with open("narges.pdf", "rb") as pdf:
            bot.send_document(message.chat.id, pdf, caption="📖 پرداخت تأیید شد! این هم داستان نرگس. 🎉")
    else:
        bot.send_message(message.chat.id, "❌ کد وارد شده معتبر نیست! لطفاً کد صحیح را ارسال کنید.")

# ✅ اجرای ربات
bot.polling(none_stop=True)