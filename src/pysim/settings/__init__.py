from typing import Any

from .default import create_default_settings
from .dictionary import DictionarySettings
from .hierarchy import HierarchicalSettings
from .settings import Settings


class _GlobalSettings:
    __settings: Settings
    __runtime_settings: DictionarySettings

    def __init__(self):
        self.__runtime_settings = DictionarySettings()
        self.__settings = HierarchicalSettings([
            self.__runtime_settings,
            create_default_settings(),
        ])

    def __getitem__(self, key: str) -> Any:
        return self.__settings[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__runtime_settings[key] = value


settings = _GlobalSettings()

__all__ = ['settings']
