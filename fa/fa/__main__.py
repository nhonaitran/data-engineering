"""
Main module.
"""
import sys
import logging

from dependency_injector.wiring import inject, Provide

from .listers import FlightLister
from .containers import Container


@inject
def main(lister: FlightLister = Provide[Container.lister]) -> None:
    """
    Main entry point for fa (flights-analytics).
    """
    logging.info('Flights depart from KHOU:')
    for flight in lister.flights_depart_from('KHOU'):
        logging.info(f"\t-{flight}")

    logging.info('Flights arrive at KIWS:')
    for flight in lister.flights_arrive_at('KIWS'):
        logging.info(f"\t-{flight}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)8s: (%(threadName)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    container = Container()
    container.config.from_yaml('config.yml')
    container.config.finder.type.from_env('FLIGHT_FINDER_TYPE')
    container.wire(modules=[sys.modules[__name__]])

    main()
