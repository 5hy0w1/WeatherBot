import telebot
import keyboards
import messages
import time
import pickle
import os.path
import datetime
from weather_api import YandexAPI, make_img
from settings import *


bot = telebot.TeleBot(TOKEN)
weather = YandexAPI(WEATHER_TOKEN)
users = {}
weekdays = ['Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
monthes = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


@bot.message_handler(commands="start")
def start(message):
    client_id = message.from_user.id
    users[client_id] = {'location': None, 'lang': 'Ru', 'last_request': None}
    bot.send_message(client_id,
                     messages.start,
                     reply_markup=keyboards.start_keyboard)


@bot.message_handler(content_types=["location"])
def update_location(message):
    users[message.from_user.id]['location'] = message.location
    bot.send_message(message.from_user.id, messages.location_added)
    bot.send_message(message.from_user.id, f"lon: {message.location.longitude}\nlat: {message.location.latitude}")


@bot.message_handler(commands=['weather'])
def send_weather(message):
    client_id = message.from_user.id
    last_request = users[client_id]['last_request']
    now = time.time()
    if not last_request or (now - last_request) > API_REQUESTS_FREQUENCY:
        lat = users[client_id]['location'].latitude
        lon = users[client_id]['location'].longitude
        current = weather._get_weather(lat, lon)
        date = datetime.datetime.now()
        if current['fact']['condition'] in ['clear', 'partly-cloudy']:
            background = "./imgs/backgrounds/clear1.png"
        else:
            background = "./imgs/backgrounds/cloudy.jpg"
        make_img(weekdays[date.weekday()],
                 f'{date.day} {monthes[date.month - 1]}',
                 str(current['fact']['temp']),
                 current['fact']['condition'],
                 str(current['fact']['wind_speed']),
                 background,
                 "./imgs/icons/wind.png",
                 client_id)
        with open(f'{client_id}.png', 'rb') as file:
            bot.send_photo(client_id, file)
        users[client_id]['last_request'] = now
    else:
        bot.send_message(client_id, messages.requests_too_frequent)


try:
    if os.path.exists(DUMP_FILE_PATH):
        with open(DUMP_FILE_PATH, 'rb') as file:
            data = pickle.load(file)
            if type(data) == dict:
                users = data

    bot.polling(1, 0, 0)
except Exception:
    with open(DUMP_FILE_PATH, 'wb') as file:
        pickle.dump(users, file)
