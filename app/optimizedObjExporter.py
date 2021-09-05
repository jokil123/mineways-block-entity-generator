from PIL import Image
import re


class VertexNormal():
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


class Vertex():
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


class UvVertex():
    def __init__(self, u: float, v: float) -> None:
        self.u = u
        self.v = v


class Face():
    def __init__(self, triangulation: list[int] = None, uv: list[int] = None, normal: list[int] = None, object: str = None, group: str = None, materialSelection: str = None) -> None:
        self.triangulation = triangulation or []
        self.uv = uv or []
        self.normal = normal or []
        self.objectLabel = object
        self.group = group
        self.materialSelection = materialSelection


class MaterialMap:
    def __init__(self, rgb: list[float] = None, map: Image = None) -> None:
        self.rgb = rgb or []
        self.map = map or Image.new(mode="RGBA", size=(1, 1))


class Material():
    def __init__(self, name: str, ambient: MaterialMap = None, diffuse: MaterialMap = None, specular: MaterialMap = None, specularWeight: MaterialMap = None, dissolve: MaterialMap = None, illum: float = None) -> None:
        self.name = name
        self.ambient = ambient or MaterialMap()
        self.diffuse = diffuse or MaterialMap()
        self.specular = specular or MaterialMap()
        self.specularWeight = specularWeight or MaterialMap()
        self.dissolve = dissolve or MaterialMap()
        self.illum = illum or 0


class MaterialLibrary():
    def __init__(self, materials: list[Material] = None) -> None:
        self.materials = materials or []


class ObjModel():
    def __init__(self, verts: list[Vertex] = None, faces: list[Face] = None, uvVerts: list[UvVertex] = None, vertexNormals: list[VertexNormal] = None, materialLibrary: MaterialLibrary = None) -> None:
        self.verts = verts or []
        self.faces = faces or []
        self.uvVerts = uvVerts or []
        self.vertexNormals = vertexNormals or []
        self.MaterialLibrary = materialLibrary or MaterialLibrary()


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
            uv = UvVertex(float(instructionParams[0]), float(
                instructionParams[1]))
            obj.uvVerts.append(uv)

        elif IsInstruction("vn", instruction):
            vertexNormal = VertexNormal(float(instructionParams[0]),
                                        float(instructionParams[1]),
                                        float(instructionParams[2]))
            obj.vertexNormals.append(vertexNormal)

        elif IsInstruction("v", instruction):
            vertex = Vertex(
                float(instructionParams[0]),
                float(instructionParams[1]),
                float(instructionParams[2]),)

            obj.verts.append(vertex)

        elif IsInstruction("f", instruction):
            face = Face(object=currentObject,
                        group=currentGroup,
                        materialSelection=currentMaterialSelection)

            for parameter in instructionParams:
                args = parameter.split("/")

                face.triangulation.append(int(args[0]))
                try:
                    face.uv.append(int(args[1]))
                except:
                    pass
                try:
                    face.normal.append(int(args[2]))
                except:
                    pass

            obj.faces.append(face)

        for mtllib in mtllibs:
            path = JoinPath(file, mtllib)
            obj.MaterialLibrary = LoadMaterialLibrary(path)

    return obj


def JoinPath(rootPath: str, subPath: str) -> str:
    pathSegments = rootPath.split("/")[0:-1]
    pathSegments.append(subPath)
    newPath = "/".join(pathSegments)
    return newPath


def LoadMaterialLibrary(path: str) -> MaterialLibrary:
    mtllib = MaterialLibrary()

    mtlFile = open(path, "r").read()
    mtlInstructions = mtlFile.splitlines()

    currentMaterial: Material

    for instruction in mtlInstructions:

        pass

    return mtllib


obj = LoadModel("schematics/3d/tileEntities/tileEntities.obj")
