from pysim.simulation.objects.object import Object


class Block(Object):
    def is_movable(self) -> bool:
        return True
