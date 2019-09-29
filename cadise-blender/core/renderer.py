from ..base import (
    module,
    setting
)

from bl_ui import (
    properties_output,
    properties_data_camera
)

import bpy

class CadiseRenderEngine(bpy.types.RenderEngine):
    # These three members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = setting.cadise_id_name
    bl_label = "Cadise"
    bl_use_preview = False

    # Init is called whenever a new render engine instance is created. Multiple
    # instances may exist at the same time, for example for a viewport and final
    # render.
    def __init__(self):
        super.__init__()

    # When the render engine instance is destroy, this is called. Clean up any
    # render engine data here, for example stopping running render threads.
    def __del__(self):
        pass

    # This is the method called by Blender for both final renders (F12) and
    # small preview for materials, world and lights.
    def render(self, depsgraph):
        self.report({"ERROR"}, "It is unsupported to render in blender currently, please export scene file instead.")

    # For viewport renders, this method gets called once at the start and
    # whenever the scene or 3D viewport changes. This method is where data
    # should be read from Blender in the same thread. Typically a render
    # thread will be started to do the work while keeping Blender responsive.
    def view_update(self, context, depsgraph):
        pass

    # For viewport renders, this method is called whenever Blender redraws
    # the 3D viewport. The renderer is expected to quickly draw the render
    # with OpenGL, and not perform other expensive work.
    # Blender will draw overlays for selection and editing on top of the
    # rendered image automatically.
    def view_draw(self, context, depsgraph):
        pass


# define render module and setup its compatible panels
class RenderModule(module.ModuleBase):
    def register(self):
        bpy.utils.register_class(CadiseRenderEngine)

        properties_output.RENDER_PT_dimensions.COMPAT_ENGINES.add(setting.cadise_id_name)

    def unregister(self):
        bpy.utils.unregister_class(CadiseRenderEngine)

        properties_output.RENDER_PT_dimensions.COMPAT_ENGINES.remove(setting.cadise_id_name)


# add render module in moduleManager
def include_submodule(moduleManager):
    moduleManager.add_module(RenderModule())