import telebot
import google.generativeai as genai
import os

# Koyeb sozlamalaridagi (Environment variables) nomlar bilan bir xil bo'lishi shart
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram botni sozlash
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Gemini AI yordamida ishlaydigan SMM yordamchingizman. Savolingizni yozing!")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # AI dan javob olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Xatolikni foydalanuvchiga ko'rsatish
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

bot.infinity_polling()
