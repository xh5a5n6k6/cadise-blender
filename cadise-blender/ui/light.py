from ..base import setting

import bpy

class CadiseLightPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    COMPAT_ENGINES = {setting.cadise_id_name}

    @classmethod
    def poll(cls, context):
        render_panel_setting = context.scene.render
        return (context.light and
                render_panel_setting.engine in cls.COMPAT_ENGINES)

class CADISE_LIGHT_PT_property(CadiseLightPanel):
    bl_label = "Cadise - Property"

    def draw(self, context):
        light = context.light
        layout = self.layout

        layout.prop(light, "type", expand = True)

        layout.prop(light, "color")
        layout.prop(light, "energy")

        light_type = light.type
        if light_type == 'AREA':
            layout.prop(light, "shape")

            light_shape = light.shape
            if light_shape == 'SQUARE':
                layout.prop(light, "size", text = "Size")
            elif light_shape == 'RECTANGLE':
                layout.prop(light, "size", text = "Width")
                layout.prop(light, "size_y", text = "Height")


# collect all light panel classes
CADISE_LIGHT_PANEL_CLASS = [
    CADISE_LIGHT_PT_property
]


# add all render panels into moduleManager
def include_submodule(moduleManager):
    for panel_cls in CADISE_LIGHT_PANEL_CLASS:
        moduleManager.add_class(panel_cls)