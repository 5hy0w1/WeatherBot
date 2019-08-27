from requests import Session
from PIL import Image, ImageDraw, ImageFont


class YandexAPI(Session):

    def __init__(self, api_key):
        super().__init__()
        self.headers['X-Yandex-API-Key'] = api_key

    def _get_weather(self, lat, lon):
        url = f"https://api.weather.yandex.ru/v1/informers?lat={lat}&lon={lon}&lang=ru_RU"
        response = self.get(url)
        if response.ok:
            return response.json()
        else:
            return False

    def human(self, json):
        return f"""Температура: {json['fact']['temp']}\nСкорость ветра:{json['fact']['wind_speed']}"""


def make_img(week_day, date, temp, condition, wind_speed, background, wind_icon, save):
    img = Image.open(background)
    draw = ImageDraw.Draw(img)
    icon = Image.open(wind_icon)
    font = ImageFont.truetype('arial.ttf', 48)
    big = ImageFont.truetype('arial.ttf', 120)
    draw.text((110, 140), '       ' + week_day + '\n' + date + '\n ' + condition, 'white', font=font)
    draw.text((155, 290), temp + '°', 'white', font=big)
    draw.text((200, 420), wind_speed + "м/с", font=font)
    img.paste(icon, (110, 420), mask=icon)
    img.save(f'{save}.png')


#make_img('Пн', "27 августа", '16', 'солнечно', '2', "./imgs/backgrounds/clear1.png", './imgs/icons/wind.png')
