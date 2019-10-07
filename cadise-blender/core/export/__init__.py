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
        scene = depsgraph.scene_eval
        
        mesh_objs = helper.get_mesh_objects(scene)
        materials = helper.get_materials_from_meshes(mesh_objs)
        light_objs = helper.get_light_objects(scene)

        for material in materials:
            self.__export_material(material)

        for mesh_obj in mesh_objs:
            self.__export_mesh(mesh_obj)

        for light_obj in light_objs:
            self.__export_light(light_obj)

    def __export_film(self, scene: bpy.types.Scene):
        resolution_x = scene.render.resolution_x
        resolution_y = scene.render.resolution_y
        output_filename = self.__filename + ".png"
        filter_type = helper.get_filter_type_from_scene(scene)

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

            fov = math.degrees(camera_data.angle)

            perspectiveCameraCreator = PerspectiveCameraCreator()
            perspectiveCameraCreator.set_position(CrsdVector3r(position))
            perspectiveCameraCreator.set_direction(CrsdVector3r(direction))
            perspectiveCameraCreator.set_up(CrsdVector3r(up))
            perspectiveCameraCreator.set_fov(CrsdReal(fov))

            self.__filestream.write_sd_data(perspectiveCameraCreator.to_sd_data())

            # TODO: depth of field and lens system camera

        else:
            print("Unsupport other types of camera currently.")

    def __export_renderer(self, scene: bpy.types.Scene):
        sample_number = scene.cadise_render_spp
        sampler = helper.get_sampling_type_from_scene(scene)
        render_method = helper.get_rendering_method_from_scene(scene)

        rendererCreator = RendererCreator()
        rendererCreator.set_render_method(render_method)
        rendererCreator.set_sample_number(sample_number)
        rendererCreator.set_sampler(sampler)

        self.__filestream.write_sd_data(rendererCreator.to_sd_data())

    def __export_accelerator(self, scene: bpy.types.Scene):
        acceleratorCreator = AcceleratorCreator()

        self.__filestream.write_sd_data(acceleratorCreator.to_sd_data())

    def __export_material(self, mat: bpy.types.Material):
        material_sd_data = material.material_to_sd_data(mat)

        if material_sd_data is not None:
            self.__filestream.write_sd_data(material_sd_data)

    def __export_mesh(self, mesh_obj: bpy.types.Mesh):
        mesh_data = mesh_obj.data
        
        # split mesh to triangles
        mesh_data.calc_loop_triangles()

        # check if uses custom normals
        if mesh_data.has_custom_normals:
            mesh_data.calc_normals_split()
        else:
            mesh_data.calc_normals()

        # build material-triangles remapping to export 
        # all triangles with the same material as one triangle-mesh
        material_index_triangle_remapping = {}
        for loop_triangle in mesh_data.loop_triangles:
            material_index = loop_triangle.material_index

            if material_index not in material_index_triangle_remapping.keys():
                material_index_triangle_remapping[material_index] = []
            
            material_index_triangle_remapping[material_index].append(loop_triangle)

        # for each material, export all corrsponding triangles
        # as triangle-mesh
        for material_index in material_index_triangle_remapping.keys():
            material = mesh_obj.material_slots[material_index].material
            loop_triangles = material_index_triangle_remapping[material_index]

            if material is None:
                continue

            triangle_mesh_name = helper.get_full_mesh_name_with_material(mesh_obj.name, material_index)
            matrial_name = material.name

            # It currently only exports one uv map
            uv_layers = mesh_data.uv_layers
            uv_layer = uv_layers.active
            uv_data = uv_layer.data if uv_layer.data is not None else None

            mesh_sd_data = mesh.mesh_to_sd_data(
                mesh_data.vertices,
                loop_triangles,
                triangle_mesh_name,
                matrial_name,
                mesh_data.has_custom_normals,
                uv_data
            )

            self.__filestream.write_sd_data(mesh_sd_data)            

    def __export_light(self, light: bpy.types.Light):
        pass