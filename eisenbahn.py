import os
import time
import RPi.GPIO as GPIO

from multiprocessing import Process, Queue
from traintime import TrainTimeTable, TrainTableRequestError
from progressbar import ProgressBar
from lcd import LCD

UPDATE_INTERVAL = 60
last_update = None
text = ""

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

lcd = LCD(8, 10, 12, 16, 18, 22)

lcd.begin(16,2)
time.sleep(0.5)

train_time_table = TrainTimeTable("config.json")
progress_bar = ProgressBar(lcd)

def display_error_message():
    lcd.clear()
    lcd.home()
    lcd.write("Failed to update")
    lcd.nextline()
    sleep(9)
    lcd.write("Retrying")
    sleep(1)

def update_traintime():
    global last_update
    global text
    if last_update is not None:
        elapsed =  time.time() - last_update
        if elapsed < UPDATE_INTERVAL:
            return
    last_update = time.time()
    try:
        progress_bar.start()
        text = train_time_table.fetch_formated_next_departures()
        progress_bar.stop()
    except TrainTableRequestError:
        progress_bar.stop()
        display_error_message()
        update_traintime()

def display_time_table():
    global text
    update_traintime()
    lines = text.split("\n")
    for i in range(0, len(lines) - 1):
        lcd.clear()
        lcd.home()
        lcd.write(lines[i])
        if len(lines) > i:
            lcd.nextline()
            lcd.write(lines[i + 1])
            time.sleep(UPDATE_INTERVAL / (len(lines) * 4))

if __name__ == '__main__':
    while True:
        display_time_table()
