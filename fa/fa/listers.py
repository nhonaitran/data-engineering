"""Flight listers module."""

from .finders import FlightFinder


class FlightLister:

    def __init__(self, flight_finder: FlightFinder):
        self._flight_finder = flight_finder

    def flights_depart_from(self, airport):
        return [
            flight for flight in self._flight_finder.find_all()
            if flight.origin == airport
        ]

    def flights_arrive_at(self, airport):
        return [
            flight for flight in self._flight_finder.find_all()
            if flight.destination == airport
        ]
