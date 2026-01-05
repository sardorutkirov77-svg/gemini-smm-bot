import telebot
import google.generativeai as genai
import os

# Koyeb sozlamalaridan kalitlarni olish
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Gemini-ni eng barqaror model bilan sozlash
genai.configure(api_key=GEMINI_KEY)
# Bu yerda model nomini barqaror versiyaga o'zgartirdik
model = genai.GenerativeModel('gemini-pro') 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Gemini AI yordamida ishlaydigan SMM yordamchingizman. Savolingizni yozing!")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

bot.infinity_polling()
