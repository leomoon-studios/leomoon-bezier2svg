# Created by Styriam Sp. z o.o.

bl_info = {
    "name": "LeoMoon Bezier2SVG",
    "author": "LeoMoon Studios - www.LeoMoon.com",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Export > Bezier2SVG",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export"
    }
    
import bpy


# register
################################## 


from . import controller

from . import auto_load

auto_load.init(ignore=("addon_updater", "addon_updater_ops"))

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()