import numpy as np
import math
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Light():

    def __init__(self, light_number, light_settings, optional_light_settings: dict = {'constant':1.0,'linear':0.05,'quadratic':0.001}) -> None:
        self.light_number = light_number
        self.light_settings = light_settings
        self.ambient = self.light_settings[0,:]
        self.diffuse = self.light_settings[1,:]
        self.specular = self.light_settings[2,:]
        self.position = self.light_settings[3,:]

        self.constant =  optional_light_settings.get('constant')
        self.linear = optional_light_settings.get('linear')
        self.quadratic = optional_light_settings.get('quadratic')

        self.glLight()

        glLightf(light_number, GL_CONSTANT_ATTENUATION, self.constant)
        glLightf(light_number, GL_LINEAR_ATTENUATION, self.linear)
        glLightf(light_number, GL_QUADRATIC_ATTENUATION, self.quadratic)

        glEnable(light_number)

    def glLight(self):
        glLightfv(self.light_number, GL_AMBIENT, self.ambient)
        glLightfv(self.light_number, GL_DIFFUSE, self.diffuse)
        glLightfv(self.light_number, GL_SPECULAR, self.specular)
        glLightfv(self.light_number, GL_POSITION, self.position)

    def on_off(self) -> bool:
        if glIsEnabled(self.light_number):
            glDisable(self.light_number)
            return False
        else:
            glEnable(self.light_number)
            return True

    def add_light_settings(self,x,y):
        print(self.light_settings[x,y])
        if self.light_settings[x,y] + 0.1 < 1.0:
            self.light_settings[x,y] += 0.1
            self.glLight()
        

    def sub_light_settings(self,x,y):
        print(self.light_settings[x,y])
        if self.light_settings[x,y] - 0.1 > 0.0:
            self.light_settings[x,y] -= 0.1
            self.glLight()

    def move_light(self, theta, phi):
        x,y,z = math.cos(theta) * math.cos(phi), math.sin(phi), math.sin(theta)* math.cos(phi)
        
        glTranslate(x,y,z)
        glLightfv(self.light_number, GL_POSITION, [x,y,z])
        glTranslate(-x,-y,-z)
        pass