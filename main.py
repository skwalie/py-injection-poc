import sys
from application import Application
from ticker_reader import TickerFileReader
from dependency_injector import providers
from dependency_injector.wiring import inject, Provide
from data_frame_provider import DataFrameProvider
from ticker_reader import TickerReader
from data_store import DataStore
from container import Container
from logger import Logger
import processors


RET_OK = 0
RET_ERROR = -1


@inject
def run_ticker_reader(
        ticker_reader: TickerReader = Provide[Container.ticker_reader],
        data_store: DataStore = Provide[Container.data_store],
        log: Logger = Provide[Container.logger]):

    ticker_app = Application(
        [
            processors.TimeWatchProcessDecorator(processors.GetTickersProcessor(ticker_reader), log),
            processors.WriteSeriesProcessor(data_store)
        ],
        log)

    try:
        result = ticker_app.run()
        print(result)
        log.info("Successful execution !")
        return RET_OK
    except FileNotFoundError as fnf_err:
        log.error("File not found: " + str(fnf_err))
        return RET_ERROR
    except IOError as io_err:
        log.error("IO error: " + str(io_err))
        return RET_ERROR
    except Exception as e_err:
        log.error("Undefined error: " + str(e_err))
        return RET_ERROR


@inject
def run_data_frame_export(
        export_format: int,
        data_store: DataStore = Provide[Container.data_store],
        data_frame_provider: DataFrameProvider = Provide[Container.data_frame_provider],
        log: Logger = Provide[Container.logger]):

    data_frame_app = Application(
        [
            processors.ReadDataFrameProcessor(data_store, data_frame_provider),
            processors.ExcelExportProcessor(export_format, data_frame_provider)
        ],
        log)

    try:
        result = data_frame_app.run()
        print(result)
        log.info("Successful execution !")
        return RET_OK
    except Exception as e_err:
        log.error("Undefined error: " + str(e_err))
        return RET_ERROR


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    logger = container.logger()

    if len(sys.argv) == 3:
        if sys.argv[1] == "E" and sys.argv[2].isdigit():
            logger.info("Starting export (" + str(sys.argv) + ")")
            exit(run_data_frame_export(int(sys.argv[2])))

        if sys.argv[1] == "F":
            with container.ticker_reader.override(providers.Factory(TickerFileReader, sys.argv[2])):
                logger.info("Starting read from file (" + str(sys.argv) + ")")
                exit(run_ticker_reader())

    # default operation
    elif len(sys.argv) == 1:
        logger.info("Starting read from http service (" + str(sys.argv) + ")")
        exit(run_ticker_reader())
    else:
        logger.warning("Bad parameters:" + str(sys.argv))
        print("Bad parameters -> Usage: main.py  [F optional_json_file_path] | [E optional_export_format]")
        print("export format: 0 = excel, 1 = csv")

    exit(0)


