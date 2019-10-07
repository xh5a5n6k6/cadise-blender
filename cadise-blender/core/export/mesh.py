from ...crsd.crsd_mesh import TriangleMeshCreator
from ...crsd.crsd_type import (
    CrsdVector3r,
    CrsdVector3rArray
)

import mathutils

def mesh_to_sd_data(vertices,
                    loop_triangles,
                    mesh_name,
                    material_name,
                    has_custom_normals: bool,
                    uv_loops):
    
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
            positions.append(vertex.co)

            if not has_custom_normals:
                normals.append(vertex.normal if loop_triangle.use_smooth else loop_triangle.normal)
        
        if has_custom_normals:
            split_normals = loop_triangle.split_normals
            for split_normal in split_normals:
                normals.append(split_normal)
        
        for loop_index in loop_triangle.loops:
            uv = uv_loops[loop_index].uv if uv_loops is not None else (0.0, 0.0)
            uvws.append(mathutils.Vector((uv[0], uv[1], 0.0)))

    # store vector list as CrsdVector3rArray
    crsd_positions = CrsdVector3rArray()
    for position in positions:
        crsd_positions.append(CrsdVector3r(position))

    crsd_normals = CrsdVector3rArray()
    for normal in normals:
        crsd_normals.append(CrsdVector3r(normal))

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