from . import (
    ui_light,
    ui_material,
    ui_render,
)


# add all ui modules
def include_submodule(moduleManager):
    ui_light.include_submodule(moduleManager)
    ui_material.include_submodule(moduleManager)
    ui_render.include_submodule(moduleManager)