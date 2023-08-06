from typing import (
    Any,
    Iterable
)


def flatten(l: Iterable[Any]):
    return [item for sublist in l for item in sublist]
