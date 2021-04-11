import sys
import application as app
from container import Container
from ticker_reader import TickerFileReader
from dependency_injector import providers


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    logger = container.logger

    if len(sys.argv) == 3:
        if sys.argv[1] == "E" and sys.argv[2].isdigit():
            logger.info("Starting export (" + str(sys.argv) + ")")
            app.run_data_frame_export(int(sys.argv[2]))

        if sys.argv[1] == "F":
            with container.ticker_reader.override(providers.Factory(TickerFileReader, sys.argv[2])):
                logger.info("Starting read from file (" + str(sys.argv) + ")")
                app.run_ticker_reader()

    # default operation
    elif len(sys.argv) == 1:
        logger.info("Starting read from http service (" + str(sys.argv) + ")")
        app.run_ticker_reader()
    else:
        logger.warning("Bad parameters:" + str(sys.argv))
        print("Bad parameters -> Usage: main.py  [F optional_json_file_path] | [E optional_export_format]")
        print("export format: 0 = excel, 1 = csv")

    exit(0)
