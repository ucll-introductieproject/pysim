from abc import ABC, abstractmethod

from pygame import Rect, Surface


class Tile(ABC):
    @abstractmethod
    def render(self, surface: Surface, rect: Rect) -> None:
        ...
