from __future__ import annotations

from material import Material, MaterialLibrary


# Holds a vertex normal vector
class VertexNormal():
    def __init__(self, normal: list[float]) -> None:
        self.normal = normal or []


# Holds a vertex (3D Point)
class Vertex():
    def __init__(self, position: list[float]) -> None:
        self.position = position or []


# Holds a texture vertex (2D Point on a Texture)
class UvVertex():
    def __init__(self, uv: list[float]) -> None:
        self.uv = uv or []


# Holds a face (poly or n-gon).
class Face():
    def __init__(self, triangulation: list[int] = None, uv: list[int] = None, normal: list[int] = None, object: str = None, group: str = None, materialSelection: str = None) -> None:
        self.triangulation = triangulation or []
        self.uv = uv or []
        self.normal = normal or []
        self.objectLabel = object
        self.groupLabel = group
        self.materialSelection = materialSelection


# Holds all data of an OBJ file
class ObjModel():
    def __init__(self, verts: list[Vertex] = None, faces: list[Face] = None, uvVerts: list[UvVertex] = None, vertexNormals: list[VertexNormal] = None, materialLibrary: MaterialLibrary = None) -> None:
        self.verts = verts or []
        self.faces = faces or []
        self.uvVerts = uvVerts or []
        self.vertexNormals = vertexNormals or []
        self.MaterialLibrary = materialLibrary or MaterialLibrary()
        self.objectLabels: set[str] = set()
        self.groupLabels: set[str] = set()
