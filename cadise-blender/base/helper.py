import bpy
import os

def create_folder(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def get_file_full_name(file_path, file_name):
    return os.path.join(file_path, file_name)


# find specific objects
def get_camera_objects(scene: bpy.types.Scene):
    return [obj for obj in scene.objects if obj.type == 'CAMERA']

def get_light_objects(scene: bpy.types.Scene):
    return [obj for obj in scene.objects if obj.type == 'LIGHT']

def get_mesh_objects(scene: bpy.types.Scene):
    return [obj for obj in scene.objects if obj.type == 'MESH']

def get_active_camera(scene: bpy.types.Scene):
    return scene.camera

def get_materials_from_meshes(mesh_objs):
    materials = []
    for mesh_obj in mesh_objs:
        mesh_data = mesh_obj.data
        for mat in mesh_data.materials[:]:
            # TODO: check material type

            if materials.count(mat) != 0:
                continue

            materials.append(mat)

    return materials


def get_full_mesh_name_with_material(mesh_name, material_index):
    return "{}@{}".format(mesh_name, material_index)


def get_filter_type_from_scene(scene: bpy.types.Scene):
    filter_type = scene.cadise_render_filter_type

    if filter_type == "BOX":
        return "box"
    elif filter_type == "CONE":
        return "cone"
    elif filter_type == "GAUSSIAN":
        return "gaussian"
    elif filter_type == "MITCHELL":
        return "mitchell"
    else:
        print("Unknown filter type, use gaussian filter instead")

        return "gaussian"

def get_sampling_type_from_scene(scene: bpy.types.Scene):
    sampling_type = scene.cadise_render_sampling_type

    if sampling_type == "RANDOM":
        return "random"
    elif sampling_type == "STRATIFIED":
        return "stratified"
    else:
        print("Unknown sampling type, use stratified sampling type instead")

        return "stratified"

def get_rendering_method_from_scene(scene: bpy.types.Scene):
    rendering_method = scene.cadise_render_rendering_method

    if rendering_method == "WHITTED":
        return "whitted"
    elif rendering_method == "PUREPATH":
        return "purePath"
    elif rendering_method == "PATH":
        return "path"
    else:
        print("Unknown rendering method, use path rendering method instead")

        return "path"