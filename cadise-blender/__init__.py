from .base.module import ModuleManager

bl_info = {
    "name": "Cadise",
    "description": "Blender scene exporter for Cadise renderer.",
    "author": "Chia-Yu Chou",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Render Panel > Render Engine Menu",
    "warning": "WIP...",
    "category": "Render"
}

module_path = __name__
moduleManager = None

# register() is a function which only runs when enabling the add-on, 
# this means the module can be loaded without activating the add-on.
def register():
    global moduleManager

    moduleManager = ModuleManager()
    moduleManager.initialize(module_path)
    moduleManager.register_all()

# unregister() is a function to unload anything setup by register(), 
# this is called when the add-on is disabled.
def unregister():
    global moduleManager

    moduleManager.unregister_all()
    moduleManager = None