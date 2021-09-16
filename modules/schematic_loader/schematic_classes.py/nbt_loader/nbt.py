from __future__ import annotations
import struct


class NbtTag:
    tagId: int

    def __init__(self, name: str, value) -> None:
        self.name = name

    def AsBinary(self) -> bytearray:
        bytes = bytearray()
        bytes.append(self.tagId)
        bytes.extend(len(self.name).to_bytes(2, "big"))
        bytes.extend(self.name.encode())
        bytes.extend(self.ValueAsBinary())

        return bytes

    def ValueAsBinary(self) -> bytearray:
        return bytearray()


class Byte(NbtTag):
    tagId = 1

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name, value)
        self.value = value

    def ValueAsBinary(self) -> bytearray:
        binaryValue = bytearray()
        binaryValue.extend(self.value.to_bytes(1, "big"))
        return binaryValue


class Short(NbtTag):
    tagId = 2

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name, value)
        self.value = value

    def ValueAsBinary(self) -> bytearray:
        binaryValue = bytearray()
        binaryValue.extend(self.value.to_bytes(2, "big"))
        return binaryValue


class Int(NbtTag):
    tagId = 3

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name, value)
        self.value = value

    def ValueAsBinary(self) -> bytearray:
        binaryValue = bytearray()
        binaryValue.extend(self.value.to_bytes(4, "big"))
        return binaryValue


class Long(NbtTag):
    tagId = 4

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name, value)
        self.value = value

    def ValueAsBinary(self) -> bytearray:
        binaryValue = bytearray()
        binaryValue.extend(self.value.to_bytes(8, "big"))
        return binaryValue


class Float(NbtTag):
    tagId = 5

    def __init__(self, name: str, value: float) -> None:
        super().__init__(name, value)
        self.value = value

    def ValueAsBinary(self) -> bytearray:
        binaryValue = bytearray()
        binaryValue.extend(self.value.to_bytes(4, "big"))
        return binaryValue
