import openai
import telebot
import datetime
from telebot import types

openai.api_key = "TOKEN"
bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, добро пожаловать в ChatGPT бота. Задай мне любой вопрос и получи мгновенный ответ!\n💎 Наши боты:\n@kodex_shop_bot - Наш магазин\n@kodex_vpn_bot - Наш VPN-бот\n@kodex_file_bot - Наш файлообменник")

excluded_users = [5117455510]

user_requests = {}
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    if user_id not in excluded_users:
        if user_id not in user_requests:
            user_requests[user_id] = {"count": 0, "last_request": datetime.date.today()}
        today = datetime.date.today()
        if today > user_requests[user_id]["last_request"]:
            user_requests[user_id] = {"count": 0, "last_request": today}
        if user_requests[user_id]["count"] >= 15:
            bot.reply_to(message, "Вы исчерпали лимит запросов. Попробуйте завтра.")
            return
        user_requests[user_id]["count"] += 1
    bot.reply_to(message, "Запрос отправлен")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.text,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    bot.reply_to(message, response["choices"][0]["text"])
    
bot.polling()

