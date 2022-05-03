from __future__ import annotations

from typing import Tuple

from pygame import Vector2, Color, Rect

from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.float import LinearFloatAnimation
from pysim.graphics.animations.function import FunctionAnimation
from pysim.graphics.graphics_settings import GraphicsSettings
from pysim.graphics.primitives.primitive import Primitive
from pysim.graphics.primitives.shapes import Rectangle
from pysim.simulation.events.event import Event


class BlockEvent(Event):
    pass


class MoveEvent(BlockEvent):
    __start: Vector
    __displacement: Vector

    def __init__(self, start: Vector, displacement: Vector):
        self.__start = start
        self.__displacement = displacement

    def animate(self, settings: GraphicsSettings) -> Animation[Primitive]:
        def compute_position(time: float) -> Vector2:
            x = x_anim[time]
            y = y_anim[time]
            return Vector2(x, y)

        def compute_primitive(position: Vector2) -> Primitive:
            size = settings.tile_size * 0.9
            left = position.x - size / 2
            top = position.y - size / 2
            rect = Rect(left, top, size, size)
            color = Color(128, 128, 128)
            return Rectangle(rect, color)

        sx, sy = settings.tile_rectangle(self.__start).center
        ex, ey = settings.tile_rectangle(self.__start + self.__displacement).center
        x_anim = LinearFloatAnimation(sx, ex, 1)
        y_anim = LinearFloatAnimation(sy, ey, 1)
        pos_anim = FunctionAnimation[Vector2](1, compute_position)
        return pos_anim.map(compute_primitive)


class Block:
    __position: Vector

    def __init__(self, position: Vector):
        self.__position = position

    @property
    def position(self) -> Vector:
        return self.__position

    def move(self, direction: Orientation) -> Tuple[Block, Event]:
        displacement = Vector.from_orientation(direction)
        new_position = self.__position + displacement
        new_block = Block(new_position)
        event = MoveEvent(self.__position, displacement)
        return (new_block, event)
