from .crsd_creator import MeshCreator
from .crsd_data import (
    SdData,
    SdDataUnit
)
from .crsd_type import CrsdVector3rArray

class TriangleMeshCreator(MeshCreator):
    def __init__(self):
        super(TriangleMeshCreator, self).__init__()

        self.__type      = "triangle-mesh"
        self.__name      = ""
        self.__material  = ""
        self.__positions = CrsdVector3rArray()
        self.__normals   = CrsdVector3rArray()
        self.__uvws      = CrsdVector3rArray()
    
    def to_sd_data(self):
        sd_data = SdData(super(TriangleMeshCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.__type))
        sd_data.add_data_unit(SdDataUnit("name", "string", self.__name))
        sd_data.add_data_unit(SdDataUnit("bsdf", "material", self.__material))
        sd_data.add_data_unit(SdDataUnit("positions", "vector3r-array", self.__positions.to_string()))
        sd_data.add_data_unit(SdDataUnit("normals", "vector3r-array", self.__normals.to_string()))
        sd_data.add_data_unit(SdDataUnit("uvws", "vector3r-array", self.__uvws.to_string()))

        return sd_data
    
    def set_name(self, name):
        self.__name = name
    
    def set_material(self, material):
        self.__material = material
    
    def set_positions(self, positions: CrsdVector3rArray):
        self.__positions = positions
    
    def set_normals(self, normals: CrsdVector3rArray):
        self.__normals = normals

    def set_uvws(self, uvws: CrsdVector3rArray):
        self.__uvws = uvws