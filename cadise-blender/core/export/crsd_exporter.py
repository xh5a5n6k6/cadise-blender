from . import (
    light,
    material,
    mesh
)
from ...base import (
    helper,
    stream
)
from ...crsd.crsd_camera import PerspectiveCameraCreator
from ...crsd.crsd_creator import (
    AcceleratorCreator,
    FilmCreator,
    RendererCreator
)
from ...crsd.crsd_type import (
    CrsdReal,
    CrsdVector3r
)

import bpy
import math
import mathutils

class CrsdExporter:
    def __init__(self, filename):
        self.filename = filename
        self.filestream = None

    def begin(self, file_path):
        helper.create_folder(file_path)
        
        file_full_name = helper.get_file_full_name(file_path, self.filename)
        self.filestream = stream.FileStream(file_full_name)
        self.filestream.write_default_info()

    def end(self):
        print("Finish exporting")

    def export(self, depsgraph: bpy.types.Depsgraph):
        scene = depsgraph.scene

        # export render setting
        self.filestream.write_string(
            "###########################################\n" +
            "# Render Setting                          #\n" +
            "###########################################\n"
        )
        self.export_global_setting(scene)
        self.filestream.write_string("\n")
        
        # export world setting
        self.filestream.write_string(
            "###########################################\n" +
            "# World Setting                           #\n" +
            "###########################################\n"
        )
        self.export_world_setting(depsgraph)
    
    def export_global_setting(self, scene: bpy.types.Scene):
        self.export_film(scene)
        self.export_camera(scene)
        self.export_renderer(scene)
        self.export_accelerator(scene)

    def export_world_setting(self, depsgraph: bpy.types.Depsgraph):
        scene = depsgraph.scene_eval
        
        mesh_objs = helper.get_mesh_objects(scene)
        materials = helper.get_materials_from_meshes(mesh_objs)
        light_objs = helper.get_light_objects(scene)

        for material in materials:
            pass
            # TODO: material node system
            # material.material_export_sd(material, self.filestream)

        for mesh_obj in mesh_objs:
            mesh.mesh_export_sd(mesh_obj, self.filestream)

        for light_obj in light_objs:
            light.light_export_sd(light_obj, self.filestream)

    def export_film(self, scene: bpy.types.Scene):
        resolution_percentage = scene.render.resolution_percentage / 100.0
        resolution_x = int(scene.render.resolution_x * resolution_percentage)
        resolution_y = int(scene.render.resolution_y * resolution_percentage)
        output_filename = self.filename + ".png"
        filter_type = helper.get_filter_type_from_scene(scene)

        filmCreator = FilmCreator()
        filmCreator.set_image_width(resolution_x)
        filmCreator.set_image_height(resolution_y)
        filmCreator.set_output_filename(output_filename)
        filmCreator.set_filter(filter_type)

        self.filestream.write_sd_data(filmCreator.to_sd_data())

    def export_camera(self, scene: bpy.types.Scene):
        camera_obj = helper.get_active_camera(scene)
        camera_data = camera_obj.data
        
        if camera_data.type == 'PERSP':
            position, rotation, scale = camera_obj.matrix_world.decompose()
            if(abs(scale.x - 1) > 0.00001 or
               abs(scale.y - 1) > 0.00001 or
               abs(scale.z - 1) > 0.00001):
               
               print("Unsupport scale camera.")
               print("scale: {} {} {}".format(scale.x, scale.y, scale.z))
               return
            
            up = rotation @ mathutils.Vector((0, 1, 0))
            direction = rotation @ mathutils.Vector((0, 0, -1))

            fov = math.degrees(camera_data.angle)

            perspectiveCameraCreator = PerspectiveCameraCreator()
            perspectiveCameraCreator.set_position(CrsdVector3r(position))
            perspectiveCameraCreator.set_direction(CrsdVector3r(direction))
            perspectiveCameraCreator.set_up(CrsdVector3r(up))
            perspectiveCameraCreator.set_fov(CrsdReal(fov))

            self.filestream.write_sd_data(perspectiveCameraCreator.to_sd_data())

            # TODO: depth of field and lens system camera

        else:
            print("Unsupport other types of camera currently.")

    def export_renderer(self, scene: bpy.types.Scene):
        sample_number = scene.cadise_render_spp
        sampler = helper.get_sampling_type_from_scene(scene)
        render_method = helper.get_rendering_method_from_scene(scene)

        rendererCreator = RendererCreator()
        rendererCreator.set_render_method(render_method)
        rendererCreator.set_sample_number(sample_number)
        rendererCreator.set_sampler(sampler)

        self.filestream.write_sd_data(rendererCreator.to_sd_data())

    def export_accelerator(self, scene: bpy.types.Scene):
        acceleratorCreator = AcceleratorCreator()

        self.filestream.write_sd_data(acceleratorCreator.to_sd_data())