from .crsd_data import (
    SdData,
    SdDataUnit
)

from abc import (
    ABC,
    abstractmethod
)

class Creator(ABC):
    def __init__(self):
        super(Creator, self).__init__()
    
    @abstractmethod
    def to_sd_data(self):
        pass

class FilmCreator(Creator):
    def __init__(self):
        super(FilmCreator, self).__init__()

        self.sd_type         = "film"
        self.image_width     = 0
        self.image_height    = 0
        self.output_filename = ""
        self.filter_type     = ""

    def to_sd_data(self):
        sd_data = SdData(self.sd_type)
        sd_data.add_data_unit(SdDataUnit("image-width", "int32", self.image_width))
        sd_data.add_data_unit(SdDataUnit("image-height", "int32", self.image_height))
        sd_data.add_data_unit(SdDataUnit("output-filename", "string", self.output_filename))
        sd_data.add_data_unit(SdDataUnit("filter", "string", self.filter_type))

        return sd_data

    def set_image_width(self, image_width):
        self.image_width = image_width
    
    def set_image_height(self, image_height):
        self.image_height = image_height
    
    def set_output_filename(self, output_filename):
        self.output_filename = output_filename
    
    def set_filter(self, filter_type):
        self.filter_type = filter_type

class AcceleratorCreator(Creator):
    def __init__(self):
        super(AcceleratorCreator, self).__init__()
    
        self.sd_type = "accelerator"
        self.type    = "bvh"
    
    def to_sd_data(self):
        sd_data = SdData(self.sd_type)
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))

        return sd_data

class RendererCreator(Creator):
    def __init__(self):
        super(RendererCreator, self).__init__()

        self.sd_type       = "renderer"
        self.type          = "sampling"
        self.sample_number = 0
        self.sampler       = ""
        self.integrator    = ""
    
    def to_sd_data(self):
        sd_data = SdData(self.sd_type)
        sd_data.add_data_unit(SdDataUnit("type", "string", self.type))
        sd_data.add_data_unit(SdDataUnit("sample-number", "int32", self.sample_number))
        sd_data.add_data_unit(SdDataUnit("sampler", "string", self.sampler))
        sd_data.add_data_unit(SdDataUnit("integrator", "string", self.integrator))

        return sd_data
    
    def set_render_method(self, render_method):
        self.integrator = render_method
    
    def set_sample_number(self, sample_number):
        self.sample_number = sample_number
    
    def set_sampler(self, sampler):
        self.sampler = sampler

class CameraCreator(Creator):
    def __init__(self):
        super(CameraCreator, self).__init__()

        self.sd_type = "camera"
    
    def get_sd_type(self):
        return self.sd_type

    @abstractmethod
    def to_sd_data(self):
        pass

class MaterialCreator(Creator):
    def __init__(self):
        super(MaterialCreator, self).__init__()

        self.sd_type = "material"
    
    def get_sd_type(self):
        return self.sd_type

    @abstractmethod
    def to_sd_data(self):
        pass  

class MeshCreator(Creator):
    def __init__(self):
        super(MeshCreator, self).__init__()

        self.sd_type = "primitive"
    
    def get_sd_type(self):
        return self.sd_type

    @abstractmethod
    def to_sd_data(self):
        pass  

class LightCreator(Creator):
    def __init__(self):
        super(LightCreator, self).__init__()

        self.sd_type = "light"
    
    def get_sd_type(self):
        return self.sd_type

    @abstractmethod
    def to_sd_data(self):
        pass    