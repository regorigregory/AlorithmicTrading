from abc import ABC, abstractmethod
from __future__ import annotations
import pandas as pd
from AbstractClasses.ObserverPattern import Subject
import time


class RequestParamsFormatter(ABC):

    def __init__(self, interval_formatter, period_formatter, tick_name_formatter):
        self._interval_formatter = interval_formatter
        self._period_formatter = period_formatter
        self._tick_formatter = tick_name_formatter

    def _get_interval_formatted(self, time_in_millis) -> dict(str, str):
        return self._interval_formatter(time_in_millis)

    def _get_period_formatted(self, epoch_start, epoch_end) -> dict(str, str):
        return self._period_formatter(epoch_start, epoch_end)

    def _get_tick_formatted(self) -> dict(str, str):
        return self._tick_formatter()

    def get_request_params(self, epoch_start, epoch_end, time_in_millis):
        return {**self._get_period_formatted(time_in_millis),
                **self._get_interval_formatted(epoch_start, epoch_end),
                **self._get_tick_formatted()}


class DataFetcher(ABC):
    def __init__(self, data_formatter: RequestParamsFormatter, interval_in_millis, number_of_intervals):
        self._formatter = data_formatter
        self._interval_in_millis = interval_in_millis
        self._number_of_intervals = number_of_intervals
    @abstractmethod
    def get_request_params(self):
        pass

    @abstractmethod
    def perform_request(self):
        pass

    def get_data(self, now):
        params = self._formatter.get_request_params(now,
                                                    now-self._interval_in_millis*self._number_of_intervals,
                                                    self._interval_in_millis)
        self.perform_request(**params)


class PriceReporter(ABC, Subject):
    def __init__(self, data_fetcher: DataFetcher, update_interval=60):
        super(Subject, self).__init__()
        self._fetcher = data_fetcher
        self._update_interval = update_interval

    def get_data(self, time_in_millis=int(time.now()*100)):
        return self._fetcher(time_in_millis)

    def start_automatic_data_retrieval(self):
        while True:
            data = self.get_data()
            self.notify(data)
            time.sleep(self._update_interval)
