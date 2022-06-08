from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

from pygame import Rect, Surface, draw

T = TypeVar('T')


class TileState(ABC):
    @abstractmethod
    def render(self, surface: Surface, rect: Rect) -> None:
        ...

    @abstractmethod
    def match(self, matcher: Matcher[T]) -> T:
        ...


class Empty(TileState):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (255, 255, 255)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_empty()


class Wall(TileState):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 0)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_wall()


class Chasm(TileState):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 255)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_chasm()


class Tile:
    def __init__(self, state: TileState):
        self.state = state


class Matcher(ABC, Generic[T]):
    @abstractmethod
    def on_empty(self) -> T:
        ...

    @abstractmethod
    def on_wall(self) -> T:
        ...

    @abstractmethod
    def on_chasm(self) -> T:
        ...


def match_tile(
        tile: TileState,
        /,
        if_empty: Callable[[], T],
        if_wall: Callable[[], T],
        if_chasm: Callable[[], T]) -> T:
    class M(Matcher):
        def on_empty(self) -> T:
            return if_empty()

        def on_wall(self) -> T:
            return if_wall()

        def on_chasm(self) -> T:
            return if_chasm()

    return tile.match(M())
