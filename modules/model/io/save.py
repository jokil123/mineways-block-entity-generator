from __future__ import annotations


from .. import mesh
from .. import material
from .io_util import SaveFile

from path_tools import PathTools


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
