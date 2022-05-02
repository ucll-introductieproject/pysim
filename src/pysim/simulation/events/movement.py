from pygame import Vector2, Color

from pysim.data import Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.float import LinearFloatAnimation
from pysim.graphics.animations.function import FunctionAnimation
from pysim.graphics.primitives.car import create_car
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.events.event import Event, AnimationSettings


class ForwardEvent(Event):
    __start: Vector
    __angle: float

    def __init__(self, start: Vector, angle: float):
        self.__start = start
        self.__angle = angle

    def animate(self, settings: AnimationSettings) -> Animation[Primitive]:
        def compute_position(time: float) -> Vector2:
            x = x_anim[time]
            y = y_anim[time]
            return Vector2(x, y)

        direction = Vector.from_polar(self.__angle, 1)
        sx, sy = settings.tile_rectangle(self.__start).center
        ex, ey = settings.tile_rectangle(self.__start + direction).center
        x_anim = LinearFloatAnimation(sx, ex, 1)
        y_anim = LinearFloatAnimation(sy, ey, 1)
        pos_anim = FunctionAnimation[Vector2](1, compute_position)
        canonical_car = create_car(Color(255, 0, 0), settings.tile_size)
        return pos_anim.map(lambda p: canonical_car.transform(p, self.__angle))


class TurnLeftEvent(Event):
    __position: Vector
    __start_angle: float

    def __init__(self, position: Vector, start_angle: float):
        self.__position = position
        self.__start_angle = start_angle

    def animate(self, settings: AnimationSettings) -> Animation[Primitive]:
        tile_rect = settings.tile_rectangle(self.__position)
        position = Vector2(tile_rect.center)
        start = self.__start_angle
        stop = start - 90
        angle_anim = LinearFloatAnimation(start, stop, 1)
        canonical_car = create_car(Color(255, 0, 0), settings.tile_size)
        return angle_anim.map(lambda angle: canonical_car.transform(position, angle))
