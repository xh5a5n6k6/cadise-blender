from .crsd_creator import CameraCreator
from .crsd_data import (
    SdData,
    SdDataUnit
)
from .crsd_type import (
    CrsdReal,
    CrsdVector3r
)

class PerspectiveCameraCreator(CameraCreator):
    def __init__(self):
        super(PerspectiveCameraCreator, self).__init__()

        self.__type      = "perspective"
        self.__position  = CrsdVector3r()
        self.__direction = CrsdVector3r()
        self.__up        = CrsdVector3r()
        self.__fov       = CrsdReal()
    
    def to_sd_data(self):
        sd_data = SdData(super(PerspectiveCameraCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.__type))
        sd_data.add_data_unit(SdDataUnit("position", "vector3r", self.__position.to_string()))
        sd_data.add_data_unit(SdDataUnit("direction", "vector3r", self.__direction.to_string()))
        sd_data.add_data_unit(SdDataUnit("up", "vector3r", self.__up.to_string()))
        sd_data.add_data_unit(SdDataUnit("fov", "real", self.__fov.to_string()))

        return sd_data
    
    def set_position(self, position: CrsdVector3r):
        self.__position = position

    def set_direction(self, direction: CrsdVector3r):
        self.__direction = direction

    def set_up(self, up: CrsdVector3r):
        self.__up = up
    
    def set_fov(self, fov: CrsdReal):
        self.__fov = fov