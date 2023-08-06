from typing import Protocol
from dataclasses import dataclass

from nametable.Block import BlockProtocol


class NametableProtocol(Protocol):
    blocks: tuple[BlockProtocol, ...]


@dataclass
class Nametable:
    blocks: tuple[BlockProtocol, ...]
