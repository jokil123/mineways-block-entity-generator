from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from nbt import nbt

from .tile_entity_classes import *


class MaterialType(Enum):
    CLASSIC = "Classic"  # <v0.3 (2009-11-10)
    ALPHA = "Alpha"      # >v0.3
    POCKET = "Pocket"    # Pocket (probably Bedrock) Edition


class ItemStackVersion(Enum):
    NUMERIC = 17  # Numeric IDs
    TEXT = 18  # Text ID


class Platform(Enum):
    BUKKIT = "bukkit"


@dataclass
class TileTick:
    # The ID of the block; used to activate the correct block update procedure.
    i: str
    # If multiple tile ticks are scheduled for the same tick, tile ticks with lower p are processed first. If they also have the same p, the order is unknown.
    p: int
    # The number of ticks until processing should occur. May be negative when processing is overdue.
    t: int
    # position
    x: int
    y: int
    z: int


@dataclass
class Id:
    namespace: str
    path: str


@dataclass
class Icon:
    count: int
    id: Id
    tag: nbt.NBTFile


@dataclass
class UUID:
    uuid: list[int]


@dataclass
class Item:
    count: int
    slot: int
    id: Id
    tag: NbtFile


@dataclass
class Entity:
    air: int
    customName: str
    customNameVisible: bool
    fallDistance: float
    fire: int
    glowing: bool
    hasVisualFire: bool
    id: Id
    invulnerable: bool
    motion: tuple[float, float, float]
    noGravity: bool
    onGround: bool
    passengers: Entity
    portalCooldown: int
    pos: tuple[float, float, float]
    rotation: tuple[float, float]
    silent: bool
    tags: list
    ticksFrozen: int
    uuid: UUID


@dataclass
class NbtFile:
    # dimensions
    width: int
    height: int
    length: int
    # version
    materials: MaterialType
    platform: Platform
    blocks: bytearray
    # usage unknown
    addblocks: bytearray
    # schematica only (deprecated)
    add: bytearray
    data: bytearray
    entities: list[Entity]
    tileEntities: list[BlockEntity]
    # schematica only
    icon: Icon
    # schematica only
    schematicaMapping: dict[int, str]
    # schematica only
    extendedMetadata: nbt.NBTFile
    # WorldEdit-only
    weOriginX: int
    weOriginY: int
    weOriginZ: int
    weOffsetX: int
    weOffsetY: int
    weOffsetZ: int
    # MCEdit-Unified only
    itemStackVersion: ItemStackVersion
    # MCEdit-Unified only
    blockIds: dict[int, str]
    # MCEdit-Unified only
    itemIds: dict[int, str]
    # MCEdit-Unified only
    tileTicks: list[TileTick]
    schematicTileTick: TileTick
    # MCEdit-Unified only
    biomes: bytearray
