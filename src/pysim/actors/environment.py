from typing import Any


def export(func):
    func.exported = True
    return func


def is_exported_method(obj: Any) -> bool:
    return hasattr(obj, 'exported') and callable(obj) and obj.exported


def collect_exported_methods(cl):
    return [identifier for identifier, member in cl.__dict__.items() if is_exported_method(member)]
