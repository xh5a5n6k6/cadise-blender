from ...base import (
    helper,
    stream
)

import bpy

class CrsdExporter:
    def __init__(self):
        self.__filestream = None

    def begin(self, file_path, file_name):
        helper.create_folder(file_path)
        
        file_full_name = helper.get_file_full_name(file_path, file_name)
        self.__filestream = stream.FileStream(file_full_name)
        self.__filestream.write_default_info()

    def end(self):
        pass

    def export(self, scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph):
        pass

    # def export_camera(self):
    #     pass

    # def export_integrator(self):
    #     pass

    # def export_filter(self):
    #     pass

    # def export_primitive(self):
    #     pass

    # def export_light(self):
    #     pass