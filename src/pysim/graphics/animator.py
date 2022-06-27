from pygame import Rect

from pysim.data import Vector
from pysim.graphics.animations.animation import Animation
from pysim.graphics.animations.constant import ConstantAnimation
from pysim.graphics.animations.parallel import ParallelAnimation
from pysim.graphics.context import GraphicsContext
from pysim.graphics.layer import Layer
from pysim.graphics.primitives.operations import UnionPrimitive
from pysim.graphics.primitives.primitive import Primitive
from pysim.simulation.events import Event
from pysim.simulation.world import World


class _GraphicsContext(GraphicsContext):
    __entity_layer: Layer
    __tile_layer: Layer

    def __init__(self, tile_layer: Layer, entity_layer: Layer):
        self.__tile_layer = tile_layer
        self.__entity_layer = entity_layer

    @property
    def tile_size(self) -> float:
        return 32

    def tile_rectangle(self, position: Vector) -> Rect:
        tile_size = self.tile_size
        width = tile_size
        height = tile_size
        left = position.x * width
        top = position.y * height
        return Rect(left, top, width, height)

    @property
    def entity_layer(self) -> Layer:
        return self.__entity_layer

    @property
    def tile_layer(self) -> Layer:
        return self.__tile_layer


class Animator:
    __tile_layer: Layer
    __entity_layer: Layer

    def __init__(self, tile_layer: Layer, entity_layer: Layer):
        self.__tile_layer = tile_layer
        self.__entity_layer = entity_layer

    def animate(self, world: World, event: Event) -> Animation[Primitive]:
        def render_tile_at(position):
            tile = world[position]
            tile_image = tile.render(context, position)
            return ConstantAnimation(tile_image, 10)

        context = _GraphicsContext(tile_layer=self.__tile_layer, entity_layer=self.__entity_layer)
        tile_primitives = [render_tile_at(Vector(x, y)) for x in range(world.width) for y in range(world.height)]
        return ParallelAnimation(UnionPrimitive, *tile_primitives)
