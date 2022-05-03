from typing import Tuple, Iterable

from pygame import Vector2, Rect, Color, Surface

from .image import Image
from .operations import UnionPrimitive
from .primitive import Primitive
from .shapes import Rectangle


class _CarBuilder:
    __image: Surface

    def __init__(self, color: Color, size: Tuple[float, float]):
        self.__image = _CarBuilder.__create_image(color, size)

    def build(self) -> Image:
        return Image(Vector2(0, 0), self.__image)

    @staticmethod
    def __create_image(color: Color, size: Tuple[float, float]) -> Surface:
        whole = UnionPrimitive([
            _CarBuilder.__create_body(color, size),
            *_CarBuilder.__create_wheels(size),
            _CarBuilder.__create_windshield(size),
        ])
        surface = Surface(size)
        surface.set_colorkey((255, 255, 255))
        whole.render(surface)
        return surface

    @staticmethod
    def __create_body(color: Color, size: Tuple[float, float]) -> Primitive:
        left = 0
        top = 0
        width, height = size
        rect = Rect(left, top, width, height)
        return Rectangle(rect, color)

    @staticmethod
    def __create_windshield(size: Tuple[float, float]) -> Primitive:
        width, height = size
        w = width * 0.2
        h = height * 0.8
        left = width - w
        top = (height - h) / 2
        rect = Rect(left, top, w, h)
        return Rectangle(rect, Color(0, 255, 255))

    @staticmethod
    def __create_wheels(size: Tuple[float, float]) -> Iterable[Primitive]:
        width, height = size
        wheel_width = width * 0.3
        wheel_height = height * 0.15
        wheel_size = (wheel_width, wheel_height)
        yield _CarBuilder.__create_wheel(Vector2(0.25 * width - wheel_width / 2, 0), wheel_size)
        yield _CarBuilder.__create_wheel(Vector2(0.25 * width - wheel_width / 2, height - wheel_height), wheel_size)
        yield _CarBuilder.__create_wheel(Vector2(0.75 * width - wheel_width / 2, 0), wheel_size)
        yield _CarBuilder.__create_wheel(Vector2(0.75 * width - wheel_width / 2, height - wheel_height), wheel_size)

    @staticmethod
    def __create_wheel(position: Vector2, size: Tuple[float, float]) -> Primitive:
        width, height = size
        left = position.x
        top = position.y
        rect = Rect(left, top, width, height)
        color = Color(0, 0, 0)
        return Rectangle(rect, color)


def create_car(color: Color, size: float) -> Image:
    width = size
    height = 0.6 * size
    return _CarBuilder(color, (width, height)).build()
