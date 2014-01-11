'''
Created on Jan 11, 2014

@author: sushant
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from MarchingSquare import *

#Globals
winHeight = 400
winWidth = 400
msHandler = -1
ESCAPE = '\033'
window = 0
showGrid = True


def init():    
    global msHandler
    msHandler = MarchingSquareHandler()
    
    msHandler.setWindow(winWidth,winHeight)
    msHandler.setGridSize(10)
    msHandler.setRadius(150)
    
    msHandler.compute()


def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    global lineList,showGrid
    
    glLoadIdentity()
    glOrtho(0,winWidth,winHeight,0,0.0,100.0)
    glClearColor( 1,1,1,1)
    glClearDepth( 1.0)
    glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)    
    glColor3f(0,0,0)
        
    lineList = msHandler.getLineList()
    gridSize = msHandler.getGridSize()
    
    if showGrid:
        glBegin(GL_LINES)
        for i in range(0,400,gridSize):
            glVertex2f(i,0)
            glVertex2f(i,400)
            
            glVertex2f(0,i)
            glVertex2f(400,i)
        glEnd()
    
    glBegin(GL_LINES)
    for i in range(len(lineList)-1):
        dline = lineList[i]
        glVertex2f(dline[0][0],dline[0][1])
        glVertex2f(dline[1][0],dline[1][1])
    glEnd()
            
    glutSwapBuffers()


def keyPressed(*args):
    global showGrid
    if args[0] == ESCAPE:
        sys.exit()
    elif args[0] == 's':
        if showGrid:
            showGrid=False
        else:
            showGrid=True
        

def main():
    global window
    
    glutInit(sys.argv)
    
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(winWidth,winHeight)

    glutInitWindowPosition(0, 0)

    window = glutCreateWindow("Marching Square")
    
    glutDisplayFunc(DrawGLScene)
    
    glutIdleFunc(DrawGLScene)

    glutReshapeFunc(ReSizeGLScene)

    glutKeyboardFunc(keyPressed)

    init()

    glutMainLoop()

print "(s) to show/hide grid"
print "Hit ESC key to quit."
main()
