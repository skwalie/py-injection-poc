import json
from dependency_injector.wiring import inject, Provide


class TickerReaderConfiguration(object):
    def __init__(self, cfg):
        self.service_url = cfg.get("tickerServiceUrl")


class MongoStoreConfiguration(object):
    def __init__(self, cfg):
        self.connection_string = cfg.get("mongoConnectionString")
        self.port = int(cfg.get("mongoPort"))
        self.db_name = cfg.get("mongoDbName")


class Configuration(object):
    def __init__(self):
        with open("config.json") as config_file:
            self._options = json.load(config_file)

    def get(self, name):
        return self._options[name]

    def ticker_reader(self):
        cfg = self
        return TickerReaderConfiguration(cfg)

    def data_store(self):
        cfg = self
        return MongoStoreConfiguration(cfg)

