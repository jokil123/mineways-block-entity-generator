from __future__ import annotations

import re
from pathlib import Path


import mesh

import material

from pathTools.pathTools import PathTools


# Test if an obj instruction is the requested one
def IsInstruction(instructionName: str, instruction: str) -> bool:
    return bool(re.search("^(" + instructionName + ") .*$", instruction))


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


# Saves a Model
def SaveModel(model: mesh.ObjModel, path: str, mtlPath: str = None) -> None:
    instructions: list[str] = []

    if not mtlPath:
        mtlPath = path.split("/")[-1]
    instructions.append("mtllib " + mtlPath + ".mtl")
    SaveMaterialLibrary(model.MaterialLibrary,
                        PathTools.JoinPath(path, mtlPath))

    for vertexNormal in model.vertexNormals:
        command = "vn " + " ".join(map(str, vertexNormal.normal))
        instructions.append(command)

    for uvVert in model.uvVerts:
        command = "vt " + " ".join(map(str, uvVert.uv))
        instructions.append(command)

    for vert in model.verts:
        command = "v " + " ".join(map(str, vert.position))
        instructions.append(command)

    faceList = model.faces.copy()

    for objectLabel in model.objectLabels:
        objectFaceList = list(filter(
            lambda i: i.objectLabel == objectLabel, faceList))
        faceList = list(set(faceList) - set(objectFaceList))

        if len(objectFaceList) != 0:
            instructions.append("o " + objectLabel)

            for groupLabel in model.groupLabels:
                groupFaceList = list(filter(
                    lambda i: i.groupLabel == groupLabel, objectFaceList))
                objectFaceList = list(set(objectFaceList) - set(groupFaceList))

                if len(groupFaceList) != 0:
                    instructions.append("g " + groupLabel)

                    for materialLabel in map(lambda i: i.name, model.MaterialLibrary.materials):
                        materialFaceList = list(filter(
                            lambda i: i.materialSelection == materialLabel, groupFaceList))

                        groupFaceList = list(set(groupFaceList) -
                                             set(materialFaceList))

                        if len(materialFaceList) != 0:
                            instructions.append("usemtl " + materialLabel)

                            for face in materialFaceList:
                                instructions.append(
                                    CreateFaceInstruction(face, model))

                    else:
                        if len(groupFaceList) != 0:
                            instructions.append("usemtl None")
                            for face in groupFaceList:
                                instructions.append(
                                    CreateFaceInstruction(face, model))
            else:
                if len(objectFaceList) != 0:
                    instructions.append("g None")
                    for face in objectFaceList:
                        instructions.append(CreateFaceInstruction(face, model))
        else:
            if len(faceList) != 0:
                instructions.append("o None")
                for face in faceList:
                    instructions.append(CreateFaceInstruction(face, model))

    SaveFile("\n".join(instructions), path, "obj")


# Saves a Material Library
def SaveMaterialLibrary(mtllib: material.MaterialLibrary, path: str) -> None:
    mtllib.textureHandler.SaveTextures(path)

    instructions: list[str] = []

    for material in mtllib.materials:
        instructions.append("newmtl " + material.name)
        for property in material.properties:
            instructions.extend(property.GenerateChannelInstructions())

    SaveFile("\n".join(instructions), path, "mtl")


# Creates OBJ instruction for a face
def CreateFaceInstruction(face: mesh.Face, model: mesh.ObjModel) -> str:
    command = "f"

    for i in range(len(face.triangulation)):
        args: list[str] = []

        args.append(str(model.verts.index(face.triangulation[i]) + 1))

        if len(face.normal) != 0:
            if len(face.uv) != 0:
                args.append(str(model.uvVerts.index(face.uv[i]) + 1))
            else:
                args.append("")
            args.append(str(model.vertexNormals.index(face.normal[i]) + 1))
        elif len(face.uv) != 0:
            args.append(str(model.uvVerts.index(face.uv[i]) + 1))

        command += " " + "/".join(args)

    return command


# Saves a raw file
def SaveFile(file: str, path: str, ext: str):
    Path("/".join(path.split("/")[:-1])).mkdir(parents=True, exist_ok=True)
    f = open(path + "." + ext, "w")
    f.write(file)
    f.close()


def main():
    obj = LoadModel("tests/3d/tileEntities/tileEntities.obj")
    for texture in obj.MaterialLibrary.textureHandler.textures:
        print(texture.name)

    SaveModel(obj, "export/yourMum")


if __name__ == "__main__":
    main()
