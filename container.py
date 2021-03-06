from dependency_injector import providers, containers
from ticker_reader import TickerHttpReader
from configuration import Configuration
from data_store import MongoStore
from data_frame_provider import CursorDataFrameProvider
from logger import DefaultLogger


class Container(containers.DeclarativeContainer):
    cfg = Configuration()
    logger = providers.Singleton(DefaultLogger)
    ticker_reader = providers.Singleton(TickerHttpReader, cfg.ticker_reader())
    data_store = providers.Singleton(MongoStore, cfg.data_store())
    data_frame_provider = providers.Singleton(CursorDataFrameProvider)
