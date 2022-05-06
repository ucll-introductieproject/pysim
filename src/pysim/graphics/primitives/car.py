from typing import Tuple, Iterable

from pygame import Vector2, Rect, Color, Surface

from .image import Image
from .operations import UnionPrimitive
from .primitive import Primitive
from .shapes import Rectangle
from ..layer import Layer


class CarPrimitiveBuilder:
    __layer: Layer
    __color: Color
    __size: Tuple[float, float]

    def __init__(self, layer: Layer, color: Color, size: Tuple[float, float]):
        self.__layer = layer
        self.__color = color
        self.__size = size

    def build(self) -> Primitive:
        return UnionPrimitive([
            self.__create_body(),
            *self.__create_wheels(),
            self.__create_windshield(),
        ])

    def __create_body(self) -> Primitive:
        left = 0
        top = 0
        width, height = self.__size
        rect = Rect(left, top, width, height)
        return Rectangle(self.__layer, rect, self.__color)

    def __create_windshield(self) -> Primitive:
        width, height = self.__size
        w = width * 0.2
        h = height * 0.8
        left = width - w
        top = (height - h) / 2
        rect = Rect(left, top, w, h)
        return Rectangle(self.__layer, rect, Color(0, 255, 255))

    def __create_wheels(self) -> Iterable[Primitive]:
        width, height = self.__size
        wheel_width = width * 0.3
        wheel_height = height * 0.15
        wheel_size = (wheel_width, wheel_height)
        yield self.__create_wheel(Vector2(0.25 * width - wheel_width / 2, 0), wheel_size)
        yield self.__create_wheel(Vector2(0.25 * width - wheel_width / 2, height - wheel_height), wheel_size)
        yield self.__create_wheel(Vector2(0.75 * width - wheel_width / 2, 0), wheel_size)
        yield self.__create_wheel(Vector2(0.75 * width - wheel_width / 2, height - wheel_height), wheel_size)

    def __create_wheel(self, position: Vector2, size: Tuple[float, float]) -> Primitive:
        width, height = size
        left = position.x
        top = position.y
        rect = Rect(left, top, width, height)
        color = Color(0, 0, 0)
        return Rectangle(self.__layer, rect, color)


def create_car(layer: Layer, color: Color, size: float) -> Image:
    width = size
    height = 0.6 * size
    primitive_layer = Layer()
    primitive = CarPrimitiveBuilder(primitive_layer, color, (width, height)).build()
    surface = Surface((width, height))
    surface.set_colorkey((255, 255, 255))
    primitive.render(surface, primitive_layer)
    return Image(layer, Vector2(0, 0), surface)
