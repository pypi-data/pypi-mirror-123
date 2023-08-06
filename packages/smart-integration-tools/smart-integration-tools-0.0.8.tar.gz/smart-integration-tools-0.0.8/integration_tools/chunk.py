from typing import Generator, Iterator, Union, Any, Tuple
from types import GeneratorType
from itertools import chain


def chunk_by_parts(seq: list, parts: int) -> Generator:
    """Chunk by part

    Args:
        seq (list): your data
        parts (int): number of parts

    """
    if len(seq) < parts:
        return [seq]
    avg = len(seq) / float(parts)
    last = 0.0
    while last < len(seq):
        yield seq[int(last) : int(last + avg)]
        last += avg


def chunk_by_items(items: list, step: int):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(items), step):
        yield items[i : i + step]


def chunk_of_generators(iterable: Union[Generator, Iterator], max_value: int = 10):
    def inner(iterator: Union[Generator, Iterator], max_value: int, switcher: list):
        switcher[0] = False
        for i in range(max_value):
            try:
                yield next(iterator)
            except StopIteration:
                return
        switcher[0] = True
        return

    iterator = iter(iterable)
    switcher = [True]
    while switcher[0] == True:
        try:
            yield inner(iterator, max_value, switcher)
        except StopIteration:
            return None


def has_items(iterable: Any) -> Tuple[bool, Any]:
    """check if iterable not empty

    Args:
        iterable (Any): list, tuple, generator

    Returns:
        Tuple[bool, Any]: True/False, chain iterable object
    """
    if isinstance(iterable, GeneratorType):
        try:
            return True, chain([next(iterable)], iterable)
        except StopIteration:
            return False, []
    return bool(iterable), iterable
