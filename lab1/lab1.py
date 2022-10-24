from random import random
from OpenGL.GL import *

def reinbow_triangle(a, b, c):

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(*a)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(*b)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(*c)
    glEnd()

    glFlush()

def triangle(a,b,c):
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_TRIANGLES)
    glVertex2f(*a)
    glVertex2f(*b)
    glVertex2f(*c)
    glEnd()
    glFlush()

def inverted_background_triangle(a,b,c,depth):
    m_ab,m_bc,m_ac=middle_between_two_points(a,b),middle_between_two_points(b,c),middle_between_two_points(c,a)
    if(depth > 0):

        triangle(m_ab,m_bc,m_ac)

        inverted_background_triangle(a,m_ab,m_ac,depth-1)
        inverted_background_triangle(b,m_bc,m_ab,depth-1)
        inverted_background_triangle(c,m_ac,m_bc,depth-1)
    
        
def square(
    x: int = -50,
    y: int = -50,
    a: int = 100,
    b: int = 100,
    color: list = [0.0,0.0,0.0]
):
    vertices = [[x,y],[x,y+b],[x+a,y+b],[x+a,y]]
    glBegin(GL_POLYGON)
    glColor3f(*color)
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()

def deform_square(d: float = 0.0):
    square(x=-50-50*d,y=-50-50*d,a=100+100*d,b=100+100*d,color=[(d**2)%1,d,(d**3)%1])

def sierpinski_carpet(depth=4,starting_point = [-90,-70],a=180,b=140):
    if(depth > 0):
        a=a/3
        b=b/3
        new_starting_coordinants = [[starting_point[0]+a*i,starting_point[1]+b*j] for i in range(3) for j in range(3)]
        new_starting_coordinants.remove(new_starting_coordinants[4])
        for vertex in new_starting_coordinants:
            sierpinski_carpet(depth-1,vertex,a,b)
        
    else:
        square(*starting_point,a,b,color=[0.3,0.0,0.0])
        
def sierpinski_triangle(a, b, c, depth = 3):
    reinbow_triangle(a,b,c)
    inverted_background_triangle(a,b,c,depth)
    
    
def middle_between_two_points(a,b):
    return (a[0]+b[0])/2,(a[1]+b[1])/2

def render(time,shape,rest):
    glClear(GL_COLOR_BUFFER_BIT)
    shape(*rest)

    