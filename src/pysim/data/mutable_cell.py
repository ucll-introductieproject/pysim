from typing import TypeVar, Generic

T = TypeVar('T')


class MutableCell(Generic[T]):
    __contents = T

    def __init__(self, initial_value: T):
        self.__contents = initial_value

    @property
    def value(self) -> T:
        return self.__contents

    @value.setter
    def value(self, new_value: T) -> None:
        self.__contents = new_value
