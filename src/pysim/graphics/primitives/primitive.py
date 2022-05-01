from abc import ABC, abstractmethod

import pygame


class Primitive(ABC):
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        ...
