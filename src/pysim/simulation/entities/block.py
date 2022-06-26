from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.entities.entity import Entity
from pysim.simulation.events.event import Event


# TODO Add fields
class _MovedEvent(Event):
    pass


class Block(Entity):
    def move(self, position: Vector, direction: Orientation) -> Event:
        return _MovedEvent()

    def is_movable(self) -> bool:
        return True
