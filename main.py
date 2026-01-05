import telebot
import google.generativeai as genai
import os

# Kalitlarni Koyeb tizimidan olamiz
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Foydalanuvchi limitlari
users_limit = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men Gemini AI yordamida ishlaydigan SMM yordamchiman. Mavzuni yozing!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    count = users_limit.get(user_id, 0)

    if count >= 3:
        bot.reply_to(message, "Sizning bugungi bepul limitingiz tugadi. VIP obuna uchun admin bilan bog'laning: @admin_username")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    try:
        prompt = f"Ijtimoiy tarmoq uchun kreativ o'zbekcha post yoz: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
        users_limit[user_id] = count + 1
    except:
        bot.reply_to(message, "Xatolik yuz berdi. API kalitni tekshiring.")

bot.polling(none_stop=True)
