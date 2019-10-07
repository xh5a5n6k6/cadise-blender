from ..base import setting

import bpy

class CadiseMaterialPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    COMPAT_ENGINES = {setting.cadise_id_name}

    @classmethod
    def poll(cls, context):
        render_panel_setting = context.scene.render
        return render_panel_setting.engine in cls.COMPAT_ENGINES


# collect all material panel classes
CADISE_MATERIAL_PANEL_CLASS = []


# add all render panels into moduleManager
def include_submodule(moduleManager):
    for panel_cls in CADISE_MATERIAL_PANEL_CLASS:
        moduleManager.add_class(panel_cls)