from pygame import Vector2, Rect, Color

from pysim.graphics.animations.animation import Animation
from pysim.graphics.layer import Layer
from pysim.graphics.primitives.primitive import Primitive
from pysim.graphics.primitives.shapes import Rectangle


class Particle(Animation[Primitive]):
    __layer: Layer
    __position: Vector2
    __velocity: Vector2
    __size: float
    __duration: float
    __color: Color

    def __init__(self,
                 layer: Layer,
                 position: Vector2,
                 velocity: Vector2,
                 size: float,
                 duration: float,
                 color: Color):
        self.__layer = layer
        self.__position = position
        self.__velocity = velocity
        self.__size = size
        self.__duration = duration
        self.__color = color

    @property
    def duration(self) -> float:
        return self.__duration

    def __getitem__(self, time: float) -> Primitive:
        assert 0 <= time < self.__duration
        current_position = self.__position + time * self.__velocity
        current_size = self.__size * (1 - time / self.__duration)
        left = current_position.x - current_size / 2
        top = current_position.y - current_size / 2
        rect = Rect(left, top, current_size, current_size)
        return Rectangle(self.__layer, rect, self.__color)
