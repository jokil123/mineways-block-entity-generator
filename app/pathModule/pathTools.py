from __future__ import annotations
from ast import parse
from enum import Enum, auto


class Path:
    def __init__(self, path: str) -> None:
        self.__path = self.__ParsePath(path)

        self.__type: PathType
        self.__fileExt: str

    def __ParsePath(self, pathStr) -> list[str]:
        path: list[str] = []

        for sPathSegment in pathStr.split("/"):
            path.extend(sPathSegment.split("\\"))

        """
        filteredPath: list[str] = []

        for pathSegment in path:
            if len(pathSegment) != 0:
                filteredPath.append(pathSegment)

        return filteredPath
        """

        return path

    def Name(self) -> str:
        return self.__path[-1]

    def Dir(self) -> str:
        return "/".join(self.__path[:-1])

    def Path(self) -> str:
        return "/".join(self.__path)

    def FileExt(self) -> str:
        pass


class PathType(Enum):
    DIRECTORY = auto()
    FILE = auto()
    COMPOUND = auto()


print(Path("../../abc/def/").Name())
