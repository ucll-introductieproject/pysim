from .animation import Animation


class LinearFloatAnimation(Animation[float]):
    __start: float
    __stop: float
    __duration: float

    def __init__(self, start: float, stop: float, duration: float):
        assert duration >= 0

        self.__start = start
        self.__stop = stop
        self.__duration = duration

    def __getitem__(self, time: float) -> float:
        assert 0 <= time < self.__duration
        relative_t = time / self.__duration
        return self.__start + (self.__stop - self.__start) * relative_t

    @property
    def duration(self) -> float:
        return self.__duration
