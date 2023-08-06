"""
Use this file for VScode debug only.

"""
import bpy

from batoms.batoms import Batoms
from batoms.batom import Batom

bl_info = {
    "name": "Batoms",
    "author": "Xing Wang",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "description": "Python module for drawing and rendering beautiful atoms and molecules using blender.",
    "warning": "",
}

# Register
classes = [    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":

    register()
