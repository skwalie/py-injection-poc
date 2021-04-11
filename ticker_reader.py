import json
import requests
from configuration import TickerReaderConfiguration


class TickerReader(object):
    def read(self):
        pass


class TickerFileReader(TickerReader):
    def __init__(self, path: str):
        self._path = path

    def read(self):
        with open(self._path, "r") as read_file:
            return json.load(read_file)


class TickerHttpReader(TickerReader):
    def __init__(self, cfg: TickerReaderConfiguration):
        self._url = cfg.service_url

    def read(self):
        response = requests.get(self._url)
        return response.json()
