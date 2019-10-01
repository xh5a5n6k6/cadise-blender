from . import (
    light,
    material,
    mesh
)
from ...base import (
    helper,
    stream
)
from ...crsd.creator import (
    AcceleratorCreator,
    FilmCreator,
    RendererCreator
)
from ...crsd.camera import PerspectiveCameraCreator

import bpy
import math
import mathutils
import sys

class CrsdExporter:
    def __init__(self, filename):
        self.__filename = filename
        self.__filestream = None

    def begin(self, file_path):
        helper.create_folder(file_path)
        
        file_full_name = helper.get_file_full_name(file_path, self.__filename)
        self.__filestream = stream.FileStream(file_full_name)
        self.__filestream.write_default_info()

    def end(self):
        print("Finish exporting")

    def export(self, depsgraph: bpy.types.Depsgraph):
        scene = depsgraph.scene

        # export render setting
        self.__filestream.write_string(
            "###########################################\n" +
            "# Render Setting                          #\n" +
            "###########################################\n"
        )
        self.__export_global_setting(scene)
        self.__filestream.write_string("\n")
        
        # export world setting
        self.__filestream.write_string(
            "###########################################\n" +
            "# World Setting                           #\n" +
            "###########################################\n"
        )
        self.__export_world_setting(depsgraph)
    
    def __export_global_setting(self, scene: bpy.types.Scene):
        self.__export_film(scene)
        self.__export_camera(scene)
        self.__export_renderer(scene)
        self.__export_accelerator(scene)

    def __export_world_setting(self, depsgraph: bpy.types.Depsgraph):
        self.__export_material(depsgraph)
        self.__export_mesh(depsgraph)
        self.__export_light(depsgraph)

    def __export_film(self, scene: bpy.types.Scene):
        resolution_x = scene.render.resolution_x
        resolution_y = scene.render.resolution_y
        output_filename = self.__filename + ".jpg"
        filter_type = helper.get_filter_type(scene.cadise_render_filter_type)

        filmCreator = FilmCreator()
        filmCreator.set_image_width(resolution_x)
        filmCreator.set_image_height(resolution_y)
        filmCreator.set_output_filename(output_filename)
        filmCreator.set_filter(filter_type)

        self.__filestream.write_sd_data(filmCreator.to_sd_data())

    def __export_camera(self, scene: bpy.types.Scene):
        camera_obj = helper.get_active_camera(scene)
        camera_data = camera_obj.data
        
        if camera_data.type == 'PERSP':
            position, rotation, scale = camera_obj.matrix_world.decompose()
            if(abs(scale.x - 1) > sys.float_info.epsilon or
               abs(scale.y - 1) > sys.float_info.epsilon or
               abs(scale.z - 1) > sys.float_info.epsilon):
               
               print("Unsupport scale camera.")
               return
            
            up = rotation @ mathutils.Vector((0, 1, 0))
            direction = rotation @ mathutils.Vector((0, 0, -1))

            look_at = "{:.6f} {:.6f} {:.6f}, " \
                      "{:.6f} {:.6f} {:.6f}, " \
                      "{:.6f} {:.6f} {:.6f}".format(
                          position.x, position.y, position.z,
                          direction.x, direction.y, direction.z,
                          up.x, up.y, up.z
                      )
            fov = math.degrees(camera_data.angle)

            perspectiveCameraCreator = PerspectiveCameraCreator()
            perspectiveCameraCreator.set_look_at(look_at)
            perspectiveCameraCreator.set_fov(fov)

            self.__filestream.write_sd_data(perspectiveCameraCreator.to_sd_data())

            # TODO: depth of field and lens system camera

        else:
            print("Unsupport other types of camera currently.")

    def __export_renderer(self, scene: bpy.types.Scene):
        sample_number = scene.cadise_render_spp
        sampler = helper.get_sampling_type(scene.cadise_render_sampling_type)
        render_method = helper.get_rendering_method(scene.cadise_render_rendering_method)

        rendererCreator = RendererCreator()
        rendererCreator.set_render_method(render_method)
        rendererCreator.set_sample_number(sample_number)
        rendererCreator.set_sampler(sampler)

        self.__filestream.write_sd_data(rendererCreator.to_sd_data())

    def __export_accelerator(self, scene: bpy.types.Scene):
        acceleratorCreator = AcceleratorCreator()

        self.__filestream.write_sd_data(acceleratorCreator.to_sd_data())

    def __export_material(self, depsgraph: bpy.types.Depsgraph):
        scene = depsgraph.scene_eval
        materials = helper.get_materials_from_meshes(scene)

        for mat in materials:
            material_sd_data = material.material_to_sd_data(mat)

            # if material_sd_data is not None:
            #     self.__filestream.write_sd_data(material_sd_data)

    def __export_mesh(self, depsgraph: bpy.types.Depsgraph):
        scene = depsgraph.scene_eval
        mesh_objs = helper.get_mesh_objects(scene)

        for mesh_obj in mesh_objs:
            pass

    def __export_light(self, depsgraph: bpy.types.Depsgraph):
        scene = depsgraph.scene_eval
        light_objs = helper.get_light_objects(scene)

        for light_obj in light_objs:
            pass