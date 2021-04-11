import unittest
from unittest.mock import Mock
import application


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self._logger_mock = Mock()
        self._ticker_reader_mock = Mock()
        self._data_store_mock = Mock()
        self._sut = application

    def run_ticker_reader__when_ticker_is_returned_then_it_should_be_saved_in_datastore(self):
        self._ticker_reader_mock.read.return_value = {
            "time": {
                "updatedISO": "2021-04-08T13:03:00+00:00"
            },
            "bpi": {
                "USD": {
                    "rate_float": 57359.8233
                },
                "GBP": {
                    "rate_float": 41667.9538
                },
                "EUR": {
                    "rate_float": 48284.2947
                }
            }
        }
        self._sut.run_ticker_reader(self._logger_mock, self._ticker_reader_mock, self._data_store_mock)

