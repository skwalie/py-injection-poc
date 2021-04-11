

class Application(object):
    def __init__(self, processor_array, logger):
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



