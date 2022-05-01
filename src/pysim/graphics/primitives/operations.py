from typing import List

import pygame

from pysim.graphics.primitives.primitive import Primitive


class UnionPrimitive(Primitive):
    __children: List[Primitive]

    def __init__(self, children: List[Primitive]):
        assert len(children) >= 1
        self.__children = children

    def render(self, surface: pygame.Surface) -> None:
        for child in self.__children:
            child.render(surface)
