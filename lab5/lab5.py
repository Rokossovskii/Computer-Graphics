import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

image_vertex = [[0.0,0.0],[1.0,0.0],[0.5,1.0]]

def triangle_strip_egg_horizontal(egg_matrix):
    matrix_len = len(egg_matrix)
    for index_i in range(matrix_len-11):    
        
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(*egg_matrix[0,index_i,:])
        for index_j in range(matrix_len-1):
            
            glVertex3f(*egg_matrix[index_j,index_i+1,:])
            glVertex3f(*egg_matrix[index_j+1,index_i,:])
        glVertex3f(*egg_matrix[index_j+1,index_i+1,:])
        glEnd()
    for index_i in reversed(range(10,20)):    
        
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(*egg_matrix[0,index_i-2,:])
        for index_j in reversed(range(matrix_len-1)):
            glVertex3f(*egg_matrix[index_j,index_i+1,:])
            glVertex3f(*egg_matrix[index_j+1,index_i,:])
        glVertex3f(*egg_matrix[index_j,index_i,:])
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

def calculate_posision_of_vertices(height,bottom_edge_len,start_vertex):
    verticies_arr = [start_vertex]
    for alpha in [45,135,225]:
        verticies_arr.append([
                              start_vertex[0]+math.sin(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len,
                              start_vertex[1]-height,
                              start_vertex[2]+math.cos(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len
                              ])
    verticies_arr.append(start_vertex)
    for alpha in [225,315,45]:
        verticies_arr.append([
                              start_vertex[0]+math.sin(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len,
                              start_vertex[1]-height,
                              start_vertex[2]+math.cos(math.radians(alpha))*(math.sqrt(2)/2)*bottom_edge_len
                              ])
    verticies_arr.append(start_vertex)
    return verticies_arr

def draw_piraid(ver_arr):
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(7):
        for vertex,img_ver in zip(ver_arr[i:i+3],image_vertex):
            glTexCoord2f(*img_ver)
            glVertex3f(*vertex)
    glEnd()

def egg_shape():
    triangle_strip_egg_horizontal(egg(20))

def piramid_shape():
    height,edge_len,vertex = 5,5,[0,2,0]
    draw_piraid(calculate_posision_of_vertices(height,edge_len,vertex))