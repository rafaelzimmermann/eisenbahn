# -*- coding: utf-8 -*-
import requests
import json
import time

from threading import Thread
from threading import Lock

RHEINBAHN_URL = 'https://haltestellenmonitor.vrr.de/backend/app.php/api/stations/table'
REQUEST_TIMEOUT_SECONDS = 5
UPDATE_INTERVAL = 60

lock = Lock()
last_train_time_data = None
last_update = None


def align_text(text, max_len):
    text += " " * (max_len - len(text))
    return text

def align_text_right(text, max_len):
    text = " " * (max_len - len(text)) + text
    return text

class TrainTableRequestError(Exception):
    pass

class TrainTimeFetcher(Thread):

    def __init__(self, config):
        Thread.__init__(self)
        self.query_params = config

    def _request_next_departures(self):
        try:
            response = requests.post(RHEINBAHN_URL, data=self.query_params, timeout=REQUEST_TIMEOUT_SECONDS)
        except Exception:
            raise TrainTableRequestError()

        if response.status_code != 200:
            raise TrainTableRequestError("Request Status Code:" + str(response.status_code))
        return response.json()["departureData"]

    def run(self):
        global last_train_time_data
        global last_update
        while True:
            result = None
            try:
                result = self._request_next_departures()
            except Exception as e:
                print("Failed to fetch train time table." + str(e))
                result = "Failed!"

            lock.acquire()
            last_train_time_data = result
            last_update = time.time()
            lock.release()

            time.sleep(UPDATE_INTERVAL)



class TrainTimeTable():

    def __init__(self, config):
        self.train_time_fetcher = TrainTimeFetcher(config)
        self.train_time_fetcher.daemon = True
        self.train_time_fetcher.start()

    def _get_next_train_list(self):
        global last_train_time_data
        lines = []
        if last_train_time_data is None:
            return lines
        for item in last_train_time_data:
            line = []
            line.append(item["lineNumber"])
            line.append(item["direction"])
            line.append(str(item["countdown"]))
            lines.append(line)
        return lines

    def fetch_formated_next_departures(self, max_line_size=16):
        global last_update
        lock.acquire()
        lines = self._get_next_train_list()
        if last_update is None or len(lines) == 0:
            lock.release()
            return "No data."
        update_elapsed_time = time.time() - last_update
        lock.release()
        first_col_max_len = 3
        last_col_max_len = 2
        unit_size = 1
        text = ""
        index = 0
        for line in lines:
            text += align_text(line[0][:first_col_max_len], first_col_max_len) + " "
            text += align_text_right(line[2][:last_col_max_len], last_col_max_len) + "m"
            if index % 2 > 0:
                text += "\n"
            else:
                text += "  "
            index+=1
        if update_elapsed_time > UPDATE_INTERVAL:
            text = "OUTDATED\n" + text

        if len(text) == 0:
            text = "No data."

        return text


if __name__ == '__main__':
    import sys
    config_file = sys.argv[1] if len(sys.argv) == 2 else "config.json"
    with open(config_file) as f:
        config = json.loads(f.read())
        train_time_table = TrainTimeTable(config["trainTime"])
        print(train_time_table.fetch_formated_next_departures(max_line_size=30).encode('utf-8'))
        time.sleep(UPDATE_INTERVAL + 10)
        print(train_time_table.fetch_formated_next_departures(max_line_size=30).encode('utf-8'))
