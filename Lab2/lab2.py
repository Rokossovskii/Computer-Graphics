import math
import numpy as np
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def spin(angle):
    #glRotatef(angle,1.0,0.0,0.0)
    glRotatef(angle,0.0,1.0,0.0)
    #glRotatef(angle,0.0,0.0,1.0)

def axes():
    glBegin(GL_LINES)
    
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def pointed_egg(egg_matrix):
    
    for row in egg_matrix:
        for vertex in row:
            glColor3d(255/255, 255/255, 204/255)
            glBegin(GL_POINTS)
            glVertex3f(*vertex)
            glEnd()

def connected_egg(egg_matrix):
    for index_i,row in enumerate(egg_matrix):
        length = len(row)       
        
        for index_j,vertex in enumerate(row):
            glColor3d(255/255, 255/255, 204/255)

            glBegin(GL_LINE_LOOP)
            glVertex3f(*vertex)
            glVertex3f(*egg_matrix[index_i,(index_j+1)%length,:])
            glVertex3f(*egg_matrix[(index_i+1)%length,index_j,:])
            glEnd()
        
def triangled_egg(egg_matrix):
    for index_i,row in enumerate(egg_matrix):
        length = len(row)       
        
        for index_j,vertex in enumerate(row):
            glColor3d(255/255, 255/255, 204/255)

            glBegin(GL_POLYGON)
            glVertex3f(*vertex)
            glVertex3f(*egg_matrix[index_i,(index_j+1)%length,:])
            glVertex3f(*egg_matrix[(index_i+1)%length,index_j,:])
            glEnd()

def egg(n):
    
    return np.ndarray(shape=(n+1,n+1,3),
                      buffer=np.array([[egg_function(i/n,j/n) for i in range(n+1)] for j in range(n+1)],
                                      float))

def egg_function(u,v):
    x = (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u)*math.cos(v*math.pi)
    y = 160*u**4 - 320*u**3 + 160*u**2 - 5
    z = (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u)*math.sin(v*math.pi)
    return [x,y,z]
    

def render(time,shape,n):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()

    spin(time*180/math.pi)
    shape(egg(n))

    axes()

    glFlush()



