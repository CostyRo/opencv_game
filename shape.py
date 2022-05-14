import pygame as pg
from const import HEIGHT,SCREEN
# import pygame with alias pg and import necessary constants from const module

class Shape:

	"""Class for creating shape objects(circle, square, triangle)"""

	size=HEIGHT//10
	gravity=HEIGHT//100
	# variables for size and gravity of the object

	def __init__(self,x,y,color,shape):

		"""Init method for Shape class"""

		self.x=x
		self.y=y
		# initialise the coordinates of the shape

		self.color=color
		# initialise the color of the shape

		self.shape=shape
		# initialise the type of the shape

	def collision(self,rect):

		"""Method for determinating if the shape collides with the player"""

		if self.shape=="circle": return rect.colliderect(pg.Rect(self.x-self.size//2,self.y-self.size//2,self.size,self.size))
		# if the type of the shape is circle
		# check for collision with the circumscribed square
		elif self.shape=="square": return rect.colliderect(pg.Rect(self.x,self.y,self.size,self.size))
		# if the type of the shape is square
		# check for simple collision
		else: return rect.colliderect(pg.Rect(self.x-self.size//2,self.y,self.size,self.size))
		# if the type of the shape is triangle
		# check for collision with the circumscribed square

	def draw(self):

		"""Method to draw the shape on the screen"""

		if self.shape=="circle": pg.draw.circle(SCREEN,self.color,(self.x,self.y),self.size//2,0)
		# if the type of the shape is circle
		# draw a circle with the center in x,y coordinates
		# and with the radius of half of the shape's size
		elif self.shape=="square": pg.draw.rect(SCREEN,self.color,(self.x,self.y,self.size,self.size))
		# if the type of the shape is square
		# draw a rect with the left up corner in x,y coordinates
		# and with height and width of the shape's size
		else: pg.draw.polygon(SCREEN,self.color,[(self.x,self.y),(self.x-self.size//2,self.y+self.size*3**(1/2)//2),(self.x+self.size//2,self.y+self.size*3**(1/2)//2)])
		# if the type of the shape is triangle
		# draw a polygon with 3 points(definiton of a triangle)
		# first point is the given point, point with coordinates x,y
		# now you need to calculate the remaining 2 points
		# the triangle is equilateral
		# so the given point is included in the median
		# with this i can calculate the x1 and x2 of the remaining 2 points
		# x1 is x minus half of the size of the triangle
		# and x2 is x plus half of the size of the triangle
		# in a equilateral triangle the height is size√3/2
		# then the y1 and y2 will be y plus height of the triangle
		# with these points i can draw a equilateral triangle

	def fall(self):

		"""Method to aply gravity"""

		self.y+=self.gravity
		# increase the y coordinate with the gravity