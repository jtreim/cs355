# Import a library of functions called 'pygame'
import pygame
import numpy as np
from math import pi, sin, cos, tan, radians

class Camera:
	SPEED = 1
	def __init__(self):
		self._x = 0.0
		self._y = 0.0
		self._z = 0.0
		self.near = 1.0
		self.far = 100.0
		self.fov = 60
		self._rotate = 0
		self.reset()

	def translate_matrix(self):
		return np.matrix('1 0 0 %s; '
					 	'0 1 0 %s; '
					 	'0 0 1 %s; '
					 	'0 0 0 1' % (-1*self.x, -1*self.y, -1*self.z))

	def rotate_matrix(self):
		r = radians(self.rotate)
		c = cos(r)
		s = sin(r)
		return np.matrix('%s 0 %s 0; '
						 '0 1 0 0; '
						 '%s 0 %s 0; '
						 '0 0 0 1' % (c, -1*s, s, c))
	
	def clip_matrix(self):
		fov = radians(self.fov/2)
		zoom = 1/(tan(fov))
		a = (self.far + self.near)/(self.far - self.near)
		b = -2 * self.near * self.far/(self.far - self.near)

		return np.matrix('%s 0 0 0; '
						 '0 %s 0 0; '
						 '0 0 %s %s; '
						 '0 0 1 0' % (zoom, zoom, a, b))

	def in_frustum(self, obj_matrix):
		clipped = np.matmul(self.clip_matrix(), obj_matrix)
		max = abs(clipped[3])
		min = -1 * max

		return (clipped[0] in range(min, max) and
				clipped[1] in range(min, max) and
				clipped[2] in range(min, max))

	def canonical_matrix(self, obj_matrix):
		clipped = np.matmul(self.clip_matrix(), obj_matrix)
		clipped /= clipped[3]
		return np.matrix('%s; %s; 1' % (clipped[0,0], clipped[1,0]))

	def make_camera_centric(self, object_matrix):
		matrix = np.matmul(self.translate_matrix(), object_matrix)
		return np.matmul(self.rotate_matrix(), matrix)

	def rotate_right(self):
		self.rotate -= self.SPEED

	def rotate_left(self):
		self.rotate += self.SPEED

	def forward(self):
		self.z += cos(radians(self.rotate)) * self.SPEED
		self.x -= sin(radians(self.rotate)) * self.SPEED

	def back(self):
		self.z -= cos(radians(self.rotate)) * self.SPEED
		self.x += sin(radians(self.rotate)) * self.SPEED

	def left(self):
		self.z += sin(radians(self.rotate)) * self.SPEED
		self.x += cos(radians(self.rotate)) * self.SPEED

	def right(self):
		self.z -= sin(radians(self.rotate)) * self.SPEED
		self.x -= cos(radians(self.rotate)) * self.SPEED
	
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

	def world_translate_matrix(self):
		return np.matrix('1 0 0 %s; '
						 '0 1 0 %s; '
						 '0 0 1 %s; '
						 '0 0 0 1' % (self.x, self.y, self.z))

	def world_rotate_matrix(self):
		r_y = radians(self.rotate_y)
		r_z = radians(self.rotate_z)
		c_y = cos(r_y)
		c_z = cos(r_z)
		s_y = sin(r_y)
		s_z = sin(r_z)

		y_rotate_matrix = np.matrix('%s 0 %s 0; '
					 				'0 1 0 0; '
					 				'%s 0 %s 0; '
					 				'0 0 0 1' % (c_y, -1*s_y, s_y, c_y))
		z_rotate_matrix = np.matrix('1 0 0 0; '
									'0 %s %s 0; '
									'0 %s %s 0; '
									'0 0 0 1' % (c_z, -1*s_z, s_z, c_z))
		return np.matmul(y_rotate_matrix, z_rotate_matrix) 

	def place_in_world_matrix(self):
		return np.matmul(self.world_translate_matrix(), self.world_rotate_matrix())

	def add_lines(self):
		pass

	def reset(self):
		self.x = self._x
		self.y = self._y
		self.z = self._z
		self.rotate_y = self._rotate_y
		self.rotate_z = self._rotate_z

class House(VirtualObject):
    def add_lines(self):
        model = loadHouse()
        for line in model:
            start = line.start.matrix()
            end = line.end.matrix()

            world_matrix = self.place_in_world_matrix()

            start_matrix = np.matmul(world_matrix, start)
            end_matrix = np.matmul(world_matrix, end)

            if camera.reject_line(start_matrix, end_matrix):
                continue
            s = Point()
            linelist.append()

			


class Car(VirtualObject):
	def add_lines(self):
		model = loadCar()
		

	def add_tires(self):
		model = loadTire()

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y


class Point3D:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def matrix(self):
		return np.matrix([[self.x],
						  [self.y],
						  [self.z],
						  [1]])


class Line3D:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def loadOBJ(filename):
	
	vertices = []
	indices = []
	lines = []
	
	f = open(filename, "r")
	for line in f:
		t = str.split(line)
		if not t:
			continue
		if t[0] == "v":
			vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
			
		if t[0] == "f":
			for i in range(1,len(t) - 1):
				index1 = int(str.split(t[i],"/")[0])
				index2 = int(str.split(t[i+1],"/")[0])
				indices.append((index1,index2))
			
	f.close()
	
	#Add faces as lines
	for index_pair in indices:
		index1 = index_pair[0]
		index2 = index_pair[1]
		lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
		
	#Find duplicates
	duplicates = []
	for i in range(len(lines)):
		for j in range(i+1, len(lines)):
			line1 = lines[i]
			line2 = lines[j]
			
			# Case 1 -> Starts match
			if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
				if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
					duplicates.append(j)
			# Case 2 -> Start matches end
			if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
				if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
					duplicates.append(j)
					
	duplicates = list(set(duplicates))
	duplicates.sort()
	duplicates = duplicates[::-1]
	
	#Remove duplicates
	for j in range(len(duplicates)):
		del lines[duplicates[j]]
	
	return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    
    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))

    return tire

def coordinates(matrix, obj):
	m = np.matmul(obj.place_in_world_matrix(), matrix)
	m = camera.make_camera_centric(m)
	m = camera.canonical_matrix(m)
	m = np.matmul(screen_matrix, m)
	return Point(m[0,0], m[1,0])

# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)
screen_matrix = np.matrix('%s 0 %s; '
						  '0 %s %s; '
						  '0 0 1' % (size[0]/2, size[0]/2, size[1]/-2, size[1]/2))

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)
camera = Camera()
houses = [House(0.0, 0.0, 0.0, 0, 0), House(15.0, 0.0, 0.0, 0, 0),
		  House(30.0, 0.0, 0.0, 0, 0), House(0.0, 0.0, 30.0, 180, 0),
		  House(15.0, 0.0, 30.0, 180, 0), House(30.0, 0.0, 30.0, 180, 0),
		  House(-15.0, 0.0, 15.0, 90, 0)]
cars = [Car(5.0, .25, 12.0, 0, 0)]
tires = [VirtualObject(2.0, 0.0, 2.0, 0, 0), VirtualObject(-2.0, 0.0, 2.0, 0, 0),
		 VirtualObject(2.0, 0.0, -2.0, 0, 0), VirtualObject(-2.0, 0.0, -2.0, 0, 0)]

houseLines = loadHouse()
carLines = loadCar()
tireLines = loadTire()

#Loop until the user clicks the close button.
while not done:
 
	# This limits the while loop to a max of 100 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(100)

	# Clear the screen and set the screen background
	screen.fill(BLACK)

	#Controller Code#
	#####################################################################

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If user clicked close
			done=True
			
	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_w]:
		camera.forward()

	if pressed[pygame.K_s]:
		camera.back()
  	
	if pressed[pygame.K_a]:
		camera.left()

	if pressed[pygame.K_d]:
		camera.right()

	if pressed[pygame.K_r]:
		camera.up()

	if pressed[pygame.K_f]:
		camera.down()

	if pressed[pygame.K_e]:
		camera.rotate_right()

	if pressed[pygame.K_q]:
		camera.rotate_left()

	if pressed[pygame.K_h]:
		camera.reset()
		cars.reset()
		for tire in tires:
			tire.reset()

	linelist = []
	for house in houses:
		house.add_lines()
	for car in cars:
		car.add_lines()
	

	#Viewer Code#
	#####################################################################
	for line in linelist:
		pygame.draw.line(screen, RED, (line.start.x, line.start.y), (line.end.x, line.end.y))

	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()
