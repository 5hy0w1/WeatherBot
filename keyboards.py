from telebot.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
get_loaction_button = KeyboardButton("Отправить геолокацию", request_location=True)
start_keyboard.add(get_loaction_button)
