from __future__ import annotations
from dataclasses import dataclass
import dataclasses
from enum import Enum, auto

from nbt import nbt


def ParseSchematic(schematic: nbt.NBTFile) -> NbtFile:
    nbtFile = NbtFile()
