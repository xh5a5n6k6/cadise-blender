from .crsd_creator import MeshCreator
from .crsd_data import (
    SdData,
    SdDataUnit
)
from .crsd_type import (
    CrsdVector3r,
    CrsdVector3rArray
)

class TriangleMeshCreator(MeshCreator):
    def __init__(self):
        super(TriangleMeshCreator, self).__init__()

        self.type      = "triangle-mesh"
        self.name      = ""
        self.material  = ""
        self.positions = CrsdVector3rArray()
        self.normals   = CrsdVector3rArray()
        self.uvws      = CrsdVector3rArray()
    
    def to_sd_data(self):
        sd_data = SdData(super(TriangleMeshCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("name", "string", self.name))
        sd_data.add_data_unit(SdDataUnit("bsdf", "material", self.material))
        sd_data.add_data_unit(SdDataUnit("positions", "vector3r-array", self.positions.to_string()))
        sd_data.add_data_unit(SdDataUnit("normals", "vector3r-array", self.normals.to_string()))
        sd_data.add_data_unit(SdDataUnit("uvws", "vector3r-array", self.uvws.to_string()))

        return sd_data
    
    def set_name(self, name):
        self.name = name
    
    def set_material(self, material):
        self.material = material
    
    def set_positions(self, positions: CrsdVector3rArray):
        self.positions = positions
    
    def set_normals(self, normals: CrsdVector3rArray):
        self.normals = normals

    def set_uvws(self, uvws: CrsdVector3rArray):
        self.uvws = uvws

class RectangleCreator(MeshCreator):
    def __init__(self):
        super(RectangleCreator, self).__init__()

        self.type      = "rectangle"
        self.name      = ""
        self.material  = ""
        self.v1        = CrsdVector3r()
        self.v2        = CrsdVector3r()
        self.v3        = CrsdVector3r()

    def to_sd_data(self):
        sd_data = SdData(super(RectangleCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("name", "string", self.name))
        sd_data.add_data_unit(SdDataUnit("bsdf", "material", self.material))
        sd_data.add_data_unit(SdDataUnit("v1", "vector3r", self.v1.to_string()))
        sd_data.add_data_unit(SdDataUnit("v2", "vector3r", self.v2.to_string()))
        sd_data.add_data_unit(SdDataUnit("v3", "vector3r", self.v3.to_string()))

        return sd_data

    def set_name(self, name):
        self.name = name
    
    def set_material(self, material):
        self.material = material
    
    def set_v1(self, v1: CrsdVector3r):
        self.v1 = v1

    def set_v2(self, v2: CrsdVector3r):
        self.v2 = v2

    def set_v3(self, v3: CrsdVector3r):
        self.v3 = v3