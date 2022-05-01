from typing import Tuple

import pygame
from pygame import Vector2

from .primitive import Primitive

Color = Tuple[int, int, int]


class Circle(Primitive):
    __center: Vector2
    __radius: float
    __color: Color

    def __init__(self, center: Vector2, radius: float, color: Color):
        self.__center = center
        self.__radius = radius
        self.__color = color

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.__color, self.__center, self.__radius)
