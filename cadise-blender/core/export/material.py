# from ...crsd.material import (
#     LambertianDiffuseCreator
# )

import bpy

def material_to_sd_data(material: bpy.types.Material):
    if material.use_nodes:
        mat_sd_data = None



        return mat_sd_data
    
    else:
        print("Only support material with nodes system")
        return None