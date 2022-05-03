from pysim.settings.dictionary import DictionarySettings
from pysim.settings.settings import Settings


def create_default_settings() -> Settings:
    return DictionarySettings({
        'show_fps': False,
        'max_fps': 75,
        'speedup': 4,
        'tile_size': 128,
        'explosion_particles': 20
    })
