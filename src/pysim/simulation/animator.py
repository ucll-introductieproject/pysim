from __future__ import annotations

from typing import List

from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.stepwise import StepwiseAnimation
from pysim.graphics.graphics_settings import GraphicsContext
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.simulation import Simulation


class Animator:
    __simulation: Simulation
    __animations: List[Animation[Primitive]]
    __context: GraphicsContext

    def __init__(self, simulation: Simulation, context: GraphicsContext):
        self.__simulation = simulation
        self.__animations = []
        self.__context = context

    @property
    def simulation(self) -> Simulation:
        return self.__simulation

    def build_animation(self) -> Animation[Primitive]:
        return StepwiseAnimation(self.__animations)

    def forward(self) -> Animator:
        new_state, event = self.__simulation.forward()
        self.__simulation = new_state
        animation = event.animate(self.__context)
        self.__animations.append(animation)
        return self

    def backward(self) -> Animator:
        new_state, event = self.__simulation.backward()
        self.__simulation = new_state
        animation = event.animate(self.__context)
        self.__animations.append(animation)
        return self

    def turn_left(self) -> Animator:
        new_state, event = self.__simulation.turn_left()
        self.__simulation = new_state
        animation = event.animate(self.__context)
        self.__animations.append(animation)
        return self

    def turn_right(self) -> Animator:
        new_state, event = self.__simulation.turn_right()
        self.__simulation = new_state
        animation = event.animate(self.__context)
        self.__animations.append(animation)
        return self
