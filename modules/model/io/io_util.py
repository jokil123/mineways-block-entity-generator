from __future__ import annotations

import re

from pathlib import Path


# Test if an obj instruction is the requested one
def IsInstruction(instructionName: str, instruction: str) -> bool:
    return bool(re.search("^(" + instructionName + ") .*$", instruction))


# Saves a raw file
def SaveFile(file: str, path: str, ext: str):
    Path("/".join(path.split("/")[:-1])).mkdir(parents=True, exist_ok=True)
    f = open(path + "." + ext, "w")
    f.write(file)
    f.close()
