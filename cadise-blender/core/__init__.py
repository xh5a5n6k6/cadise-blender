from . import (
    exporter,
    renderer
)

import bpy

class CadiseAddonPreferences(bpy.types.AddonPreferences):
    # According T.C. Chang's work, this must match add-on's name
    # https://github.com/TzuChieh/Photon-v2/blob/develop/BlenderAddon/PhotonBlend/bmodule/__init__.py
    bl_idname = __package__.split('.')[0]

    install_path: bpy.props.StringProperty (
        name = "Installation Path",
        description = "Installation path to Cadise renderer (binary)",
        subtype = "DIR_PATH",
        default = ""
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "install_path")

def include_submodule(moduleManager):
    moduleManager.add_class(CadiseAddonPreferences)

    exporter.include_submodule(moduleManager)
    renderer.include_submodule(moduleManager)