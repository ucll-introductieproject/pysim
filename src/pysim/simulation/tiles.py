from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Any

from pygame import Rect, Surface, draw

T = TypeVar('T')


class Tile(ABC):
    @abstractmethod
    def render(self, surface: Surface, rect: Rect) -> None:
        ...

    @abstractmethod
    def match(self, matcher: Matcher[T]) -> T:
        ...

    @abstractmethod
    def __copy__(self) -> Tile:
        ...

    @abstractmethod
    def __deepcopy__(self, memo: Any) -> Tile:
        ...


class Empty(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (255, 255, 255)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_empty()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Empty)

    def __copy__(self) -> Empty:
        return self

    def __deepcopy__(self, memo: Any) -> Empty:
        return self


class Wall(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 0)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_wall()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Wall)

    def __copy__(self) -> Wall:
        return self

    def __deepcopy__(self, memo: Any) -> Wall:
        return self


class Chasm(Tile):
    def render(self, surface: Surface, rect: Rect) -> None:
        color = (0, 0, 255)
        draw.rect(surface, color, rect)

    def match(self, matcher: Matcher[T]) -> T:
        return matcher.on_chasm()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Chasm)

    def __copy__(self) -> Chasm:
        return self

    def __deepcopy__(self, memo: Any) -> Chasm:
        return self


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
