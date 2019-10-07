from .crsd_creator import MaterialCreator
from .crsd_data import (
    SdData,
    SdDataUnit
)
from .crsd_type import CrsdVector3r

class LambertianDiffuseCreator(MaterialCreator):
    def __init__(self):
        super(LambertianDiffuseCreator, self).__init__()

        self.__type   = "matte-lambertian"
        self.__albedo = CrsdVector3r()
    
    def to_sd_data(self):
        sd_data = SdData(super(LambertianDiffuseCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.__type))
        sd_data.add_data_unit(SdDataUnit("albedo", "rgb", self.__albedo.to_string()))

        return sd_data
    
    def set_albedo(self, albedo: CrsdVector3r):
        self.__albedo = albedo