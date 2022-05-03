from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.events.event import Event
from pysim.simulation.events.explosion import ExplosionEvent
from pysim.simulation.events.movement import TurnLeftEvent, ForwardEvent, BackwardEvent, TurnRightEvent
from pysim.simulation.events.parallel import ParallelEvents
from pysim.simulation.world import World, Wall


class Simulation:
    __world: World
    __position: Vector
    __orientation: Orientation

    def __init__(self, world: World, position: Vector, orientation: Orientation):
        self.__world = world
        self.__position = position
        self.__orientation = orientation

    def forward(self) -> Event:
        old_position = self.__position
        self.__position += Vector.from_orientation(self.__orientation)
        event = ForwardEvent(old_position, self.__orientation)
        if isinstance(self.__world[self.__position], Wall):
            return ParallelEvents([event, ExplosionEvent(self.__position)])
        else:
            return event

    def backward(self) -> Event:
        old_position = self.__position
        self.__position -= Vector.from_orientation(self.__orientation)
        event = BackwardEvent(old_position, self.__orientation)
        if isinstance(self.__world[self.__position], Wall):
            return ParallelEvents([event, ExplosionEvent(self.__position)])
        else:
            return event

    def turn_left(self) -> Event:
        event = TurnLeftEvent(self.__position, self.__orientation)
        self.__orientation = self.__orientation.turn_left()
        return event

    def turn_right(self) -> Event:
        event = TurnRightEvent(self.__position, self.__orientation)
        self.__orientation = self.__orientation.turn_right()
        return event
