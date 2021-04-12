import unittest
from unittest.mock import Mock
import main


class MainTests(unittest.TestCase):
    def setUp(self):
        self._logger_mock = Mock()
        self._ticker_reader_mock = Mock()
        self._data_store_mock = Mock()
        self._sut = main

    def test_run_ticker_reader_when_ticker_is_returned_then_it_should_be_saved_in_datastore(self):
        self._data_store_mock.insert = Mock()
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

        result = self._sut.run_ticker_reader(self._ticker_reader_mock, self._data_store_mock, self._logger_mock)

        self.assertEqual(0, result)
        self._data_store_mock.insert.assert_called_once()

    def test_run_ticker_reader_when_an_exception_is_thrown_then_datastore_insert_should_not_be_called(self):
        self._data_store_mock.insert = Mock()
        self._ticker_reader_mock.read.side_effect = IOError

        result = self._sut.run_ticker_reader(self._ticker_reader_mock, self._data_store_mock, self._logger_mock)

        self.assertEqual(-1, result)
        self._data_store_mock.insert.assert_not_called()

