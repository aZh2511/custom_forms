from dataclasses import dataclass


@dataclass(repr=True)
class Test:
    a: str
    b: str = 'a'
