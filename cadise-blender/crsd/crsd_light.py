from .crsd_creator import LightCreator
from .crsd_data import (
    SdData,
    SdDataUnit
)
from .crsd_type import (
    CrsdReal,
    CrsdVector3r
)

class PointLightCreator(LightCreator):
    def __init__(self):
        super(PointLightCreator, self).__init__()

        self.type     = "point"
        self.position = CrsdVector3r()
        self.color    = CrsdVector3r()
        self.watt     = CrsdReal() 
    
    def to_sd_data(self):
        sd_data = SdData(super(PointLightCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("position", "vector3r", self.position.to_string()))
        sd_data.add_data_unit(SdDataUnit("color", "rgb", self.color.to_string()))
        sd_data.add_data_unit(SdDataUnit("watt", "real", self.watt.to_string()))

        return sd_data

    def set_position(self, position):
        self.position = position
    
    def set_color(self, color: CrsdVector3r):
        self.color = color
    
    def set_watt(self, watt: CrsdReal):
        self.watt = watt

class AreaLightCreator(LightCreator):
    def __init__(self):
        super(AreaLightCreator, self).__init__()

        self.type      = "area"
        self.primitive = ""
        self.color     = CrsdVector3r()
        self.watt      = CrsdReal()
    
    def to_sd_data(self):
        sd_data = SdData(super(AreaLightCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("primitive", "primitive", self.primitive))
        sd_data.add_data_unit(SdDataUnit("color", "rgb", self.color.to_string()))
        sd_data.add_data_unit(SdDataUnit("watt", "real", self.watt.to_string()))

        return sd_data

    def set_primitive(self, primitive_name):
        self.primitive = primitive_name
    
    def set_color(self, color: CrsdVector3r):
        self.color = color
    
    def set_watt(self, watt: CrsdReal):
        self.watt = watt