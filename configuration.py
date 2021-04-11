from config_reader import ConfigReader
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
    @inject
    def __init__(self, config_reader):
        self._options = config_reader.read_from_file("config.json")

    def get(self, name):
        return self._options[name]

    def ticker_reader(self):
        cfg = self
        return TickerReaderConfiguration(cfg)

    def data_store(self):
        cfg = self
        return MongoStoreConfiguration(cfg)

