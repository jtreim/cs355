import sys
import math

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
CAMERA_SPEED = 1
camera = {}
camera['x'] = 0
camera['y'] = 0
camera['z'] = -20
camera['near'] = 1.0
camera['far'] = 50.0
camera['rotate'] = 0
camera['perspective'] = True

def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera['perspective']:
        gluPerspective(50, DISPLAY_WIDTH/DISPLAY_HEIGHT, camera['near'], camera['far'])
    else:
        glOrtho(-10, 10, -10, 10, camera['near'], camera['far'])

    glRotated(camera['rotate'], 0, 1, 0)
    glTranslated(camera['x'], camera['y'], camera['z'])
    
    
    drawHouse()

    
    glFlush()
    

def keyboard(key, x, y):
    
    if key == chr(27):
        import sys
        sys.exit(0)
  
    if key == b'w':
        camera['z'] += math.cos(math.radians(camera['rotate'])) * CAMERA_SPEED
        camera['x'] -= math.sin(math.radians(camera['rotate'])) * CAMERA_SPEED
    if key == b's':
        camera['z'] -= math.cos(math.radians(camera['rotate'])) * CAMERA_SPEED
        camera['x'] += math.sin(math.radians(camera['rotate'])) * CAMERA_SPEED
  
    if key == b'a':
        camera['z'] += math.sin(math.radians(camera['rotate'])) * CAMERA_SPEED
        camera['x'] += math.cos(math.radians(camera['rotate'])) * CAMERA_SPEED
    if key == b'd':
        camera['z'] -= math.sin(math.radians(camera['rotate'])) * CAMERA_SPEED
        camera['x'] -= math.cos(math.radians(camera['rotate'])) * CAMERA_SPEED

    if key == b'r':
        camera['y'] -= CAMERA_SPEED
    if key == b'f':
        camera['y'] += CAMERA_SPEED

    if key == b'e':
        camera['rotate'] += CAMERA_SPEED
    if key == b'q':
        camera['rotate'] -= CAMERA_SPEED

    if key == b'h':
        camera['x'] = 0
        camera['y'] = 0
        camera['z'] = -20
        camera['rotate'] = 0

    if key == b'o':
        camera['perspective'] = False
    if key == b'p':
        camera['perspective'] = True
  
    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
