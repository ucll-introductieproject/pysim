from typing import Tuple, Iterable

from pygame import Vector2, Rect, Color, Surface, transform

from .image import Image
from .operations import UnionPrimitive
from .primitive import Primitive
from .shapes import Rectangle


class Car:
    __image: Surface

    def __init__(self, color: Color, size: Tuple[float, float]):
        self.__image = self.__create_image(color, size)

    def build(self, position: Vector2, angle: float) -> Primitive:
        rotated = transform.rotate(self.__image, angle)
        return Image(position, rotated)

    def __create_image(self, color: Color, size: Tuple[float, float]) -> Surface:
        whole = UnionPrimitive([
            self.__create_body(color, size),
            *self.__create_wheels(size)
        ])
        surface = Surface(size)
        surface.set_colorkey((255, 255, 255))
        whole.render(surface)
        return surface

    def __create_body(self, color: Color, size: Tuple[float, float]) -> Primitive:
        left = 0
        top = 0
        width, height = size
        rect = Rect(left, top, width, height)
        return Rectangle(rect, color)

    def __create_wheels(self, size: Tuple[float, float]) -> Iterable[Primitive]:
        width, height = size
        wheel_width = width * 0.15
        wheel_height = height * 0.3
        center = Vector2(width / 2, height / 2)
        return (self.__create_wheel(center - Vector2(a * (width * 0.5 - wheel_width / 2),
                                                     b * (height * 0.4 - wheel_height / 2)),
                                    (wheel_width, wheel_height))
                for a in [-1, 1]
                for b in [-1, 1])

    def __create_wheel(self, position: Vector2, size: Tuple[float, float]) -> Primitive:
        width, height = size
        left = position.x - width / 2
        top = position.y - height / 2
        rect = Rect(left, top, width, height)
        color = Color(0, 0, 0)
        return Rectangle(rect, color)
