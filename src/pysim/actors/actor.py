from multiprocessing import Process, Queue
from typing import Any, Callable, TypeVar, Generic

from pysim.actors.channel import Channel
from pysim.actors.environment import collect_exported_methods

T = TypeVar('T')


def _create_mapping_from_environment(environment) -> dict[str, Any]:
    exported_members_ids = collect_exported_methods(type(environment))
    result = {}

    for member_id in exported_members_ids:
        # Fighting Python's scope rules
        def body():
            nonlocal result
            member = getattr(environment, member_id)
            result[member_id] = lambda *args, **kwargs: member(*args, **kwargs)

        body()

    return result


def _run(source: str, environment_factory: Callable[[Channel], Any], channel: Channel[T]) -> None:
    environment = environment_factory(channel)
    mapping = _create_mapping_from_environment(environment)
    exec(source, mapping)


class Actor(Generic[T]):
    __channel: Channel[T]

    def __init__(self, source: str, environment_factory: Callable[[Channel], Any]):
        queue: Queue[T] = Queue()
        self.__channel = Channel(queue)
        self.__process = Process(target=_run, args=(source, environment_factory, self.__channel))
        self.__process.start()

    def send(self, message: T):
        self.__channel.send(message)

    def receive(self) -> T:
        return self.__channel.receive()
