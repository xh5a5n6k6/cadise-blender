from . import setting

import bpy

class CadiseRenderPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    
    COMPAT_ENGINES = {setting.cadise_id_name}

    @classmethod
    def poll(cls, context):
        render_panel_setting = context.scene.render
        return render_panel_setting.engine in cls.COMPAT_ENGINES