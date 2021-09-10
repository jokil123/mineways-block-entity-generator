from __future__ import annotations

from PIL import Image

from randomError.randomError import RandomError
from pathTools.pathTools import PathTools


class TextureHandler:
    def __init__(self) -> None:
        self.textures: list[Texture] = []

    def LoadTexture(self, path: str) -> Texture:
        textures = list(filter(lambda x: x.path == path, self.textures))

        if len(textures) == 0:
            newTexture = self.CreateTexture(path)
            self.textures.append(newTexture)
            return newTexture
        elif len(textures) == 1:
            return textures[0]
        else:
            raise RandomError()

    def OpenImage(self, path: str) -> Image.Image:
        return Image.open(path).copy()

    def CreateTexture(self, path) -> Texture:
        return Texture(PathTools(path).Name(), PathTools(path).Path(), self.OpenImage(path))


class Texture:
    def __init__(self, name: str, path: str, texture: Image.Image) -> None:
        self.name = name
        self.path = path
        self.texture = texture
