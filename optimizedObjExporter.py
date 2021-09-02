import PIL
import re


class Vert():
    def __init__(self, x: float, y: float, z: float, object: str = None, group: str = None, materialSelection: str = None) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.objectLabel = object
        self.group = group
        self.materialSelection = materialSelection


class UvVert():
    def __init__(self, u: float, v: float) -> None:
        self.u = u
        self.v = v


class Face():
    def __init__(self, triangulation: list[int], uv: list[int]) -> None:
        self.triangulation = triangulation
        self.uv = uv


class MaterialLibrary():
    def __init__(self, map_Kd=None) -> None:
        self.map_Kd = map_Kd


class ObjModel():
    def __init__(self, verts: list[Vert] = [], faces: list[Face] = [], uvVerts: list[UvVert] = [], materialLibrary=MaterialLibrary()) -> None:
        self.verts = verts
        self.faces = faces
        self.uvVerts = uvVerts
        self.MaterialLibrary: materialLibrary = materialLibrary


class ObjModelExporter():
    def __init__(self) -> None:
        self.objModels: list[ObjModel] = []

    def AddObjModel(self, objModel):
        pass

    def Save(self, path):
        pass


def IsInstruction(instructionName: str, instruction: str) -> bool:
    return bool(re.search("^(" + instructionName + ") .*$", instruction))


def LoadModel(file: str) -> ObjModel:
    objFile = open(file, "r").read()
    objInstructions = objFile.splitlines()

    obj = ObjModel()

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

        elif IsInstruction("g", instruction):
            currentGroup = instructionParams[0]

        elif IsInstruction("usemtl", instruction):
            currentMaterialSelection = instructionParams[0]

        elif IsInstruction("vt", instruction):
            uv = UvVert(float(instructionParams[0]), float(
                instructionParams[1]))
            obj.uvVerts.append(uv)

        elif IsInstruction("v", instruction):
            vert = Vert(
                float(instructionParams[0]),
                float(instructionParams[1]),
                float(instructionParams[2]),
                currentObject, currentGroup, currentMaterialSelection)

            obj.verts.append(vert)

    return obj


obj = LoadModel("schematics/3d/tileEntities/tileEntities.obj")
