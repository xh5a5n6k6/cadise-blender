from .crsd_creator import CameraCreator
from .crsd_data import (
    SdData,
    SdDataUnit
)
from .crsd_type import (
    CrsdReal,
    CrsdVector3r
)

class PerspectivePinholeCameraCreator(CameraCreator):
    def __init__(self):
        super(PerspectivePinholeCameraCreator, self).__init__()

        self.type      = "perspective-pinhole"
        self.position  = CrsdVector3r()
        self.direction = CrsdVector3r()
        self.up        = CrsdVector3r()
        self.fov       = CrsdReal()
    
    def to_sd_data(self):
        sd_data = SdData(super(PerspectivePinholeCameraCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("position", "vector3r", self.position.to_string()))
        sd_data.add_data_unit(SdDataUnit("direction", "vector3r", self.direction.to_string()))
        sd_data.add_data_unit(SdDataUnit("up", "vector3r", self.up.to_string()))
        sd_data.add_data_unit(SdDataUnit("fov", "real", self.fov.to_string()))

        return sd_data
    
    def set_position(self, position: CrsdVector3r):
        self.position = position

    def set_direction(self, direction: CrsdVector3r):
        self.direction = direction

    def set_up(self, up: CrsdVector3r):
        self.up = up
    
    def set_fov(self, fov: CrsdReal):
        self.fov = fov