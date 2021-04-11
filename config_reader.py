import json


class ConfigReader(object):
    def read_from_file(self, filename):
        pass


class JsonConfigReader(ConfigReader):
    def read_from_file(self, filename):
        with open(filename) as config_file:
            return json.load(config_file)
