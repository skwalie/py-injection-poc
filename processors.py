from data_store import DataStore
from datetime import datetime
from ticker_reader import TickerReader
from data_frame_provider import DataFrameProvider
from logger import Logger

import mapper


class Processor(object):
    def execute(self, subject):
        pass


class ProcessorDecorator(Processor):
    def __init__(self, decorated: Processor):
        self.instance = decorated

    def execute(self, subject):
        return self.instance.execute(subject)


class TimeWatchProcessDecorator(ProcessorDecorator):
    def __init__(self, decorated: Processor, logger: Logger):
        super().__init__(decorated)
        self._log = logger

    def execute(self, subject):
        start_time = datetime.now()
        result = super().execute(subject)
        diff = datetime.now() - start_time
        self._log.info(type(self.instance).__name__ + " spent " + str(diff) + " to run")
        return result


class GetTickersProcessor(Processor):
    def __init__(self, ticker_reader: TickerReader):
        self._ticker_reader = ticker_reader

    def execute(self, subject):
        return self._ticker_reader.read()


class WriteSeriesProcessor(Processor):
    def __init__(self, data_store: DataStore):
        self._data_store = data_store

    def execute(self, subject):
        mapped = mapper.map_ticker(subject)
        self._data_store.insert(mapped, "tickers")
        return subject


class ReadDataFrameProcessor(Processor):
    def __init__(self, data_store: DataStore, data_frame_provider: DataFrameProvider):
        self._data_store = data_store
        self._data_frame_provider = data_frame_provider

    def execute(self, subject):
        series = self._data_store.get_collection("tickers")
        return self._data_frame_provider.get_frame(series)


class ExcelExportProcessor(Processor):
    def __init__(self, export_format: int, data_frame_provider: DataFrameProvider):
        self._export_format = export_format
        self._data_frame_provider = data_frame_provider

    def execute(self, subject):
        file_name = "output/" + \
                    str(datetime.utcnow()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")

        self._data_frame_provider.save(subject, file_name, self._export_format)
        return subject
