# -*- coding: utf-8 -*-
import requests
import json

RHEINBAHN_URL = 'https://haltestellenmonitor.vrr.de/backend/app.php/api/stations/table'

def align_text(text, max_len):
    text += " " * (max_len - len(text))
    return text

class TrainTableRequestError(Exception):
    pass

class TrainTimeTable():

    def __init__(self, config_file):
        with open(config_file) as file:
            self.query_params = json.loads(file.read())

    def _request_next_departures(self):
        try:
            response = requests.post(RHEINBAHN_URL, data=self.query_params)
        except Exception:
            raise TrainTableRequestError()

        if response.status_code != 200:
            raise TrainTableRequestError("Request Status Code:" + str(response.status_code))
        return response.json()["departureData"]

    def _get_next_train_list(self):
        departures = self._request_next_departures()
        lines = []
        for item in departures:
            line = []
            if item["countdown"] < 60:
                line.append(item["lineNumber"])
                line.append(item["direction"])
                line.append(str(item["countdown"]) if item["countdown"] > 0 else "sofort")
                lines.append(line)
        return lines

    def fetch_formated_next_departures(self, max_line_size=16):
        lines = self._get_next_train_list()
        first_col_max_len = 3
        last_col_max_len = 2
        unit_size = 3
        middle_col_size = max_line_size - (last_col_max_len + first_col_max_len + unit_size + 2)
        text = ""
        for line in lines:
            text += align_text(line[0][:first_col_max_len], first_col_max_len) + " "
            text += align_text(line[1][:middle_col_size], middle_col_size) + " "
            if line[2] == "sofort":
                text += line[2]
            else:
                text += align_text(line[2][:last_col_max_len], last_col_max_len) + "min"
            text += "\n"
        return text


if __name__ == '__main__':
    import sys
    config_file = sys.argv[1] if len(sys.argv) == 2 else "config.json"
    print(config_file)
    train_time_table = TrainTimeTable(config_file)
    print(train_time_table.fetch_formated_next_departures(max_line_size=30).encode('utf-8'))
