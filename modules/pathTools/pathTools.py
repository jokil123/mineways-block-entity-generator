from __future__ import annotations
from ast import parse
from enum import Enum, auto
import os
from pathlib import Path as pathLibPath


class Path:
    def __init__(self, path: str) -> None:
        self.__path = self.__ParsePath(path)

        self.__isFile: bool = self.IsFile()
        self.__fileExt: str

    def __ParsePath(self, pathStr: str) -> list[str]:
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

    @staticmethod
    def JoinPath(rootPath: str, subPath: str) -> str:
        pathSegments = rootPath.split("/")[0:-1]
        pathSegments.append(subPath)
        newPath = "/".join(pathSegments)
        return newPath

    def IsFile(self) -> bool:
        return os.path.isfile(self.Path())

    def IsDir(self) -> bool:
        return os.path.isdir(self.Path())

    def Exists(self) -> bool:
        return os.path.exists(self.Path())

    def Create(self) -> str:
        if not self.Exists():
            pathLibPath(self.Dir()).mkdir(parents=True, exist_ok=True)
        return self.Path()

    def Name(self) -> str:
        return self.__path[-1]

    def Dir(self) -> str:
        return "/".join(self.__path[:-1])

    def Path(self) -> str:
        return "/".join(self.__path)


print(Path("abc").Exists())
