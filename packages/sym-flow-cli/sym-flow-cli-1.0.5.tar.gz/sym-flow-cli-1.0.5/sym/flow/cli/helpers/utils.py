from typing import Callable, Dict, TypeVar

KeyT = TypeVar("KeyT")
ValueT = TypeVar("ValueT")


def filter_dict(
    d: Dict[KeyT, ValueT], filter_func: Callable[[ValueT], bool]
) -> Dict[KeyT, ValueT]:
    return {k: v for k, v in d.items() if filter_func(v)}
