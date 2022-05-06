from abc import ABC, abstractmethod

import pygame

from pysim.graphics.layer import Layer


class Primitive(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface, layer: Layer) -> None:
        ...


class LayerPrimitive(Primitive):
    __layer: Layer

    def __init__(self, layer: Layer):
        self.__layer = layer

    @property
    def layer(self) -> Layer:
        return self.__layer

    def render(self, surface: pygame.Surface, layer: Layer) -> None:
        if layer is self.__layer:
            self._render_on_layer(surface)

    @abstractmethod
    def _render_on_layer(self, surface: pygame.Surface) -> None:
        ...
