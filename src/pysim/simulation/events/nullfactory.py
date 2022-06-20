from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.simulation.events.eventfactory import EventFactory


class NullEventFactory(EventFactory[None]):
    def actor_moved_forward(self, agent_index: int) -> None:
        return None

    def object_moved(self, origin: Vector, orientation: Orientation) -> None:
        return None

    def parallel(self, *event: None) -> None:
        return None

    def nothing(self) -> None:
        return None
