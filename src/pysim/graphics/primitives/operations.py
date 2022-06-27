from typing import List, Iterable

import pygame

from pysim.graphics.layer import Layer
from pysim.graphics.primitives.primitive import Primitive


class UnionPrimitive(Primitive):
    __children: List[Primitive]

    def __init__(self, children: Iterable[Primitive]):
        self.__children = list(children)

    def render(self, surface: pygame.Surface, layer: Layer) -> None:
        for child in self.__children:
            child.render(surface, layer)
