# -*- coding: utf-8 -*-
import json
import math
import requests

from datetime import datetime


WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
ONE_DAY_SECONDS = 86400

class Weather():

    def __init__(self, weather_api_config):
        self.api_key = weather_api_config["apiKey"]
        self.city_name = weather_api_config["cityName"]
        self.country_code = weather_api_config["countryCode"]
        self.units = weather_api_config["units"]

    def get_forecast(self):
        params = {
            "q": self.city_name + "," + self.country_code,
            "units": self.units,
            "APPID": self.api_key
        }

        response = requests.get(WEATHER_API_URL, params=params)
        return response.json()

    def get_formated_forecast(self):
        weather_data = self.get_forecast()
        unit = u"\N{DEGREE SIGN}C"
        forecast = weather_data["list"][0]
        current_temp = math.ceil(forecast["main"]["temp"])

        text = forecast["weather"][0]["description"].upper()
        text += " " + str(int(current_temp)) + unit + " "
        return text


if __name__ == "__main__":
    import sys
    with open("config.json") as config_file:
        config = json.loads(config_file.read())
        weather = Weather(config["weather"])
        print(weather.get_formated_forecast())
