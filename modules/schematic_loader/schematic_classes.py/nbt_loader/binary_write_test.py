from typing import ByteString


path = "modules/schematic_loader/schematic_classes.py/nbt_loader/"

f = open(path + "test", "wb")

fileBytes: bytearray = bytearray()
num = 9876
numBytes = num.to_bytes(2, "little")

fileBytes.extend(numBytes)

f.write(fileBytes)

f.close()
