import pygame
from pygame import Vector2, Rect, Color

from .primitive import LayerPrimitive
from ..layer import Layer


class Circle(LayerPrimitive):
    __center: Vector2
    __radius: float
    __color: Color

    def __init__(self, layer: Layer, center: Vector2, radius: float, color: Color):
        super().__init__(layer)
        self.__center = center
        self.__radius = radius
        self.__color = color

    def _render_on_layer(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.__color, self.__center, self.__radius)


class Rectangle(LayerPrimitive):
    __rect: Rect
    __radius: float
    __color: Color

    def __init__(self, layer: Layer, rect: Rect, color: Color):
        super().__init__(layer)
        self.__rect = rect
        self.__color = color

    def _render_on_layer(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.__color, self.__rect)
