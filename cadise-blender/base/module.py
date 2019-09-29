from . import setting

from abc import (
    ABC,
    abstractmethod
)

import bpy
import importlib
import sys

class ModuleBase(ABC):
    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def unregister(self):
        pass

class SingleClassModule(ModuleBase):
    def __init__(self, cls):
        self.cls = cls
    
    def register(self):
        bpy.utils.register_class(self.cls)

    def unregister(self):
        bpy.utils.unregister_class(self.cls)

class ModuleManager:
    def __init__(self):
        self.modules = []

    def initialize(self, module_path):
        for module_name in setting.cadise_modules:
            module_full_name = "{}.{}".format(module_path, module_name)

            if module_full_name in sys.modules:
                importlib.reload(sys.modules[module_full_name])
            else:
                importlib.import_module(module_full_name)

            module = sys.modules[module_full_name]
            if hasattr(module, "include_submodule"):
                module.include_submodule(self)
            else:
                print("ERROR")

    def add_module(self, module):
        self.modules.append(module)
    
    def add_class(self, cls):
        self.add_module(SingleClassModule(cls))

    def register_all(self):
        for module in self.modules:
            module.register()
    
    def unregister_all(self):
        for module in self.modules:
            module.unregister()