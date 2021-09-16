from __future__ import annotations


class Block:
    def __init__(self) -> None:
        self.namespace: str = "minecraft"
        self.id: int
        self.subId: int


class Schematic:
    def __init__(self) -> None:
        self.blocks: list[Block] = []
