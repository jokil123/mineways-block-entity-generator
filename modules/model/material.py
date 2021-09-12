from __future__ import annotations

import texture


class Material():
    def __init__(self, name: str) -> None:
        self.name = name
        self.properties: list[MaterialProperty] = []


# Holds a list of Materials
class MaterialLibrary():
    def __init__(self, materials: list[Material] = None) -> None:
        self.materials = materials or []
        self.textureHandler = texture.TextureHandler()


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
        self.map: texture.Texture
        self.mapPath: str

    def GenerateChannelInstructions(self) -> list[str]:
        instructions: list[str] = []

        if len(self.value) != 0:
            instructions.append(
                self.prefix + " " +
                " ".join(map(str, self.value))
            )

        try:
            instructions.append(
                "map_" + self.prefix + " " + self.mapPath
            )
        except:
            pass

        return instructions
