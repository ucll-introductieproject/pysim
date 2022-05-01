from typing import Any, Dict

from .settings import Settings


class DictionarySettings(Settings):
    __table: Dict[str, Any]

    def __init__(self, dictionary: Dict[str, Any] = None):
        self.__table = dictionary or {}

    def __getitem__(self, key: str) -> Any:
        return self.__table[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__table[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.__table
