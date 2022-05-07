from __future__ import annotations

from abc import abstractmethod
from typing import Tuple

from pygame import Vector2

from pysim.data import Vector
from pysim.data.orientation import Orientation
from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.constant import ConstantAnimation
from pysim.graphics.animations.float import LinearFloatAnimation
from pysim.graphics.animations.function import FunctionAnimation
from pysim.graphics.graphics_settings import GraphicsContext
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.entities.entity import Entity
from pysim.simulation.events.event import Event


class AgentEvent(Event):
    @abstractmethod
    def animate(self, context: GraphicsContext) -> Animation[Primitive]:
        ...


class StayEvent(AgentEvent):
    __position: Vector
    __orientation: Orientation

    def __init__(self, position: Vector, orientation: Orientation):
        self.__position = position
        self.__orientation = orientation

    def animate(self, context: GraphicsContext) -> Animation[Primitive]:
        position = Vector2(context.tile_rectangle(self.__position).center)
        angle = self.__orientation.angle
        transformed_car = context.agent.transform(position, angle)
        return ConstantAnimation[Primitive](transformed_car, 1)


class MoveEvent(AgentEvent):
    __start: Vector
    __displacement: Vector
    __orientation: Orientation

    def __init__(self, start: Vector, displacement: Vector, orientation: Orientation):
        self.__start = start
        self.__displacement = displacement
        self.__orientation = orientation

    def animate(self, context: GraphicsContext) -> Animation[Primitive]:
        def compute_position(time: float) -> Vector2:
            x = x_anim[time]
            y = y_anim[time]
            return Vector2(x, y)

        sx, sy = context.tile_rectangle(self.__start).center
        ex, ey = context.tile_rectangle(self.__start + self.__displacement).center
        x_anim = LinearFloatAnimation(sx, ex, 1)
        y_anim = LinearFloatAnimation(sy, ey, 1)
        pos_anim = FunctionAnimation[Vector2](1, compute_position)
        canonical_car = context.agent
        return pos_anim.map(lambda p: canonical_car.transform(p, self.__orientation.angle))


class ForwardEvent(MoveEvent):
    def __init__(self, start: Vector, orientation: Orientation):
        super().__init__(start, Vector.from_orientation(orientation), orientation)


class BackwardEvent(MoveEvent):
    def __init__(self, start: Vector, orientation: Orientation):
        super().__init__(start, -Vector.from_orientation(orientation), orientation)


class TurnEvent(AgentEvent):
    __position: Vector
    __start_orientation: Orientation

    def __init__(self, position: Vector, start_orientation: Orientation):
        self.__position = position
        self.__start_orientation = start_orientation

    def animate(self, context: GraphicsContext) -> Animation[Primitive]:
        tile_rect = context.tile_rectangle(self.__position)
        position = Vector2(tile_rect.center)
        start = self.__start_orientation.angle
        stop = self._make_turn(self.__start_orientation).angle
        angle_anim = LinearFloatAnimation(start, stop, 1)
        return angle_anim.map(lambda angle: context.agent.transform(position, angle))

    @abstractmethod
    def _make_turn(self, orientation: Orientation) -> Orientation:
        ...


class TurnLeftEvent(TurnEvent):
    def _make_turn(self, orientation: Orientation) -> Orientation:
        return orientation.turn_left()


class TurnRightEvent(TurnEvent):
    def _make_turn(self, orientation: Orientation) -> Orientation:
        return orientation.turn_right()


class BumpEvent(MoveEvent):
    def __init__(self, start: Vector, orientation: Orientation):
        super().__init__(start, Vector(0, 0), orientation)


class Agent(Entity):
    __position: Vector
    __orientation: Orientation

    def __init__(self, position: Vector, orientation: Orientation):
        self.__position = position
        self.__orientation = orientation

    @property
    def position(self) -> Vector:
        return self.__position

    @property
    def orientation(self) -> Orientation:
        return self.__orientation

    def forward(self) -> Tuple[Agent, Event]:
        direction = Vector.from_orientation(self.__orientation)
        new_position = self.__position + direction
        new_agent = Agent(new_position, self.__orientation)
        event = ForwardEvent(self.__position, self.__orientation)
        return (new_agent, event)

    def backward(self) -> Tuple[Agent, Event]:
        direction = Vector.from_orientation(self.__orientation)
        new_position = self.__position - direction
        new_agent = Agent(new_position, self.__orientation)
        event = BackwardEvent(self.__position, self.__orientation)
        return (new_agent, event)

    def turn_left(self) -> Tuple[Agent, Event]:
        new_agent = Agent(self.__position, self.__orientation.turn_left())
        event = TurnLeftEvent(self.__position, self.__orientation)
        return (new_agent, event)

    def turn_right(self) -> Tuple[Agent, Event]:
        new_agent = Agent(self.__position, self.__orientation.turn_right())
        event = TurnRightEvent(self.__position, self.__orientation)
        return (new_agent, event)

    def stay(self) -> Event:
        event = StayEvent(self.__position, self.__orientation)
        return event
