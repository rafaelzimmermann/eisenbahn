import os
import time

from multiprocessing import Process, Queue
from traintime import TrainTimeTable, TrainTableRequestError
from progressbar import ProgressBar
from weather.weather import Weather

MESSAGE_ERROR_DISPLAY_DURATION = 10

def initiate_lcd():
    from lcd import LCD
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    lcd = LCD(8, 10, 12, 16, 18, 22)

    lcd.begin(16,2)
    time.sleep(0.5)
    return lcd

def create_weather_chars(lcd):
    lcd.create_char()


class Einsenbahn():

    def __init__(self, lcd, train_time_service, weather_service):
        self.lcd = lcd
        self.train_time_service = train_time_service
        self.progress_bar = ProgressBar(lcd)
        self.weather = weather_service

    def display_error_message(self):
        self.lcd.clear()
        self.lcd.home()
        self.lcd.write("Failed to update")
        self.lcd.nextline()
        self.lcd.write("Retrying")
        time.sleep(MESSAGE_ERROR_DISPLAY_DURATION)

    def display_text(self, lines, duration):
        if len(lines) > 0:
            self.lcd.clear()
            self.lcd.home()
            self.lcd.write(lines.pop(0))
            if len(lines) > 0:
                self.lcd.nextline()
                self.lcd.write(lines[0])
        time.sleep(duration)
        if len(lines) > 2:
            self.display_text(lines, duration)

    def display_time_table(self):
        try:
            self.progress_bar.start()
            text = self.train_time_service.fetch_formated_next_departures()
            self.progress_bar.stop()
            for i in range(1):
                lines = text.split("\n")
                lines_display_duration = 15 / (len(lines) / 2)
                self.display_text(lines, duration=lines_display_duration)
        except Exception as e:
            print(e)
            self.progress_bar.stop()
            self.display_error_message()

    def display_weather(self):
        self.progress_bar.start()
        try:
            text = self.weather.get_formated_forecast()
            self.progress_bar.stop()
            lines = text.split("\n")
            self.display_text(lines, duration=10)
        except Exception as e:
            print(e)
            self.progress_bar.stop()
            self.display_error_message()


def main(lcd):
    import json
    eisenbahn = None
    with open('config.json') as config_file:
        config = json.loads(config_file.read())
        train_time_service = TrainTimeTable(config["trainTime"])
        weather_service = Weather(config["weather"])
        eisenbahn = Einsenbahn(lcd, train_time_service, weather_service)

    while True:
        eisenbahn.display_time_table()
        eisenbahn.display_weather()


if __name__ == '__main__':
    main(initiate_lcd())
