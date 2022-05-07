from pygame import Vector2

from pysim.data import Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.explosion import Explosion
from pysim.graphics.graphics_settings import GraphicsContext
from pysim.graphics.primitives.primitive import Primitive
from pysim.settings import settings
from pysim.simulation.events.event import Event


class ExplosionEvent(Event):
    __position: Vector

    def __init__(self, position: Vector):
        self.__position = position

    def animate(self, context: GraphicsContext) -> Animation[Primitive]:
        n_particles = settings['explosion_particles']
        position = Vector2(context.tile_rectangle(self.__position).center)
        duration = 1
        return Explosion(context.entity_layer, n_particles, position, duration)
