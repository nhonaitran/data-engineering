"""Flight entities module."""


class Flight:
    flight_id: str = None
    origin: str = None
    destination: str = None

    def __init__(self, flight_id: str, origin: str, destination: str):
        self.flight_id = str(flight_id)
        self.origin = str(origin)
        self.destination = str(destination)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={repr(self.flight_id)}, origin={repr(self.origin)}, destination={repr(self.destination)})"
