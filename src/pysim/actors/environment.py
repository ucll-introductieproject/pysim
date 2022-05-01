from typing import Any


def export(func):
    func.exported = True
    return func


def is_exported_method(object: Any) -> bool:
    return hasattr(object, 'exported') and callable(object) and object.exported


def collect_exported_methods(cl):
    return [id for id, member in cl.__dict__.items() if is_exported_method(member)]
