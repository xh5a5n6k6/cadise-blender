from ..base.panel import CadiseRenderPanel

import bpy

class CADISE_RENDER_PT_option(CadiseRenderPanel):
    bl_label = "Cadise Option"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        # layout.prop(scene, "cadise_is_animation")

class CADISE_RENDER_PT_sampling(CadiseRenderPanel):
    bl_label = "Cadise Sampling"

    bpy.types.Scene.cadise_render_spp = bpy.props.IntProperty (
        name = "SPP",
        description = "Samples per pixel",
        default = 4,
        min = 1,
        max = 2 ** 31 - 1
    )

    bpy.types.Scene.cadise_render_sampling_type = bpy.props.EnumProperty(
        items = [
            ("RANDOM", "Random", "Random sampling"),
            ("STRATIFIED", "Stratified", "Stratified jitter sampling")
        ],
        name = "Sampling Type",
        description = "Cadise's sampling types",
        default = "STRATIFIED",
    )

    bpy.types.Scene.cadise_render_filter_type = bpy.props.EnumProperty(
        items = [
            ("BOX", "Box", "Box filter"),
            ("CONE", "Cone", "Cone filter"),
            ("GAUSSIAN", "Gaussian", "Gaussian filter"),
            ("MITCHELL", "Mitchell", "Mitchell filter")
        ],
        name = "Filter Type",
        description = "Cadise's filter types",
        default = "MITCHELL",
    )

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop(scene, "cadise_render_spp")
        layout.prop(scene, "cadise_render_sampling_type")
        layout.prop(scene, "cadise_render_filter_type")


# collect all render panel classes
CADISE_RENDER_PANEL_CLASS = [
    CADISE_RENDER_PT_option,
    CADISE_RENDER_PT_sampling
]


# add all render panels into moduleManager
def include_submodule(moduleManager):
    for panel_cls in CADISE_RENDER_PANEL_CLASS:
        moduleManager.add_class(panel_cls)