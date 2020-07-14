from .crsd_creator import AcceleratorCreator
from .crsd_data import (
    SdData,
    SdDataUnit
)
from .crsd_type import (
    CrsdReal,
    CrsdVector3r
)

class BvhAcceleratorCreator(AcceleratorCreator):
    def __init__(self):
        super(BvhAcceleratorCreator, self).__init__()

        self.type       = "bvh"
        self.split_mode = "equal"
    
    def to_sd_data(self):
        sd_data = SdData(super(BvhAcceleratorCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("split-mode", "string", self.split_mode))

        return sd_data
    
    def set_split_mode(self, split_mode):
        self.split_mode = split_mode

class KdTreeAcceleratorCreator(AcceleratorCreator):
    def __init__(self):
        super(KdTreeAcceleratorCreator, self).__init__()

        self.type       = "kd-tree"
        self.split_mode = "sah"
    
    def to_sd_data(self):
        sd_data = SdData(super(KdTreeAcceleratorCreator, self).get_sd_type())
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("split-mode", "string", self.split_mode))

        return sd_data
    
    def set_split_mode(self, split_mode):
        self.split_mode = split_mode