from dataclasses import dataclass
from os import name

f = open("ids", "r").read()

outFile = []

block: dict[]

for i in range(len(f.splitlines())):
    if i % 3 == 0:
        blocks
