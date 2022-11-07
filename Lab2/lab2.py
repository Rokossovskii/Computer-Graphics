import math
import numpy as np
import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def spin(angle):
    glRotatef(angle,1.0,0.0,0.0)
    glRotatef(angle,0.0,1.0,0.0)
    glRotatef(angle,0.0,0.0,1.0)

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
    for index_i,row in enumerate(egg_matrix[1:]):      
        
        for index_j,vertex in enumerate(row[1:]):
            glColor3d(255/255, 255/255, 204/255)

            glBegin(GL_LINE_LOOP)
            glVertex3f(*vertex)
            glVertex3f(*egg_matrix[index_i+1,(index_j),:])
            glVertex3f(*egg_matrix[(index_i),index_j+1,:])
            glEnd()
        
def triangled_egg(egg_matrix):
    for index_i,row in enumerate(egg_matrix[1:]):    
        
        for index_j,vertex in enumerate(row[1:]):
            glColor3d(0/255, 0/255, 0/255)

            glBegin(GL_POLYGON)
            glVertex3f(*vertex)
            glVertex3f(*egg_matrix[index_i+1,(index_j),:])
            glVertex3f(*egg_matrix[(index_i),index_j+1,:])
            glEnd()

    for index_i,row in enumerate(egg_matrix[:-1]):    
        
        for index_j,vertex in enumerate(row[:-1]):
            glColor3d(251/255, 95/255, 252/255)

            glBegin(GL_POLYGON)
            glVertex3f(*vertex)
            glVertex3f(*egg_matrix[index_i+1,(index_j),:])
            glVertex3f(*egg_matrix[(index_i),index_j+1,:])
            glEnd()

def triangle_strip_egg_vertical(egg_matrix):
    matrix_len = len(egg_matrix)
    for index_i in range(1,matrix_len):    
        glColor3d(index_i/matrix_len, index_i/matrix_len, index_i/matrix_len)
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(*egg_matrix[index_i,1,:])
        for index_j in range(1,matrix_len):
            
            glVertex3f(*egg_matrix[index_i-1,index_j,:])
            glVertex3f(*egg_matrix[index_i,index_j-1,:])
        glEnd()

def triangle_strip_egg_horizontal(egg_matrix):
    matrix_len = len(egg_matrix)
    for index_i in range(matrix_len-1):    
        
        glColor3d(index_i/matrix_len, index_i/matrix_len, index_i/matrix_len)
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(*egg_matrix[0,index_i,:])
        for index_j in range(matrix_len-1):
            
            glVertex3f(*egg_matrix[index_j,index_i+1,:])
            glVertex3f(*egg_matrix[index_j+1,index_i,:])
        glVertex3f(*egg_matrix[index_j+1,index_i+1,:])
        glEnd()

def sierpinski_piramid(depth,height,edge_len,vertex):
    if depth > 0:
        for ver in calculate_posision_of_vertices(height,edge_len,vertex):
            sierpinski_piramid(depth -1,height-0.5,edge_len-0.5,ver)
    else:
        draw_piraid(calculate_posision_of_vertices(height,edge_len,vertex))
    

def calculate_posision_of_vertices(height,bottom_edge_len,start_vertex):
    verticies_arr = [start_vertex]
    for alpha in [45,135,225]:
        verticies_arr.append([start_vertex[0]+math.sin(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len,
                              start_vertex[1]+math.cos(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len,
                              start_vertex[2]-height])
    verticies_arr.append(start_vertex)
    for alpha in [225,315,45]:
        verticies_arr.append([start_vertex[0]+math.sin(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len,
                              start_vertex[1]+math.cos(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len,
                              start_vertex[2]-height])
    verticies_arr.append(start_vertex)
    return verticies_arr

def draw_piraid(ver_arr):
    glColor3d(255/255, 255/255, 150/255)
    glBegin(GL_TRIANGLE_STRIP)
    for vertex in ver_arr:
        glVertex3f(*vertex)
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

def render2(time,shape,n,height,edge_len,vertex):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time*180/math.pi)
    shape(n,height,edge_len,vertex)

    axes()

    glFlush()