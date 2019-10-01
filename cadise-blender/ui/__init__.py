from . import (
    light,
    material,
    render,
)


# add all ui modules
def include_submodule(moduleManager):
    light.include_submodule(moduleManager)
    material.include_submodule(moduleManager)
    render.include_submodule(moduleManager)