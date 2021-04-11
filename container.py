from dependency_injector import providers, containers
from ticker_reader import TickerHttpReader
from configuration import Configuration
from data_store import MongoStore
from data_frame_provider import CursorDataFrameProvider
from config_reader import JsonConfigReader
from logger import Logger


class Container(containers.DeclarativeContainer):
    cfg = Configuration(JsonConfigReader())
    logger = providers.Factory(Logger)
    ticker_reader = providers.Singleton(TickerHttpReader, cfg.ticker_reader())
    data_store = providers.Singleton(MongoStore, cfg.data_store())
    data_frame_provider = providers.Singleton(CursorDataFrameProvider)
