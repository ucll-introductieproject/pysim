from pygame import Surface, Vector2, transform

from pysim.graphics.layer import Layer
from pysim.graphics.primitives.primitive import Primitive, LayerPrimitive


class Image(LayerPrimitive):
    __center: Vector2
    __surface: Surface

    def __init__(self, layer: Layer, center: Vector2, surface: Surface):
        super().__init__(layer)
        self.__center = center
        self.__surface = surface

    def _render_on_layer(self, surface: Surface) -> None:
        width, height = self.__surface.get_size()
        position = self.__center - Vector2(width / 2, height / 2)
        surface.blit(self.__surface, position)

    def transform(self, displacement: Vector2, rotation_angle: float) -> Primitive:
        rotated = transform.rotate(self.__surface, -rotation_angle)
        return Image(self.layer, self.__center + displacement, rotated)
