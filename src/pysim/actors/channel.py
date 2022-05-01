from multiprocessing import Queue
from typing import TypeVar, Generic

T = TypeVar('T')


class Channel(Generic[T]):
    __queue: Queue

    def __init__(self, queue: Queue, timeout: float = 1):
        self.__queue = queue
        self.__timeout = timeout

    def send(self, message: T) -> None:
        self.__queue.put(message)

    def receive(self) -> T:
        return self.__queue.get(block=True, timeout=self.__timeout)
