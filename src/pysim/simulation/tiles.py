from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, NoReturn, Optional

from pygame import Color

from pysim.data import Vector
from pysim.graphics.context import GraphicsContext
from pysim.graphics.primitives.primitive import Primitive
from pysim.graphics.primitives.shapes import Rectangle
from pysim.simulation.entities.entity import Entity


class Tile(ABC):
    @abstractmethod
    def render(self, context: GraphicsContext, position: Vector) -> Primitive:
        ...

    def __copy__(self) -> NoReturn:
        raise copy.Error()

    @abstractmethod
    def __deepcopy__(self, memo: Any) -> Tile:
        ...

    @abstractmethod
    def is_traversable(self) -> bool:
        """
        Returns True if an entity can move onto this tile,
        False otherwise.
        """
        ...

    @property
    @abstractmethod
    def accepts_objects(self) -> bool:
        ...

    @property
    @abstractmethod
    def contents(self) -> Optional[Entity]:
        ...

    @contents.setter
    @abstractmethod
    def contents(self, obj: Entity) -> None:
        ...


class CanContainObject:
    __contents: Optional[Entity]

    @property
    def accepts_objects(self) -> bool:
        return self.__contents is None

    @property
    def contents(self) -> Optional[Entity]:
        return self.__contents

    @contents.setter
    def contents(self, obj: Entity) -> None:
        self.__contents = obj


class CannotContainObject:
    @property
    def accepts_objects(self) -> bool:
        return False

    @property
    def contents(self) -> Optional[Entity]:
        return None

    @contents.setter
    def contents(self, obj: Entity) -> None:
        raise NotImplementedError()


class Empty(CanContainObject, Tile):
    def __init__(self, contents: Optional[Entity] = None) -> None:
        self.contents = contents

    def render(self, context: GraphicsContext, position: Vector) -> Primitive:
        rect = context.tile_rectangle(position)
        color = Color(200, 200, 200)
        return Rectangle(context.tile_layer, rect, color)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Empty)

    def __deepcopy__(self, memo: Any) -> Empty:
        contents = deepcopy(self.contents, memo)
        return Empty(contents)

    def is_traversable(self) -> bool:
        return True


class Wall(CannotContainObject, Tile):
    def render(self, context: GraphicsContext, position: Vector) -> Primitive:
        rect = context.tile_rectangle(position)
        color = Color(0, 0, 0)
        return Rectangle(context.tile_layer, rect, color)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Wall)

    def __deepcopy__(self, memo: Any) -> Wall:
        return self

    def is_traversable(self) -> bool:
        return False


class Chasm(CanContainObject, Tile):
    def __init__(self, contents: Optional[Entity] = None) -> None:
        self.contents = contents

    def render(self, context: GraphicsContext, position: Vector) -> Primitive:
        rect = context.tile_rectangle(position)
        color = Color(0, 0, 255)
        return Rectangle(context.tile_layer, rect, color)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Chasm)

    def __deepcopy__(self, memo: Any) -> Chasm:
        contents = deepcopy(self.contents, memo)
        return Chasm(contents)

    def is_traversable(self) -> bool:
        return True
