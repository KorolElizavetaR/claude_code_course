from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True)
class Item:
    id: int = field(default=0, init=False)
    name: str = ""
    description: str = ""

    __index: ClassVar[int] = 0

    def __init__(self, name: str, description: str) -> None:
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "description", description)
        object.__setattr__(self, "id", Item.__index)
        Item.__index += 1