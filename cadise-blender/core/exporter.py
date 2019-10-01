
from .export import CrsdExporter
from ..base.module import ModuleBase

import bpy
import bpy_extras

class OBJECT_OT_cadise_exporter(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """
    Export blender scene to cadise renderer scene description
    """

    # bpy.ops.cadise.export
    bl_idname = "object.cadise_exporter"
    bl_label = "CRSD Export"

    # ExportHelper mixin class uses this
    filename_ext = ""

    # filter_glob: StringProperty(
    #     default="*.crsd",
    #     options={'HIDDEN'},
    #     maxlen=255,  # Max internal buffer length, longer would be clamped.
    # )

    is_animation: bpy.props.BoolProperty (
        name = "Export Animation",
        description = "Export a series of scene files according to frame setting",
        default = False
    )

    def execute(self, context):
        scene = context.scene

        # export frames according to frame setting
        if self.is_animation:
            for frame_number in range(scene.frame_start, scene.frame_end + 1):
                scene.frame_set(frame_number)
                self.export_scene("scene_" + str(frame_number).zfill(5), context.evaluated_depsgraph_get())

        # export current frame
        else:
            self.export_scene("scene", context.evaluated_depsgraph_get())

        return {"FINISHED"}

    def export_scene(self, filename, depsgraph):
        exporter = CrsdExporter(filename)
        exporter.begin(self.filepath)
        exporter.export(depsgraph)
        exporter.end()


# define exporter module and setup its topbar setting
def menu_func_export(self, context):
    self.layout.operator(OBJECT_OT_cadise_exporter.bl_idname, text="Cadise Renderer SD (.crsd)")

class ExportModule(ModuleBase):
    def register(self):
        bpy.utils.register_class(OBJECT_OT_cadise_exporter)
        bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    def unregister(self):
        bpy.utils.unregister_class(OBJECT_OT_cadise_exporter)
        bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


# add exporter module in moduleManager
def include_submodule(moduleManager):
    moduleManager.add_module(ExportModule())