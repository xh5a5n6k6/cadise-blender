from . import (
    exporter,
    renderer
)

def include_submodule(moduleManager):
    exporter.include_submodule(moduleManager)
    renderer.include_submodule(moduleManager)