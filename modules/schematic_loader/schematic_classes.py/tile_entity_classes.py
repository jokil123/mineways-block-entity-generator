from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from .schematic_classes_main import Id, Entity, Item, UUID

from nbt import nbt


@dataclass
class CustomName:
    customName: str


@dataclass
class BlockEntity:
    id: Id
    keepPacked: bool
    x: int
    y: int
    z: int


@dataclass
class Banner(BlockEntity, CustomName):
    patterns: list[BannerPattern]


@dataclass
class BannerPattern:
    color: int
    pattern: str


@dataclass
class Lock:
    lock: str


@dataclass
class LootTable:
    lootTable: str
    lootTableSeed: int


@dataclass
class Beacon(BlockEntity, CustomName, Lock):
    levels: int
    primary: int
    secondary: int


@dataclass
class Bed(BlockEntity):
    pass


@dataclass
class BeeHive(BlockEntity):
    bees: list[Bee]
    flowerPos: tuple[int, int, int]


@dataclass
class Bee:
    entity: list[Entity]
    minOccupationTicks: int
    ticksInHive: int


@dataclass
class Bell(BlockEntity):
    pass


@dataclass
class Comparator(BlockEntity):
    outputSignal: int


@dataclass
class CommandBlock(BlockEntity, CustomName):
    auto: bool
    command: str
    conditionMet: bool
    lastExecution: int
    lastOutput: str
    powered: bool
    successCount: int
    trackOutput: bool
    updateLastExecution: bool


@dataclass
class Conduit(BlockEntity):
    target: UUID


@dataclass
class DaylightDetector(BlockEntity):
    pass


@dataclass
class InventoryBlock(BlockEntity, CustomName, LootTable, Lock):
    items: list[Item]


@dataclass
class Barrel(InventoryBlock):
    pass


@dataclass
class Chest(InventoryBlock):
    pass


@dataclass
class ShulkerBox(InventoryBlock):
    pass


@dataclass
class TrappedChest(InventoryBlock):
    pass


@dataclass
class BrewingStand(BlockEntity, CustomName, Lock):
    brewTime: int
    Fuel: int
    items: list[Item]


@dataclass
class Campfire(BlockEntity):
    cookingTime: list[int]
    cookingTotalTimes: list[int]
    items: list[Item]


@dataclass
class SoulCampfire(Campfire):
    pass


@dataclass
class Dispenser(InventoryBlock):
    pass


@dataclass
class Dropper(InventoryBlock):
    pass


@dataclass
class Hopper(InventoryBlock):
    transferCooldown: int


@dataclass
class EnchantingTable(BlockEntity, CustomName):
    pass


@dataclass
class EnderChest(BlockEntity):
    pass


@dataclass
class EndGateway(BlockEntity):
    age: int
    exactTeleport: bool
    exitPortal: tuple[int, int, int]


@dataclass
class EndPortal(BlockEntity):
    pass


@dataclass
class SmeltingBlock(BlockEntity, CustomName, Lock):
    burnTime: int
    cookTime: int
    cookTimeTotal: int
    items: list[Item]
    recipesUsed: int


@dataclass
class BlastFurnace(SmeltingBlock):
    pass


@dataclass
class Furnace(SmeltingBlock):
    pass


@dataclass
class Smoker(SmeltingBlock):
    pass


@dataclass
class Jigsaw(BlockEntity):
    finalState: str
    joint: str
    name: str
    pool: str
    target: str


@dataclass
class Jukebox(BlockEntity):
    recordItem: Item


@dataclass
class Lectern(BlockEntity):
    book: Item
    page: int


@dataclass
class mobSpawner(BlockEntity):
    delay: int
    maxNearbyEntities: int
    maxSpawnDelay: int
    minSpawnDelay: int
    requiredPlayerRange: int
    spawnCount: int
    spawnData: nbt.NBTFile
    spawnPotentials:
    spawnRange: int


@dataclass
class Piston(BlockEntity):
    blockStates:
    extending: bool
    facing: int
    progress: float
    source: bool


@dataclass
class Sign(BlockEntity):
    glowingText: bool
    color: str
    text1: str
    text2: str
    text3: str
    text4: str


@dataclass
class Skull(BlockEntity):
    extraType: str
    skullOwner: SkullOwner


@dataclass
class SkullOwner:
    id: UUID
    name: str
    properties: list[Texture]


@dataclass
class Texture:
    value: str
    signature: str


@dataclass
class StructureBlock:
    author: str
    ignoreEntities: bool
    integrity: float
    metadata: str
    mirror: MirrorMode
    mode: StructureBlockMode
    name: str
    posX: int
    posY: int
    posZ: int
    powered: bool
    rotation: StructureBlockRotation
    seed: int
    showboundingbox: bool
    sizeX: int
    sizeY: int
    sizeZ: int


class StructureBlockRotation(Enum):
    CW0 = "NONE"
    CW90 = "CLOCKWISE_90"
    CW180 = "CLOCKWISE_180"
    CW270 = "COUNTERCLOCKWISE_90"


class StructureBlockMode(Enum):
    SAVE = "SAVE"
    LOAD = "LOAD"
    CORNER = "CORNER"
    DATA = "DATA"


class MirrorMode(Enum):
    NONE = "NONE"
    XAXIS = "LEFT_RIGHT"
    ZAXIS = "FRONT_BACK"
