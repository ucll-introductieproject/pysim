from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

from pygame import Rect, Surface, draw

T = TypeVar('T')


class Tile(ABC):
    @abstractmethod
    def render(self, surface: Surface, rect: Rect) -> None:
        ...

    @abstractmethod
    def match(self, matcher: Matcher[T]) -> T:
        ...


class Empty(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (255, 255, 255)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_empty()


class Wall(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 0)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_wall()


class Chasm(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 255)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_chasm()


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
        tile: Tile,
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
