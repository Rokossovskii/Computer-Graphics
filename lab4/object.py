import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Object_in_3D():

    def __init__(self, object_material_settings, obj0_shiness) -> None:
        self.ambient = object_material_settings[0,:]
        self.diffuse = object_material_settings[1,:]
        self.specular = object_material_settings[2,:]
        self.shininess = obj0_shiness

        glMaterialfv(GL_FRONT, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialf(GL_FRONT, GL_SHININESS, self.shininess)

    def render_object(object_building_instruction):
        object_building_instruction()
    
    def move_object(self):
        pass