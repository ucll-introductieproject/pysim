from abc import ABC, abstractmethod

from pygame import Surface


class Screen(ABC):
    @abstractmethod
    def update(self, elapsed_seconds: float) -> None:
        ...

    @abstractmethod
    def render(self, surface: Surface) -> None:
        ...
