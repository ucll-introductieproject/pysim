from pygame import Surface, Vector2, transform

from pysim.graphics.primitives.primitive import Primitive


class Image(Primitive):
    __center: Vector2
    __surface: Surface

    def __init__(self, center: Vector2, surface: Surface):
        self.__center = center
        self.__surface = surface

    def render(self, surface: Surface) -> None:
        width, height = self.__surface.get_size()
        position = self.__center - Vector2(width / 2, height / 2)
        surface.blit(self.__surface, position)

    def transform(self, displacement: Vector2, rotation_angle: float) -> Primitive:
        rotated = transform.rotate(self.__surface, rotation_angle)
        return Image(self.__center + displacement, rotated)
