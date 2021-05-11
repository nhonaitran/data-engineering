"""Containers module."""

from dependency_injector import containers, providers
from . import finders, listers, entities


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    flight = providers.Factory(entities.Flight)

    csv_finder = providers.Singleton(
        finders.CsvFlightFinder,
        flight_factory=flight.provider,
        path=config.finder.csv.path,
        delimiter=config.finder.csv.delimiter,
    )

    sqlite_finder = providers.Singleton(
        finders.SqliteFlightFinder,
        flight_factory=flight.provider,
        path=config.finder.sqlite.path,
    )

    finder = providers.Selector(
        config.finder.type,
        csv=csv_finder,
        sqlite=sqlite_finder,
    )

    lister = providers.Factory(
        listers.FlightLister,
        flight_finder=finder,
    )
