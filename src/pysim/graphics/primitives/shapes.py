import pygame
from pygame import Vector2, Rect, Color

from .primitive import Primitive


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


class Rectangle(Primitive):
    __rect: Rect
    __radius: float
    __color: Color

    def __init__(self, rect: Rect, color: Color):
        self.__rect = rect
        self.__color = color

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.__color, self.__rect)