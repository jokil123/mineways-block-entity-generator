from nbt import nbt
from dataclasses import dataclass
from enum import Enum, auto


class MaterialType(Enum):
    CLASSIC = "Classic"
    POCKET = "Pocket"
    ALPHA = "Alpha"


@dataclass
class NbtFile:
    width: int
    height: int
    length: int
    materials: MaterialType
    blocks: list[int]
    # addblocks
    # add
    data: list[int]
    entities: list[entity]
    tileEntities: list[tileEntity]
    # icon
    # schematicaMapping
    # extendedMetadata
    weOriginX: int
    weOriginY: int
    weOriginZ: int
    weOffsetX: int
    weOffsetY: int
    weOffsetZ: int
    # itemStackVersion
    # blockIds
    # itemIds
    # tileTicks
    # i
    # p
    # t
    # x
    # y
    # z
    # biomes


def ParseSchematic(schematic: nbt.NBTFile) -> NbtFile:
    nbtFile = NbtFile()
