import json


def is_time_to_send(time, time_to_send):
    return get_formatted_time(time) == time_to_send


def is_on_the_hour(time):
    minute = time.minute
    second = time.second

    return minute == 00 and second == 00


def is_on_the_second(time):
    return time.second == 00


def get_formatted_time(time):
    return time.strftime("%H:%M:%S")


class JsonFile:

    def __init__(self, file_dir):
        self.file = open(file_dir)
        self.json_file = json.load(self.file)
        self.file.close()

    def get_key(self, key):
        return self.json_file[key]
