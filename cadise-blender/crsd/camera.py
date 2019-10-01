from .creator import CameraCreator
from .data import (
    SdData,
    SdDataUnit
)

class PerspectiveCameraCreator(CameraCreator):
    def __init__(self):
        super(PerspectiveCameraCreator, self).__init__()

        self.__type    = "perspective"
        self.__look_at = ""
        self.__fov     = 0
    
    def to_sd_data(self):
        sd_data = SdData(super(PerspectiveCameraCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.__type))
        sd_data.add_data_unit(SdDataUnit("look-at", "vector3r-array", self.__look_at))
        sd_data.add_data_unit(SdDataUnit("fov", "real", self.__fov))

        return sd_data
    
    def set_look_at(self, look_at):
        self.__look_at = look_at
    
    def set_fov(self, fov):
        self.__fov = fov