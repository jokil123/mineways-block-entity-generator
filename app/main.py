from __future__ import annotations

from model.io.load import LoadModel
from model.io.save import SaveModel


def main():
    obj = LoadModel("tests/3d/tileEntities/tileEntities.obj")
    for texture in obj.MaterialLibrary.textureHandler.textures:
        print(texture.name)

    SaveModel(obj, "export/yourMum")


if __name__ == "__main__":
    main()
