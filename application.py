from dependency_injector.wiring import inject, Provide
from data_frame_provider import DataFrameProvider
from ticker_reader import TickerReader
from data_store import DataStore
from container import Container
from logger import Logger
import processors


class Application(object):
    @inject
    def __init__(self, processor_array, logger: Logger = Provide[Container.logger]):
        self._processors = processor_array or []
        self._log = logger
        self._result = {}

    def run(self):
        self._log.info("Processing...")
        for processor in self._processors:
            self._process_and_log(processor)

        return self._result

    def _process_and_log(self, caller):
        self._log.info("calling: " + type(caller).__name__)
        self._log.debug("input : " + str(self._result))
        self._result = caller.execute(self._result)
        self._log.info("called: " + type(caller).__name__)
        self._log.debug("output : " + str(self._result))


RET_OK = 0
RET_ERROR = -1


@inject
def run_ticker_reader(
        log: Logger = Provide[Container.logger],
        ticker_reader: TickerReader = Provide[Container.ticker_reader],
        data_store: DataStore = Provide[Container.data_store]):

    app = Application(
        [
            processors.TimeWatchProcessDecorator(processors.GetTickersProcessor(ticker_reader), log),
            processors.FormatToSeriesProcessor(),
            processors.WriteSeriesProcessor(data_store)
        ])

    try:
        result = app.run()
        print(result)
        log.info("Successful execution !")
        exit(RET_OK)
    except FileNotFoundError as fnf_err:
        log.error("File not found: " + str(fnf_err))
        exit(RET_ERROR)
    except IOError as io_err:
        log.error("IO error: " + str(io_err))
        exit(RET_ERROR)
    except Exception as e_err:
        log.error("Undefined error: " + str(e_err))
        exit(RET_ERROR)


@inject
def run_data_frame_export(
        export_format: int,
        log: Logger = Provide[Container.logger],
        data_store: DataStore = Provide[Container.data_store],
        data_frame_provider: DataFrameProvider = Provide[Container.data_frame_provider]):

    app = Application(
        [
            processors.ReadDataFrameProcessor(data_store, data_frame_provider),
            processors.ExcelExportProcessor(export_format, data_frame_provider)
        ])

    try:
        result = app.run()
        print(result)
        log.info("Successful execution !")
        exit(RET_OK)
    except Exception as e_err:
        log.error("Undefined error: " + str(e_err))
        exit(RET_ERROR)
