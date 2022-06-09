from abc import ABC, abstractmethod


class Object(ABC):
    @abstractmethod
    def is_movable(self) -> bool:
        ...
