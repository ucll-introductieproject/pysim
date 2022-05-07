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
        return matcher.on_empty(self)


class Wall(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 0)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_wall(self)


class Chasm(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 255)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_chasm(self)


class Matcher(ABC, Generic[T]):
    @abstractmethod
    def on_empty(self, tile: Empty) -> T:
        ...

    @abstractmethod
    def on_wall(self, tile: Wall) -> T:
        ...

    @abstractmethod
    def on_chasm(self, tile: Chasm) -> T:
        ...


def match_tile(
        tile: Tile,
        if_empty: Callable[[Empty], T],
        if_wall: Callable[[Wall], T],
        if_chasm: Callable[[Chasm], T]) -> T:
    class M(Matcher):
        def on_empty(self, tile: Empty) -> T:
            return if_empty(tile)

        def on_wall(self, tile: Wall) -> T:
            return if_wall(tile)

        def on_chasm(self, tile: Chasm) -> T:
            return if_chasm(tile)

    return tile.match(M())
