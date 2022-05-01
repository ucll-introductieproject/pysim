from abc import ABC, abstractmethod
from typing import Any


class Settings(ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        ...

    @abstractmethod
    def __contains__(self, key: str) -> bool:
        ...
