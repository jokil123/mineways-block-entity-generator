from nbt import nbt, region, world


class TileEntity():
    def __init__(self, x, y, z, id):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

    def generateMesh():
        pass


class Bed(TileEntity):
    pass


def main():
    tileEntityObjects = []

    filePath = "schematics/tileEntities.schematic"

    nbtFile = nbt.NBTFile(filename=filePath)

    for tag in nbtFile.tags:
        if tag.name == "TileEntities":
            tileEntities = tag.tags

    tileEntityTypes = []

    for tileEntity in tileEntities:

        for tag in tileEntity.tags:
            if tag.name == "id":
                tileEntityTypes.append(tag.value)
                continue

    uniqueTileEntityTypes = set(tileEntityTypes)

    print(uniqueTileEntityTypes)


if __name__ == "__main__":
    main()
