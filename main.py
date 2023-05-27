import os
import math
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import key_api


bot = Bot(token=key_api.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем.
async def start_command (message: types.Message):
   await message.reply("City name?")

@dp.message_handler()
async def get_weather (message: types.Message):
   try:
      ans = message.text
      response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={ans}&lang=ru&units=metric&APPID={key_api.API_OpenW}")
      data = response.json()
      city = data["name"]
      cur_temp = data["main"]["temp"]
      humidity = data["main"]["humidity"]
      pressure = data["main"]["pressure"]
      wind = data["wind"]["speed"]
      wind_deg = data["wind"]["deg"]
      country = data["sys"]["country"]
      print(ans)
      sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
      sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
      length_of_the_day = sunset_timestamp - sunrise_timestamp

      code_wind = {
         "0" : "northerly",
         "90" : "easterly ",
         "180" : "southerly ",
         "270" : "westerly "
      }

      code_to_smile = {
         "Clear": "Ясно \U00002600",
         "Clouds": "Облачно \U00002601",
         "Rain": "Дождь \U00002614",
         "Drizzle": "Дождь \U00002614",
         "Thunderstorm": "Гроза \U000026A1",
         "Snow": "Снег \U0001F328",
         "Mist": "Туман \U0001F32B"
      }

      weather_description = data["weather"][0]["main"]

      if weather_description in code_to_smile:
         wd = code_to_smile[weather_description]

      else:
         # если эмодзи для погоды нет, выводим другое сообщение
         wd = "Посмотри в окно, я не понимаю, что там за погода..."

      if str(wind_deg) in code_wind:
         win_d = code_wind[wind_deg]
      elif (wind_deg > 0) and (wind_deg < 90):
         win_d = "С/В"
      elif (wind_deg > 90) and (wind_deg < 180):
         win_d = "Ю/В"
      elif (wind_deg > 180) and (wind_deg < 270):
         win_d = "Ю/З"
      elif (wind_deg > 270) and (wind_deg < 360):
         win_d = "С/З"
      else:
         win_d = "ветер неизвестного направления"

      await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                          f"Погода в городе: {city} ({country})\n"
                          f"Температура: {cur_temp}°C {wd}\n"
                          f"Влажность: {humidity}%\n"
                          f"Давление: {math.ceil(pressure / 1.333)} мм.рт.ст\n"
                          f"Ветер: {wind} м/с  {win_d} ({wind_deg} deg)\n"
                          f"Восход солнца: {sunrise_timestamp}\n"
                          f"Закат солнца: {sunset_timestamp}\n"
                          f"Продолжительность дня: {length_of_the_day}\n"
                          f"Хорошего дня!")

   except:
      await message.reply("FAIL city name")

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)

