from typing import Tuple

from pygame import Vector2, Rect, Color

from .primitive import Primitive
from .shapes import Rectangle
from .transform import UnionPrimitive


def _create_body(position: Vector2, color: Color, size: Tuple[float, float]) -> Primitive:
    width, height = size
    left = position.x - width / 2
    top = position.y - height / 2
    rect = Rect(left, top, width, height)
    return Rectangle(rect, color)


def _create_wheel(position: Vector2, size: Tuple[float, float]) -> Primitive:
    width, height = size
    left = position.x - width / 2
    top = position.y - height / 2
    rect = Rect(left, top, width, height)
    color = Color(0, 0, 0)
    return Rectangle(rect, color)


def create_car_primitive(position: Vector2, angle: float, color: Color, size: Tuple[float, float]) -> Primitive:
    width, height = size
    wheel_width = width * 0.2
    wheel_height = height * 0.3
    body = _create_body(position, color, size)
    wheels = (_create_wheel(position + Vector2(a * width * 0.5, b * height * 0.3), (wheel_width, wheel_height))
              for a in [-1, 1]
              for b in [-1, 1])
    return UnionPrimitive([body, *wheels])
