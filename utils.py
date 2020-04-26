import json


class JsonFile:

    def __init__(self, file_dir):
        self.file = open(file_dir)
        self.json_file = json.load(self.file)
        self.file.close()

    def get_key(self, key):
        return self.json_file[key]