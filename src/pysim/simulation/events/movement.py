from pygame import Vector2, Color

from pysim.data import Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.float import LinearFloatAnimation
from pysim.graphics.animations.function import FunctionAnimation
from pysim.graphics.primitives.car import create_car
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.events.event import Event


class ForwardEvent(Event):
    __start: Vector
    __direction: Vector

    def __init__(self, start: Vector, direction: Vector):
        self.__start = start
        self.__direction = direction

    def animate(self) -> Animation[Primitive]:
        def compute_position(time: float) -> Vector2:
            x = x_anim[time]
            y = y_anim[time]
            return Vector2(x, y)

        wx, wy = self.__start
        dx, dy = self.__direction
        tile_size = 128
        sx = wx * tile_size
        sy = wy * tile_size
        ex = (wx + dx) * tile_size
        ey = (wy + dy) * tile_size
        x_anim = LinearFloatAnimation(sx, ex, 1)
        y_anim = LinearFloatAnimation(sy, ey, 1)
        pos_anim = FunctionAnimation[Vector2](1, compute_position)
        canonical_car = create_car(Color(255, 0, 0), tile_size)
        return pos_anim.map(lambda p: canonical_car.transform(p, 0))
