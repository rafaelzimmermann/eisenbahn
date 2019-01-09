# -*- coding: utf-8 -*-
import time

from threading import Thread, Event

def center_text(columns, text):
    spaces = " " * ((columns - len(text)) / 2)
    return spaces + text + spaces

class ProgressBarAnimationThread(Thread):

    def __init__(self, lcd, *args):
        Thread.__init__(self)
        self.lcd = lcd
        self.stop_event = Event()

    def run(self):
        bar = chr(255) + chr(255) + chr(255)
        loading_text = center_text(self.lcd.cols, "LOADING")
        while not self.stop_event.is_set():
            for index in range(0, self.lcd.cols - len(bar)):
                self.lcd.clear()
                self.lcd.home()
                self.lcd.write(loading_text)
                self.lcd.nextline()
                self.lcd.write((index * " ") + bar)
                time.sleep(0.3)
                if self.stop_event.is_set():
                    return
            for index in range(len(bar), self.lcd.cols):
                self.lcd.clear()
                self.lcd.home()
                self.lcd.write(loading_text)
                self.lcd.nextline()
                self.lcd.write(((self.lcd.cols - index) * " ") + bar)
                time.sleep(0.3)
                if self.stop_event.is_set():
                    return

    def stop(self):
        self.stop_event.set()


class ProgressBar():

    def __init__(self, lcd):
        self.lcd = lcd
        self.animation_thread = None

    def start(self):
        if self.animation_thread is not None:
            return
        self.animation_thread = ProgressBarAnimationThread(self.lcd)
        self.animation_thread.start()

    def stop(self):
        self.animation_thread.stop()
        self.animation_thread.join()
        self.animation_thread = None
        self.lcd.clear()
