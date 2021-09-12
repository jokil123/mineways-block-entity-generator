from __future__ import annotations

import mesh
import material

from modules.model.io.io_util import IsInstruction
from io_util import IsInstruction
from path_tools import PathTools


# Loads an obj model and returns it
def LoadModel(file: str) -> mesh.ObjModel:
    objFile = open(file, "r").read()
    objInstructions = objFile.splitlines()

    obj = mesh.ObjModel()

    currentObject = None
    currentGroup = None
    currentMaterialSelection = None

    mtllibs: list[str] = []

    for instruction in objInstructions:
        if instruction == "":
            continue

        instructionParams = instruction.split()[1:]

        if IsInstruction("mtllib", instruction):
            mtllibs.append(instructionParams[0])

        elif IsInstruction("o", instruction):
            currentObject = instructionParams[0]
            obj.objectLabels.add(instructionParams[0])

        elif IsInstruction("g", instruction):
            currentGroup = instructionParams[0]
            obj.groupLabels.add(instructionParams[0])

        elif IsInstruction("usemtl", instruction):
            currentMaterialSelection = instructionParams[0]

        elif IsInstruction("vt", instruction):
            uv = mesh.UvVertex([float(instructionParams[0]),
                                float(instructionParams[1])])
            obj.uvVerts.append(uv)

        elif IsInstruction("vn", instruction):
            vertexNormal = mesh.VertexNormal([float(instructionParams[0]),
                                              float(instructionParams[1]),
                                              float(instructionParams[2])])
            obj.vertexNormals.append(vertexNormal)

        elif IsInstruction("v", instruction):
            vertex = mesh.Vertex([float(instructionParams[0]),
                                  float(instructionParams[1]),
                                  float(instructionParams[2])])

            obj.verts.append(vertex)

        elif IsInstruction("f", instruction):
            face = mesh.Face(object=currentObject,
                             group=currentGroup,
                             materialSelection=currentMaterialSelection)

            for parameter in instructionParams:
                args = parameter.split("/")

                face.triangulation.append(obj.verts[int(args[0]) - 1])

                try:
                    face.uv.append(obj.uvVerts[int(args[1]) - 1])
                except:
                    pass
                try:
                    face.normal.append(obj.vertexNormals[int(args[2]) - 1])
                except:
                    pass

            obj.faces.append(face)

    for mtllib in mtllibs:
        path = PathTools.JoinPath(file, mtllib)
        obj.MaterialLibrary = LoadMaterialLibrary(path)

    return obj


# Loads a Material Library
def LoadMaterialLibrary(path: str) -> material.MaterialLibrary:
    mtllib = material.MaterialLibrary()

    mtlFile = open(path, "r").read()
    mtlInstructions = mtlFile.splitlines()

    currentMaterial = material.Material("I HATE MYSELF")  # pls fix this

    for instruction in mtlInstructions:
        instructionParams = instruction.split()[1:]

        if instruction == "":
            continue

        elif IsInstruction("newmtl", instruction):
            currentMaterial = material.Material(instructionParams[0])
            mtllib.materials.append(currentMaterial)

        elif IsInstruction("illum", instruction):
            matChan = material.MaterialSetting("illum")
            matChan.value = [int(instructionParams[0])]
            currentMaterial.properties.append(matChan)

        channels: list = ["Ka", "Kd", "Ks", "Ns", "d", "Tf"]

        # This will instantiate material properties/channels twice (fix this)
        for channel in channels:
            matChan = material.MaterialChannel(channel)
            channelExists = False

            if IsInstruction(channel, instruction):
                matChan.value = list(map(float, instructionParams))
                channelExists = True
            if IsInstruction("map_" + channel, instruction):
                matChan.mapPath = instructionParams[0]
                matChan.map = mtllib.textureHandler.LoadTexture(
                    PathTools.JoinPath(path, matChan.mapPath))
                channelExists = True

            if channelExists:
                currentMaterial.properties.append(matChan)

    return mtllib
