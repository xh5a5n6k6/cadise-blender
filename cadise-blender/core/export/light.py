from ...base import helper
from ...base.stream import FileStream
from ...crsd.crsd_light import (
    PointLightCreator,
    AreaLightCreator
)
from ...crsd.crsd_mesh import RectangleCreator
from ...crsd.crsd_type import (
    CrsdReal,
    CrsdVector3r
)

import bpy
import mathutils

def light_export_sd(light_obj: bpy.types.Light, filestream: FileStream):
    light_data = light_obj.data

    if light_data.type == 'POINT':
        position, _, _ = light_obj.matrix_world.decompose()
        color = light_data.color
        color_vector = mathutils.Vector((color.r, color.g, color.b))
        watt = light_data.energy

        cadise_vector_position = helper.to_cadise_vector(position)

        pointLightCreator = PointLightCreator()
        pointLightCreator.set_position(CrsdVector3r(cadise_vector_position))
        pointLightCreator.set_color(CrsdVector3r(color_vector))
        pointLightCreator.set_watt(CrsdReal(watt))

        filestream.write_sd_data(pointLightCreator.to_sd_data())
    elif light_data.type == 'AREA':
        if light_data.shape == 'SQUARE' or light_data.shape == 'RECTANGLE':
            # export primitive first
            width = light_data.size
            height = light_data.size_y if light_data.shape == 'RECTANGLE' else width

            half_width = width / 2.0
            half_height = height / 2.0

            local_to_world_matrix = light_obj.matrix_world

            v1 = mathutils.Vector((-half_width, -half_height, 0.0))
            v2 = mathutils.Vector((half_width, -half_height, 0.0))
            v3 = mathutils.Vector((half_width, half_height, 0.0))

            cadise_vector_v1 = helper.to_cadise_vector(local_to_world_matrix @ v1)
            cadise_vector_v2 = helper.to_cadise_vector(local_to_world_matrix @ v2)
            cadise_vector_v3 = helper.to_cadise_vector(local_to_world_matrix @ v3)

            rectangleCreator = RectangleCreator()
            rectangleCreator.set_name(light_obj.name)
            rectangleCreator.set_v1(CrsdVector3r(cadise_vector_v1))
            rectangleCreator.set_v2(CrsdVector3r(cadise_vector_v2))
            rectangleCreator.set_v3(CrsdVector3r(cadise_vector_v3))

            filestream.write_sd_data(rectangleCreator.to_sd_data())

            # export area light
            color = light_data.color
            color_vector = mathutils.Vector((color.r, color.g, color.b))
            watt = light_data.energy

            areaLightCreator = AreaLightCreator()
            areaLightCreator.set_primitive(light_obj.name)
            areaLightCreator.set_color(CrsdVector3r(color_vector))
            areaLightCreator.set_watt(CrsdReal(watt))

            filestream.write_sd_data(areaLightCreator.to_sd_data())
        else:
            print("Unsupported shape of area light")
    else:
        print("Unsupported light type")