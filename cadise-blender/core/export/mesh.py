from ...base import helper
from ...base.stream import FileStream
from ...crsd.crsd_mesh import TriangleMeshCreator
from ...crsd.crsd_type import (
    CrsdVector3r,
    CrsdVector3rArray
)

import bpy
import mathutils

def mesh_to_sd_data(vertices,
                    loop_triangles,
                    has_custom_normals: bool,
                    uv_loops,
                    local_to_world_matrix,
                    mesh_name,
                    material_name):
    
    _, rotation, _ = local_to_world_matrix.decompose()

    positions = []
    normals   = []
    uvws      = []

    for loop_triangle in loop_triangles:
        """
        vertices and loops are different

        Reference Code: 
        https://github.com/TzuChieh/Photon-v2/blob/develop/BlenderAddon/PhotonBlend/bmodule/mesh/triangle_mesh.py
        """
        for vertex_index in loop_triangle.vertices:
            vertex = vertices[vertex_index]
            positions.append(local_to_world_matrix @ vertex.co)

            if not has_custom_normals:
                normal = vertex.normal if loop_triangle.use_smooth else loop_triangle.normal
                normals.append(rotation @ normal)
        
        if has_custom_normals:
            split_normals = loop_triangle.split_normals
            for split_normal in split_normals:
                normals.append(rotation @ split_normal)
        
        for loop_index in loop_triangle.loops:
            uv = uv_loops[loop_index].uv if uv_loops is not None else (0.0, 0.0)
            uvws.append(mathutils.Vector((uv[0], uv[1], 0.0)))

    # store vector list as CrsdVector3rArray
    crsd_positions = CrsdVector3rArray()
    for position in positions:
        cadise_vector_position = helper.to_cadise_vector(position)
        crsd_positions.append(CrsdVector3r(cadise_vector_position))

    crsd_normals = CrsdVector3rArray()
    for normal in normals:
        cadise_vector_normal = helper.to_cadise_vector(normal)
        crsd_normals.append(CrsdVector3r(cadise_vector_normal))

    crsd_uvws = CrsdVector3rArray()
    for uvw in uvws:
        crsd_uvws.append(CrsdVector3r(uvw))

    triangleMeshCreator = TriangleMeshCreator()
    triangleMeshCreator.set_name(mesh_name)
    triangleMeshCreator.set_material(material_name)
    triangleMeshCreator.set_positions(crsd_positions)
    triangleMeshCreator.set_normals(crsd_normals)
    triangleMeshCreator.set_uvws(crsd_uvws)

    return triangleMeshCreator.to_sd_data()

def mesh_export_sd(mesh_obj: bpy.types.Mesh, filestream: FileStream):
    mesh_data = mesh_obj.data
    
    local_to_world_matrix = mesh_obj.matrix_world

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
        uv_data = uv_layer.data if uv_layer is not None else None

        mesh_sd_data = mesh_to_sd_data(
            mesh_data.vertices,
            loop_triangles,
            mesh_data.has_custom_normals,
            uv_data,
            local_to_world_matrix,
            triangle_mesh_name,
            matrial_name,
        )

        filestream.write_sd_data(mesh_sd_data)