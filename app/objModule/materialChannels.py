from __future__ import annotations
from PIL import Image


class Material():
    def __init__(self, name: str) -> None:
        self.name = name
        self.properties: list[MaterialProperty] = []


class MaterialProperty():
    def __init__(self, prefix: str) -> None:
        self.prefix: str = prefix

    def GenerateChannelInstructions(self) -> list[str]:
        return [self.prefix]


class MaterialSetting(MaterialProperty):
    def __init__(self, prefix: str) -> None:
        super().__init__(prefix)
        self.value: list[int]

    def GenerateChannelInstructions(self) -> list[str]:
        return [self.prefix + " " + " ".join(map(str, self.value))]


class MaterialChannel(MaterialProperty):

    def __init__(self, prefix: str) -> None:
        super().__init__(prefix)
        self.value: list[float] = []
        self.map: Image
        self.mapPath: str

    def GenerateChannelInstructions(self) -> list[str]:
        instructions: list[str] = []

        if len(self.value) != 0:
            instructions.append(
                self.prefix + " " +
                " ".join(map(str, self.value))
            )

        try:
            self.map
        except:
            try:
                instructions.append(
                    "map_" + self.prefix + " " + self.mapPath
                )
            except:
                pass

        return instructions


class TextureHandler:
    def __init__(self) -> None:
        self.textures: list[Texture] = []

    def LoadTexture(self, path: str) -> Texture:
        texture = filter(lambda x: x.path == path, self.textures)

        if len(texture) == 0:

    def OpenImage(self, path: str) -> Image.Image:
        pass


class Texture:
    def __init__(self, name: str, path: str, texture: Image.Image) -> None:
        self.name = name
        self.path = path
        self.texture = texture
