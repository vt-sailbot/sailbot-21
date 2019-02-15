from abc import ABC, abstractmethod
from enum import Enum
from pubsub import pub


class AirmarBroadcasterType(Enum):
    Testable = 0,
    Messanger = 1


class AirmarBroadcaster(ABC):
    """An abstract class to hide the interface required to notify the rest of the system of airmar input events.
    Messages are async to prevent them from blocking eachother, since RC input may need a high priority."""

    @abstractmethod
    def read_wind_speed(self, wind_speed=None):
        """Broadcasts the average wind speed recorded by airmar.

        Keyword arguments:
        wind_speed -- The wind speed in meters.
        """
        pass

    @abstractmethod
    def read_wind_heading(self, wind_head=None):
        """Broadcasts the average wind heading recorded by airmar.

        Keyword arguments:
        wind_head -- The wind heading in degrees.
        """
        pass

    @abstractmethod
    def read_boat_latitude(self, boat_lat=None):
        """Broadcasts the boat's latitude recorded by airmar.

        Keyword arguments:
        boat_lat -- The boat's latitude.
        """
        pass

    @abstractmethod
    def read_boat_longitude(self, boat_long=None):
        """Broadcasts the boat's longitude recorded by airmar.

        Keyword arguments:
        boat_long -- The boat's longitude.
        """
        pass

    @abstractmethod
    def read_boat_heading(self, boat_head=None):
        """Broadcasts the boat's heading recorded by airmar.

        Keyword arguments:
        boat_head -- The boat's heading in degrees.
        """
        pass

    @abstractmethod
    def read_boat_speed(self, boat_speed=None):
        """Broadcasts the boat's speed recorded by airmar.

        Keyword arguments:
        boat_speed -- The boat's speed in meters
        """
        pass


class TestableAirmarBroadcaster(AirmarBroadcaster):
    """ A broadcaster built to test methods that need to broadcast."""

    def __init__(self):
        self.wind_speeds = []
        self.wind_heads = []
        self.boat_lats = []
        self.boat_heads = []
        self.boat_speeds = []

    def read_wind_speed(self, wind_speed=None):
        if wind_speed is not None:
            self.wind_speeds.append(wind_speed)

    def read_wind_heading(self, wind_head=None):
        if wind_head is not None:
            self.wind_heads.append(wind_head)

    def read_boat_latitude(self, boat_lat=None):
        if boat_lat is not None:
            self.boat_lats.append(boat_lat)

    def read_boat_heading(self, boat_head):
        if boat_head is not None:
            self.boat_heads.append(boat_head)

    def read_boat_speeds(self, boat_speed):
        if boat_speed is not None:
            self.boat_speeds.append(boat_speed)


class AirmarMessenger(AirmarBroadcaster):
    """Implements an interface with the pub/sub messaging system to broadcast airmar data."""

    def read_wind_speed(self, wind_speed=None):
        if wind_speed is not None:
            pub.sendMessage("set wind speed", wind_speed)

    def read_wind_heading(self, wind_head=None):
        if wind_head is not None:
            pub.sendMessage("set wind heading", wind_head)

    def read_boat_latitude(self, boat_lat=None):
        if boat_lat is not None:
            pub.sendMessage("set boat latitude", boat_lat)

    def read_boat_heading(self, boat_head=None):
        if boat_head is not None:
            pub.sendMessage("set boat heading", boat_head)

    def read_boat_speed(self, boat_speed=None):
        if boat_speed is not None:
            pub.sendMessage("set boat speed", boat_speed)


def make_broadcaster(broadcaster_type=AirmarBroadcasterType.Messenger):
    """Creates a new, implementation-relevant AirmarBroadcaster.

    Implements the factory pattern.

    Keyword arguments:
    broadcaster_type -- The type of broadaster to create

    Returns:
    The correct AirmarBroadcaster for the environment.
    """
    if broadcaster_type == AirmarBroadcasterType.Messenger:
        return AirmarMessenger()

    return TestableAirmarBroadcaster()
