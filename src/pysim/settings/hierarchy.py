from typing import Any, List

from .settings import Settings


class HierarchicalSettings(Settings):
    __children: List[Settings]

    def __init__(self, children: List[Settings]):
        assert children is not None
        assert len(children) > 0
        self.__children = children

    def __getitem__(self, key: str) -> Any:
        child = next(c for c in self.__children if key in c)
        return child[key]

    def __contains__(self, key: str) -> bool:
        return any(key in c for c in self.__children)
