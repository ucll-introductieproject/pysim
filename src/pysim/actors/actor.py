from multiprocessing import Process, Queue
from typing import Any, Callable, TypeVar, Generic

from pysim.actors.channel import Channel

T = TypeVar('T')


def export(func):
    func.exported = True
    return func


def is_exported_method(object):
    return hasattr(object, 'exported') and callable(object) and object.exported


def collect_exported_methods(cl):
    return [id for id, member in cl.__dict__.items() if is_exported_method(member)]


def _create_mapping_from_environment(environment) -> dict[str, Any]:
    exported_members_ids = collect_exported_methods(type(environment))
    result = {}

    for id in exported_members_ids:
        # Fighting Python's scope rules
        def body():
            nonlocal result
            member = getattr(environment, id)
            func = lambda *args, **kwargs: member(*args, **kwargs)
            result[id] = func

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
