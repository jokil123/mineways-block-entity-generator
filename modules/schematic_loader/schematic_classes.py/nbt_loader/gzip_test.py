import gzip

f = open("tests/schematics/tileEntities.schematic", "rb").read()

fd = gzip.decompress(f)

outFile = open(
    "tests/schematics/tileEntities.decompressed", "wb")

outFile.write(fd)
outFile.close()
