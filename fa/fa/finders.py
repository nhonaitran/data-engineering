"""Movie finders module."""

import csv
import logging
import sqlite3
from typing import Callable, List

from .entities import Flight


class FlightFinder:

    def __init__(self, flight_factory: Callable[..., Flight]) -> None:
        self._flight_factory = flight_factory

    def find_all(self) -> List[Flight]:
        """Fetch flights matching criteria"""
        raise NotImplementedError()


class CsvFlightFinder(FlightFinder):

    def __init__(
            self,
            flight_factory: Callable[..., Flight],
            path: str,
            delimiter: str,
    ) -> None:
        self._csv_file_path = path
        self._delimiter = delimiter
        super().__init__(flight_factory)

    def find_all(self) -> List[Flight]:
        with open(self._csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
            return [self._flight_factory(*row) for row in csv_reader]

class SqliteFlightFinder(FlightFinder):

    def __init__(
            self,
            flight_factory: Callable[..., Flight],
            path: str,
    ) -> None:
        self._database = sqlite3.connect(path)
        super().__init__(flight_factory)

    def find_all(self) -> List[Flight]:
        with self._database as db:
            rows = db.execute('SELECT flight_id, origin, destination FROM flights')
            return [self._flight_factory(*row) for row in rows]


