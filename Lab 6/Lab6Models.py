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

class Camera:
	SPEED = 1
	def __init__(self):
		self._x = -30.0
		self._y = -10.0
		self._z = -60.0
		self.near = 1.0
		self.far = 100.0
		self._rotate = -20
		self.perspective = True
		self.reset()

	def rotate_right(self):
		self.rotate -= self.SPEED

	def rotate_left(self):
		self.rotate += self.SPEED

	def forward(self):
		self.z += math.cos(math.radians(self.rotate)) * self.SPEED
		self.x -= math.sin(math.radians(self.rotate)) * self.SPEED

	def back(self):
		self.z -= math.cos(math.radians(self.rotate)) * self.SPEED
		self.x += math.sin(math.radians(self.rotate)) * self.SPEED

	def left(self):
		self.z += math.sin(math.radians(self.rotate)) * self.SPEED
		self.x += math.cos(math.radians(self.rotate)) * self.SPEED

	def right(self):
		self.z -= math.sin(math.radians(self.rotate)) * self.SPEED
		self.x -= math.cos(math.radians(self.rotate)) * self.SPEED
	
	def up(self):
		self.y -= self.SPEED

	def down(self):
		self.y += self.SPEED

	def reset(self):
		self.x = self._x
		self.y = self._y
		self.z = self._z
		self.rotate = self._rotate


class VirtualObject:
	def __init__(self, x, y, z, rotate_y, rotate_z):
		self._x = x
		self._y = y
		self._z = z
		self._rotate_y = rotate_y
		self._rotate_z = rotate_z
		self.reset()

	def reset(self):
		self.x = self._x
		self.y = self._y
		self.z = self._z
		self.rotate_y = self._rotate_y
		self.rotate_z = self._rotate_z


DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
camera = Camera()
houses = [VirtualObject(0.0, 0.0, 0.0, 0, 0), VirtualObject(15.0, 0.0, 0.0, 0, 0),
		  VirtualObject(30.0, 0.0, 0.0, 0, 0), VirtualObject(0.0, 0.0, 30.0, 180, 0),
		  VirtualObject(15.0, 0.0, 30.0, 180, 0), VirtualObject(30.0, 0.0, 30.0, 180, 0),
		  VirtualObject(-15.0, 0.0, 15.0, 90, 0)]
car = VirtualObject(5.0, .25, 12.0, 0, 0)
tires = [VirtualObject(2.0, 0.0, 2.0, 0, 0), VirtualObject(-2.0, 0.0, 2.0, 0, 0),
		 VirtualObject(2.0, 0.0, -2.0, 0, 0), VirtualObject(-2.0, 0.0, -2.0, 0, 0)]

def updateCar(tire_rotate_z):
	for tire in tires:
		tire.rotate_z += tire_rotate_z
	car.x += .2
	glutPostRedisplay()
	glutTimerFunc(100, updateCar, -5)

def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawCar():
	glLineWidth(2.5)
	glColor3f(0.0, 1.0, 0.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-3, 2, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 2, 2)
	#Back Side
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 2, -2)
	#Connectors
	glVertex3f(-3, 2, 2)
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, -2)
	glEnd()
	
def drawTire():
	glLineWidth(2.5)
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-1, .5, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, .5, .5)
	#Back Side
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, .5, -.5)
	#Connectors
	glVertex3f(-1, .5, .5)
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, -.5)
	glEnd()

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

    if camera.perspective:
        gluPerspective(50, DISPLAY_WIDTH/DISPLAY_HEIGHT, camera.near, camera.far)
    else:
        glOrtho(-10, 10, -10, 10, camera.near, camera.far)

    glRotated(camera.rotate, 0, 1, 0)
    glTranslated(camera.x, camera.y, camera.z)
    
    for house in houses:
		glPushMatrix()
		glTranslated(house.x, house.y, house.z)
		glRotated(house.rotate_y, 0, 1, 0)
		drawHouse()
		glPopMatrix()
	
    glPushMatrix()
    glTranslated(car.x, car.y, car.z)
    glRotated(car.rotate_y, 0, 1, 0)
    drawCar()
    for tire in tires:
		glPushMatrix()
		glTranslated(tire.x, tire.y, tire.z)
		glRotated(tire.rotate_y, 0, 1, 0)
		glRotated(tire.rotate_z, 0, 0, 1)
		drawTire()
		glPopMatrix()
    glPopMatrix()
    
    glFlush()
    

def keyboard(key, x, y):
    if key == chr(27):
        import sys
        sys.exit(0)
  
    if key == b'w':
        camera.forward()

    if key == b's':
        camera.back()
  
    if key == b'a':
        camera.left()

    if key == b'd':
        camera.right()

    if key == b'r':
        camera.up()

    if key == b'f':
        camera.down()

    if key == b'e':
        camera.rotate_right()

    if key == b'q':
        camera.rotate_left()

    if key == b'h':
        camera.reset()
        car.reset()
        for tire in tires:
        	tire.reset()

    if key == b'o':
        camera.perspective = False
    if key == b'p':
        camera.perspective = True
  
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(10, updateCar, -5)
glutMainLoop()
