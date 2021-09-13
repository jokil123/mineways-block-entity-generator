from __future__ import annotations
from dataclasses import dataclass

import numpy


@dataclass
class BlockId():
    id: int
    subId: int


# Height Length Width
def GetBlocks(blockIdData: list[int], blockSubIdData: list[int], dimensions: tuple[int, int, int]) -> list[list[list[BlockId]]]:

    blocks = numpy.ndarray(
        shape=(dimensions[0], dimensions[1], dimensions[2]), dtype=BlockId)

    for height in range(dimensions[0]):
        for length in range(dimensions[1]):
            for width in range(dimensions[2]):
                blockIndex = GetBlockIndex((height, length, width), dimensions)

                block = BlockId(
                    blockIdData[blockIndex], blockSubIdData[blockIndex])

                blocks[height, length, width] = block

    return blocks.tolist()


def GetBlockIndex(position: tuple[int, int, int], dimensions: tuple[int, int, int]):
    return (position[1] * dimensions[1] + position[2]) * dimensions[2] + position[0]
