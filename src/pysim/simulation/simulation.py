from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.events.event import Event
from pysim.simulation.events.movement import TurnLeftEvent, ForwardEvent, BackwardEvent


class Simulation:
    __position: Vector
    __orientation: Orientation

    def __init__(self, position: Vector, orientation: Orientation):
        self.__position = position
        self.__orientation = orientation

    def forward(self) -> Event:
        old_position = self.__position
        self.__position += Vector.from_orientation(self.__orientation)
        event = ForwardEvent(old_position, self.__orientation)
        return event

    def backward(self) -> Event:
        old_position = self.__position
        self.__position -= Vector.from_orientation(self.__orientation)
        event = BackwardEvent(old_position, self.__orientation)
        return event

    def turn_left(self) -> Event:
        event = TurnLeftEvent(self.__position, self.__orientation)
        self.__orientation = self.__orientation.turn_left()
        return event
