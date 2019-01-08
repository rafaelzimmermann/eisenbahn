import os
import time
import RPi.GPIO as GPIO

from traintime import TrainTimeTable
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

def update_traintime():
    global last_update
    global text
    if last_update is None:
        last_update = time.time()
        text = train_time_table.fetch_formated_next_departures()
    else:
        elapsed =  time.time() - last_update
        if elapsed > 60:
            last_update = time.time()
            text = train_time_table.fetch_formated_next_departures()

index = 0
display_line_size = 2
while True:
    update_traintime()
    lines = text.split("\n")
    for i in range(0, len(lines) - 1):
        os.system('clear')
        print(lines[i])
        lcd.clear()
        lcd.home()
        lcd.write(lines[i])
        if len(lines) > i:
            print(lines[i + 1])
            lcd.nextline()
            lcd.write(lines[i + 1])
            time.sleep(UPDATE_INTERVAL / (len(lines) * 2))
